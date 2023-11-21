from flask import Blueprint, abort, current_app, make_response
from sqlalchemy.orm.interfaces import *
#   from sqlalchemy.orm import RelationshipDirection


from ..model_dir.field import Field
from ..model_dir.type_field import TypeField
from ..model_dir.photo import Photo

from ..model_dir.form import Form
from flask import jsonify, request, abort
from flask_jwt_extended import jwt_required

from .. import db

from ..thingsboard.connector_thingsboard import ThingsboardConnector

app_file_form= Blueprint('form',__name__)





@app_file_form.route("/form", methods=["GET"])
@jwt_required()
def get_forms():
    forms = Form.query.all()
    
    tb=ThingsboardConnector()
    for form in forms:
        tb.syncAssetsFromInstanceAndChildren(form)
            
    return jsonify([item.to_json() for item in forms])


@app_file_form.route("/form/<id>", methods=["GET"])
@jwt_required()
def get_form(id):
    form = Form.query.get(id)
    if form is None:
        abort(make_response(jsonify(error="form is not found"), 404))
       
    return jsonify(form.to_json())

    
@app_file_form.route("/form/<id>", methods=["DELETE"])
@jwt_required()
def delete_form(id):
    form = Form.query.get(id)
    if form is None:
        abort(make_response(jsonify(error="form is not found"), 404))
        
    for item_field in form.fields:
        for item_photo in item_field.photos:
            photo = Photo.query.get(item_photo.id)
            if photo is not None:
                db.session.delete(photo)
                current_app.logger.info('photo deleted id = ' + photo.id)
            
        field = Field.query.get(item_field.id)
        if field is not None:
            db.session.delete(field)
            current_app.logger.info('field deleted id = ' + field.id)
    
    db.session.delete(form)
    current_app.logger.info('form deleted id = ' + form.id)
    
    db.session.commit()
    
     # synchro thingsboard
    tb=ThingsboardConnector()
    tb.delAssetsFromInstanceAndChildren(form)
         
    return jsonify({'result': True})


"""
Exemple de json à envoyer
{
    "form_on_site_uuid": "form_on_site_uuid_value40",
    "intervention_on_site_uuid": "intervention_on_site_uuid_value1",
    "form_name":"visite de l'échafaudage E1",
    "fields":[
        {
                "field_on_site_uuid": "field_on_site_uuid_value_40",
                "field_name": "hauteur",
                "field_value": "100.1",
                "type_field": "double",
                "average_latitude": 0.1,
                "average_longitude": 0.2,
                "photos_on_site_uuid": [
                    "photo_on_site_uuid_valuec"
                ]
        }
    ]
}
    

"""

@app_file_form.route('/form', methods=['PUT', 'POST'])
@jwt_required()
def update_form():
    
    # update form
    form_on_site_uuid = request.json.get("form_on_site_uuid", None)
    if form_on_site_uuid is None:
        abort(make_response(jsonify(error="missing form_on_site_uuid parameter"), 400))
        
    form = Form.query.filter(Form.form_on_site_uuid == form_on_site_uuid).first()
    if form is None:
        form_name                 = request.json.get("form_name", None)
        average_latitude            = request.json.get("average_latitude", None)
        average_longitude           = request.json.get("average_longitude", None)
        intervention_on_site_uuid   = request.json.get("intervention_on_site_uuid", None)
        form = Form(
            form_on_site_uuid=form_on_site_uuid,
            form_name=form_name,
            intervention_on_site_uuid=intervention_on_site_uuid,
            average_latitude=average_latitude,
            average_longitude=average_longitude
        )
        db.session.add(form)
        db.session.commit()
    else:
        form.form_name                 = request.json.get("form_name",        form.form_name)
        form.average_latitude            = request.json.get("average_latitude",   form.average_latitude)
        form.average_longitude           = request.json.get("average_longitude",  form.average_longitude)
        form.intervention_on_site_uuid   = request.json.get("intervention_on_site_uuid", form.intervention_on_site_uuid)
        db.session.commit()
    
    arr_children_fields=[]
    dict_children_photos={}
    
    fields = request.json.get("fields", None)
    if (fields is not None):
        for itemfield in fields:
                field = Field.query.filter(Field.field_on_site_uuid == itemfield["field_on_site_uuid"]).first()
                
                if field is None:
                    field = Field(
                        form_id           = form.id,
                        form_on_site_uuid = form.form_on_site_uuid,
                    )
              
                if "field_name" in itemfield:
                    field.field_name          = itemfield["field_name"]
                if "field_on_site_uuid" in itemfield:
                    field.field_on_site_uuid  = itemfield["field_on_site_uuid"]
                if "field_value" in itemfield:
                    field.field_value         = itemfield["field_value"]
                if "type_field" in itemfield:
                    type_field_name           = itemfield["type_field"]
                    type_field                = TypeField.query.filter(TypeField.name == type_field_name).first()
                    field.type_field_id       = type_field.id
                if "average_latitude" in itemfield:
                    field.average_latitude    = itemfield["average_latitude"]
                if "average_longitude" in itemfield:
                    field.average_longitude   = itemfield["average_longitude"]

                db.session.add(field)
                db.session.commit()
                arr_children_fields.append(field)
                
                if "photos_on_site_uuid" in itemfield:
                    photos_on_site_uuid = itemfield["photos_on_site_uuid"]
                    
                    arr_photos_linked=[]
                    for photo_on_site_uuid in photos_on_site_uuid:
                        
                        photo = Photo.query.filter(Photo.photo_on_site_uuid == photo_on_site_uuid).first()
                        if photo is not None:
                            
                            # update de la clé étrangère photo->field et annule et écrasement de photo.field_on_site_uuid
                            photo.field_id=field.id 
                            photo.field_on_site_uuid=field.field_on_site_uuid
                            db.session.commit()
                            # ajoute dans un tableau des photos pour remonter thingsboard
                            arr_photos_linked.append(photo) 
                            
                    dict_children_photos[field.id]=arr_photos_linked
                     
    
    tb=ThingsboardConnector()
    tb.syncAssetsFromInstanceAndChildren(form)    
    
    return jsonify({ "message":"ok"}), 200
