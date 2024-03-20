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


@app_file_intervention.route("/intervention_values/dict/<id>", methods=["GET"])
@jwt_required()
def get_intervention_values_dict_id(id):
    intervention_values = InterventionValues.query.get(id)
    if intervention_values is None:
        abort(make_response(jsonify(error="intervention_values is not found"), 404))
        
    return intervention_values.to_dict()


@app_file_intervention.route("/intervention_values/csv", methods=["GET"])
def get_intervention_values_csv():
    
    site_id=request.args.get("site_id")
    _site=getByIdOrByName(Site, site_id)
    if _site is None:
         abort(make_response(jsonify(error="site is not found"), 404))
    
    interventionValues = filterInterventionValues()
    
    columns=[]
    data=[]
    for interventionValue in interventionValues:
        dict_columns_data =interventionValue.to_dict()
        columns=dict_columns_data["columns"]
        donnees=dict_columns_data["data"]
        dict_converted={}
        
        for key, value in donnees.items():
            if value is not None and str(value).startswith("<svg"):
                value="yes"
            if value is None:
                value=""
            dict_converted[key]=unidecode(str(value))
            
            
        data.append(dict_converted)

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

    site_id=request.args.get("site_id")
    _site=getByIdOrByName(Site, site_id)
    
    if "maxutc" in request.args:
        _maxutc=request.args.get("maxutc")
        if _site is not None:
            if _site.maxutc is not None:
                current_app.logger.info("avant maxutc {} vs {}".format(_maxutc, _site.maxutc))
                _maxutc = _maxutc.replace("T"," ")
                current_app.logger.info("apres maxutc {} vs {}".format(_maxutc, _site.maxutc))
                if str(_maxutc) == str(_site.maxutc):
                    current_app.logger.info("maxutc should 304 !!!!")
                    return jsonify({"message":"not modified"}), 304
                
    interventionValues = filterInterventionValues()
    
    resp=make_response(jsonify([item.to_json() for item in interventionValues]))
    
    if _site is not None:
        maxutc = getLastModified(interventionValues)
        if maxutc is not None:
            resp.headers['X-LastModified'] = maxutc
        # if _site.maxutc != maxutc:
        #     _site.maxutc = maxutc;
        #     db.session.commit()
        
    return resp


@app_file_intervention.route("/intervention_values/photos", methods=["GET"])
@jwt_required()
def get_intervention_values_photos():
    
    site_id=request.args.get("site_id")
    _site=getByIdOrByName(Site, site_id)
    
    if "maxutc" in request.args:
        _maxutc=request.args.get("maxutc")
        if _site is not None:
            if _site.maxutc is not None:
                current_app.logger.info("avant maxutc {} vs {}".format(_maxutc, _site.maxutc))
                _maxutc = _maxutc.replace("T"," ")
                current_app.logger.info("apres maxutc {} vs {}".format(_maxutc, _site.maxutc))
                if str(_maxutc) == str(_site.maxutc):
                    current_app.logger.info("maxutc should 304 !!!!")
                    return jsonify({"message":"not modified"}), 304
                
                
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
    
    # update du timestamp au niveau du "site" (pour reactualisation via 304)
    maxutc = getLastModified([interventionValues])
    if maxutc is not None:
        _site.maxutc = maxutc;
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

