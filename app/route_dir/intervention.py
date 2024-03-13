from flask import Blueprint, abort, make_response, current_app, url_for

import hashlib
import pandas as pd
import csv
from unidecode import unidecode

from ..model_dir.intervention import Intervention, InterventionValues
from ..model_dir.type_intervention import TypeIntervention, TypeInterventionSite
from ..model_dir.section import Section
from ..model_dir.form import Form

from ..model_dir.place import Place
from ..model_dir.site import Site
from ..model_dir.form import Form
from ..model_dir.mymixin import User
from ..model_dir.field import Field, FieldValue
from ..model_dir.event import Event
from ..model_dir.field_histo import FieldHisto
from flask import jsonify, request, abort
from flask_jwt_extended import jwt_required

from .. import db, getByIdOrByName, getLastModified
app_file_intervention= Blueprint('intervention',__name__)

import json
from sqlalchemy import func, desc

@app_file_intervention.route("/intervention_old", methods=["GET"])
def get_interventions():
    if not 'site_id' in request.args:
        interventions = Intervention.query.all()
    else:
        _site=getByIdOrByName(Site, request.args.get("site_id"))
        if _site is None:
            abort(make_response(jsonify(error="site is not found"), 404))
        
        interventions = Intervention.query.filter(Intervention.site_id==_site.id).all()
        
    return jsonify([item.to_json() for item in interventions])

@app_file_intervention.route("/intervention_values/<id>", methods=["GET"])
@jwt_required()
def get_intervention_values_id(id):
    intervention_values = InterventionValues.query.get(id)
    if intervention_values is None:
        abort(make_response(jsonify(error="intervention_values is not found"), 404))
    return jsonify(intervention_values.to_json())


@app_file_intervention.route("/intervention_values/csv", methods=["GET"])
def get_intervention_values_csv():
    
    interventionValues = filterInterventionValues()
    
    # feed an dataFrame with headers and values
    # import pandas as pd
    #
    # data = [['Alice', 30, 'New York'], ['Bob', 25, 'Los Angeles']]  # Example 2D array
    # columns = ['Name', 'Age', 'City']  # Header
    # df = pd.DataFrame(data, columns=columns)
    #
    # ou mieux
    # resp = make_response(df.to_csv())
    # resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
    # resp.headers["Content-Type"] = "text/csv"
    # return resp
    # 
    
    site_id=request.args.get("site_id")
    _site=getByIdOrByName(Site, site_id)
    
    type_intervention_id=request.args.get("type_intervention_id")
    _type_intervention=getByIdOrByName(TypeIntervention, type_intervention_id)

    _type_intervention_site = TypeInterventionSite.query.get((_type_intervention.id,_site.id))
    if _type_intervention_site is None:
        abort(make_response(jsonify(error="_type_intervention_site is not found"), 404))

    dictTemplate=json.loads(_type_intervention_site.template_text)
    # return jsonify(json.loads(_type_intervention_site.template_text)),200 
    
    
    data=[]
    columns=[]
    for interventionValue in interventionValues:
        record=[]
        columns=[]
        inits=[ {
            
            
            "label":"hashtag",
                                "value": interventionValue.hashtag},
            {"label":"type_intervention", 
                                "value": interventionValue.type_intervention.name},
            {"label":"id", 
                                "value": interventionValue.id},
            {"label":"status", 
                                "value": interventionValue.status},
            {"label":"assignee_email", 
                                 "value": interventionValue.assignee_user.email if interventionValue.assignee_user is not None else ""},
            {"label":"registre", 
                                "value": interventionValue.name},
            {"label":"place", 
                                "value": interventionValue.place.name},

            {"label":"num_chrono", 
                                "value": interventionValue.num_chrono},
            {"label":"indice", 
                                "value": interventionValue.indice},
            {"label":"feb",
             "value": "https://{}{}".format(request.headers.get('X-Forwarded-Host'), url_for('backoffice.get_interventions_values_id', id=interventionValue.id))
             }
        ]
        
        # http://127.0.0.1:4998/api/v1/intervention_values/csv?site_id=5dc837b9-9678-494c-9b1a-78ff1bf4a17b&type_intervention_id=scaffolding%20request
        for item in inits:
            columns.append(item["label"])
            try :
                value = item["value"] if item["value"] is not None else ""
            except :
                value=""
            record.append(unidecode(str(value)))
            
        dict_field_values={}
        for item in interventionValue.fields_values:
            dict_field_values[item.field_on_site_uuid]=item.value;
            
        for form, form_values in dictTemplate["forms"].items():
            columns.append("formulaire_{}".format(form))    
            record.append(unidecode(form_values["form_name"]))
            for section, section_values in form_values["sections"].items():
                #columns.append("section_{}".format(section))    
                #record.append(section_values["section_name"])
                for field, fields_values in section_values["fields"].items():
                    field_name=fields_values["field_name"]
                    field_on_site_uuid=fields_values["field_on_site_uuid"]
                    columns.append(field_name)
                    if field_on_site_uuid in dict_field_values.keys():
                        value  = dict_field_values[field_on_site_uuid]
                        if len(value) < 200:
                            record.append(unidecode(value))
                        else:
                            record.append("yes")
                    else:
                        record.append("")
            
        
        data.append(record)
        
    df = pd.DataFrame(data, columns=columns)
    S=df.to_csv(index=True, na_rep="", index_label="n", quoting=csv.QUOTE_ALL, sep=";") 
    resp = make_response(S)
    
    resp.headers["Content-Disposition"] = "attachment; filename=export_{}.csv".format(_site.get_urlName())
    resp.headers["Content-Type"] = "text/csv"
    # resp.charset="iso-8859-1"
    
    return resp 
    





@app_file_intervention.route("/intervention_values", methods=["GET"])
@jwt_required()
def get_intervention_values():

    interventionValues = filterInterventionValues()
    
    resp=make_response(jsonify([item.to_json() for item in interventionValues]))
    
    site_id=request.args.get("site_id")
    if site_id is not None:
        _site=getByIdOrByName(Site, site_id)
        if _site is not None:
            maxutc = getLastModified(interventionValues)
            if maxutc is not None:
                resp.headers['X-LastModified'] = maxutc
            if _site.maxutc != maxutc:
                _site.maxutc = maxutc;
                db.session.commit()
            
    return resp


@app_file_intervention.route("/intervention_values/photos", methods=["GET"])
@jwt_required()
def get_intervention_values_photos():
    
    interventionValues = filterInterventionValues()

    resp=make_response(jsonify([item.photos_to_json() for item in interventionValues]))
    
    maxutc = getLastModified(interventionValues)
    if maxutc is not None:
        resp.headers['X-LastModified'] = maxutc

    return resp


@app_file_intervention.route('/intervention_values', methods=['POST'])
@jwt_required()
def post_intervention_values():
    
    if not request.json:
        abort(make_response(jsonify(error="no json provided in request"), 400))

    intervention_values_on_site_uuid   = request.json.get('intervention_values_on_site_uuid')
    site_id                     = request.json.get('site_id')
    type_intervention_id        = request.json.get('type_intervention_id')
    intervention_name           = request.json.get('intervention_name')
    place                       = request.json.get('place')
    template_text               = request.json.get('template_text')
    field_on_site_uuid_values   = request.json.get('field_on_site_uuid_values')
    status                      = request.json.get('status')
    num_chrono                  = request.json.get('num_chrono')
    indice                      = request.json.get('indice')
    assignee_user_id            = request.json.get('assignee_user_id')
    
    
    _site=getByIdOrByName(obj=Site, id=site_id, tenant_id=None )
    
    _type_intervention=getByIdOrByName(TypeIntervention, type_intervention_id)
    
    if place is not None:
        _place = Place.query.filter(Place.place_on_site_uuid == place["place_on_site_uuid"]).first()
    
    # je n'ai trouvé ni avec place_id, ni avec place_on_site_uuid, je dois en creer une 
    current_app.logger.info("place en input")
    current_app.logger.info(place)
    
    if _place is None:
        _place = Place(
            place_on_site_uuid = place["place_on_site_uuid"],
            name = place["name"],
            site_id = _site.id,
            place_json = place["place_json"]
        )
        db.session.add(_place)
        current_app.logger.info("create place")
        current_app.logger.info(_place)
    else:
        _place.site_id = _site.id
        _place.name = place["name"]
        _place.place_json = place["place_json"]
        current_app.logger.info("update place")
        current_app.logger.info(_place)
    
    db.session.commit()  
    
    if num_chrono == "[numchrono]":
        num_chrono = None
        
    if num_chrono=="[NNNNN]":         
        # je vais chercher le max hashtag des interventionValues pour type d'intervention et pour un site donné (ainsi, ce compteur sera effectué par Site ...)
        _interventionValueMax = db.session.query(InterventionValues).filter(InterventionValues.site_id==_site.id).filter(InterventionValues.type_intervention_id==_type_intervention.id).order_by(desc(InterventionValues.num_chrono)).first()
        if _interventionValueMax is None:
            num_chrono=1
        else:
            num_chrono=_interventionValueMax.num_chrono
            if num_chrono is None:
                num_chrono=1
            else:
                num_chrono = num_chrono+1
        indice="A"
    
    #else:
    #    num_chrono = None
        
   
    interventionValues= InterventionValues.query.filter(InterventionValues.intervention_values_on_site_uuid == intervention_values_on_site_uuid).first()
    if interventionValues is None:
        # je vais chercher le max hashtag des interventionValues pour type d'intervention et pour un site donné (ainsi, ce compteur sera effectué par Site ...)
        _interventionValueMax = db.session.query(InterventionValues).filter(InterventionValues.site_id==_site.id).filter(InterventionValues.type_intervention_id==_type_intervention.id).order_by(desc(InterventionValues.hashtag)).first()
        if _interventionValueMax is None:
             max_id=0
        else:
            max_id=_interventionValueMax.hashtag  
        
  
        interventionValues = InterventionValues(
                        intervention_values_on_site_uuid = intervention_values_on_site_uuid,
                        name = intervention_name, 
                        place_id = _place.id,
                        version=1,
                        site_id = _site.id,
                        type_intervention_id = _type_intervention.id,
                        hashtag = max_id + 1,
                        # template_text= template_text        ,
                        status=status,
                        num_chrono=num_chrono,
                        indice=indice,
                        assignee_user_id=assignee_user_id
        )
        
        db.session.add(interventionValues)
        event=Event(object=interventionValues.__class__.__name__, object_id=interventionValues.id, action="create",  description="")
        db.session.add(event)
        
    else:
        # print(intervention.to_json())
        
        interventionValues.place_id = _place.id
        interventionValues.version = interventionValues.version + 1
        interventionValues.site_id = _site.id
        interventionValues.type_intervention_id = _type_intervention.id
        # interventionValues.template_text= template_text
        old_status =  interventionValues.status
        interventionValues.status = status
        
        if num_chrono is not None:
            if interventionValues.num_chrono is None:
                interventionValues.num_chrono=num_chrono
            
        if interventionValues.num_chrono is not None: 
            intervention_name=_place.name+"-"+str(interventionValues.num_chrono).zfill(5)+"-"+indice
        
        interventionValues.name = intervention_name
        interventionValues.indice=indice
        current_app.logger.info("assignee_user_id = %s", assignee_user_id)
        if assignee_user_id is not None:
                _assignee=getByIdOrByName(obj= User, id=assignee_user_id)
                if _assignee is not None:
                    interventionValues.assignee_user_id = _assignee.id
                
        event=Event(object=interventionValues.__class__.__name__, object_id=interventionValues.id, action="update",  description="update {}".format(intervention_name))
        db.session.add(event)
        if old_status != status:
            event=Event(object=interventionValues.__class__.__name__, object_id=interventionValues.id, action="status changed", value_before=old_status, value_after=status, description="update status {}".format(intervention_name))
            db.session.add(event)
            
        
         
    db.session.commit()  

    for k, v in field_on_site_uuid_values.items():
        current_app.logger.info("%s - %s", k, v)
    
        _fieldValue = FieldValue.query.filter(FieldValue.intervention_values_id==interventionValues.id).filter(FieldValue.field_on_site_uuid==k).first()
        
        if _fieldValue is None:
            _field= Field.query.filter(Field.field_on_site_uuid == k).first()
            _fieldValue=FieldValue(
                 intervention_values_id=interventionValues.id,
                 field_on_site_uuid=k,
                 field_id=_field.id,
                 value=v
             )
            db.session.add(_fieldValue)
        else:
            _fieldValue.value = v
        db.session.commit()                
    
            
                
    return jsonify(interventionValues.to_json()), 201


@app_file_intervention.route("/intervention/<id>", methods=["GET"])
@jwt_required()
def get_intervention(id):
    intervention = Intervention.query.get(id)
    if intervention is None:
        abort(make_response(jsonify(error="intervention is not found"), 404))
    return jsonify(intervention.to_json())

@app_file_intervention.route("/intervention/<id>", methods=["DELETE"])
@jwt_required()
def delete_intervention(id):
    intervention = Intervention.query.get(id)
    if intervention is None:
        abort(make_response(jsonify(error="intervention is not found"), 404))
    db.session.delete(intervention)
    db.session.commit()
    return jsonify({'result': True, 'id': id})

@app_file_intervention.route("/intervention_values/hashtag/<site_id>")
@jwt_required()
def get_interventionvalues_siteid(site_id):
    _interventionValueMax = db.session.query(InterventionValues).filter(InterventionValues.site_id==site_id).order_by(desc(InterventionValues.hashtag)).first()
    if _interventionValueMax is None:
         max_id=0
    else:
        max_id=_interventionValueMax.hashtag  
    return jsonify({'max_id': max_id, 'site_id': site_id})


def filterInterventionValues():
    
    query_interventionValues = InterventionValues.query
    
    
    site_id=request.args.get("site_id")
    _site=getByIdOrByName(Site, site_id)
    if _site is None:
        abort(make_response(jsonify(error="site is not found"), 404))
    
    query_interventionValues = query_interventionValues.filter(InterventionValues.site_id == _site.id)
    
    type_intervention_id=request.args.get("type_intervention_id")
    if type_intervention_id is not None:
        _type_intervention=getByIdOrByName(TypeIntervention, type_intervention_id)
        if _type_intervention is None:
            abort(make_response(jsonify(error="_type_intervention is not found"), 404))


        query_interventionValues = query_interventionValues.filter(InterventionValues.type_intervention_id == _type_intervention.id)
    
    
    interventionValues = query_interventionValues.all()
    
    return interventionValues