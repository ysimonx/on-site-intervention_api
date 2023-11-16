from flask import Blueprint, abort, current_app, make_response
from sqlalchemy.orm.interfaces import *
#   from sqlalchemy.orm import RelationshipDirection


from ..model_dir.field import Field
from ..model_dir.type_field import TypeField
from ..model_dir.photo import Photo

from ..model_dir.report import Report
from flask import jsonify, request, abort
from flask_jwt_extended import jwt_required

from .. import db

from ..thingsboard.connector_thingsboard import ThingsboardConnector

app_file_report= Blueprint('report',__name__)





@app_file_report.route("/report", methods=["GET"])
@jwt_required()
def get_reports():
    reports = Report.query.all()
    
    tb=ThingsboardConnector()
    for report in reports:
        tb.syncAssetsFromInstanceAndChildren(report)
            
    return jsonify([item.to_json() for item in reports])


@app_file_report.route("/report/<id>", methods=["GET"])
@jwt_required()
def get_report(id):
    report = Report.query.get(id)
    if report is None:
        abort(make_response(jsonify(error="report is not found"), 404))
       
    return jsonify(report.to_json())

    
@app_file_report.route("/report/<id>", methods=["DELETE"])
@jwt_required()
def delete_report(id):
    report = Report.query.get(id)
    if report is None:
        abort(make_response(jsonify(error="report is not found"), 404))
        
    for item_field in report.fields:
        for item_photo in item_field.photos:
            photo = Photo.query.get(item_photo.id)
            if photo is not None:
                db.session.delete(photo)
                current_app.logger.info('photo deleted id = ' + photo.id)
            
        field = Field.query.get(item_field.id)
        if field is not None:
            db.session.delete(field)
            current_app.logger.info('field deleted id = ' + field.id)
    
    db.session.delete(report)
    current_app.logger.info('report deleted id = ' + report.id)
    
    db.session.commit()
    
     # synchro thingsboard
    tb=ThingsboardConnector()
    tb.delAssetsFromInstanceAndChildren(report)
         
    return jsonify({'result': True})


"""
Exemple de json à envoyer
{
    "report_on_site_uuid": "report_on_site_uuid_value40",
    "intervention_on_site_uuid": "intervention_on_site_uuid_value1",
    "report_name":"visite de l'échafaudage E1",
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

@app_file_report.route('/report', methods=['PUT', 'POST'])
@jwt_required()
def update_report():
    
    # update report
    report_on_site_uuid = request.json.get("report_on_site_uuid", None)
    if report_on_site_uuid is None:
        abort(make_response(jsonify(error="missing report_on_site_uuid parameter"), 400))
        
    report = Report.query.filter(Report.report_on_site_uuid == report_on_site_uuid).first()
    if report is None:
        report_name                 = request.json.get("report_name", None)
        average_latitude            = request.json.get("average_latitude", None)
        average_longitude           = request.json.get("average_longitude", None)
        intervention_on_site_uuid   = request.json.get("intervention_on_site_uuid", None)
        report = Report(
            report_on_site_uuid=report_on_site_uuid,
            report_name=report_name,
            intervention_on_site_uuid=intervention_on_site_uuid,
            average_latitude=average_latitude,
            average_longitude=average_longitude
        )
        db.session.add(report)
        db.session.commit()
    else:
        report.report_name                 = request.json.get("report_name",        report.report_name)
        report.average_latitude            = request.json.get("average_latitude",   report.average_latitude)
        report.average_longitude           = request.json.get("average_longitude",  report.average_longitude)
        report.intervention_on_site_uuid   = request.json.get("intervention_on_site_uuid", report.intervention_on_site_uuid)
        db.session.commit()
    
    arr_children_fields=[]
    dict_children_photos={}
    
    fields = request.json.get("fields", None)
    if (fields is not None):
        for itemfield in fields:
                field = Field.query.filter(Field.field_on_site_uuid == itemfield["field_on_site_uuid"]).first()
                
                if field is None:
                    field = Field(
                        report_id           = report.id,
                        report_on_site_uuid = report.report_on_site_uuid,
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
    tb.syncAssetsFromInstanceAndChildren(report)    
    
    return jsonify({ "message":"ok"}), 200
