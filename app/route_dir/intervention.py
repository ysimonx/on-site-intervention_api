from flask import Blueprint, abort, make_response, current_app

import hashlib

from ..model_dir.intervention import Intervention, InterventionValues
from ..model_dir.type_intervention import TypeIntervention, TypeInterventionSite
from ..model_dir.section import Section
from ..model_dir.form import Form

from ..model_dir.place import Place
from ..model_dir.site import Site
from ..model_dir.form import Form
from ..model_dir.field import Field, FieldValue
from ..model_dir.field_histo import FieldHisto
from flask import jsonify, request, abort
from flask_jwt_extended import jwt_required

from .. import db, getByIdOrByName
app_file_intervention= Blueprint('intervention',__name__)

import json
from sqlalchemy import func, desc

@app_file_intervention.route("/intervention", methods=["GET"])
def get_interventions():
    if not 'site_id' in request.args:
        interventions = Intervention.query.all()
    else:
        _site=getByIdOrByName(Site, request.args.get("site_id"))
        if _site is None:
            abort(make_response(jsonify(error="site is not found"), 404))
        
        interventions = Intervention.query.filter(Intervention.site_id==_site.id).all()
        
    return jsonify([item.to_json() for item in interventions])


@app_file_intervention.route('/intervention_old', methods=['POST'])
@jwt_required()
def create_intervention():
    
    if not request.json:
        abort(make_response(jsonify(error="no json provided in request"), 400))


    intervention_on_site_uuid   = request.json.get('intervention_on_site_uuid')
    intervention_name           = request.json.get('intervention_name')
    place_on_site_uuid          = request.json.get('place_on_site_uuid')
    place_name                  = request.json.get('place_name')
    site_id             = request.json.get('site_id')
    type_intervention           = request.json.get('type_intervention')
    forms                       = request.json.get('forms')
   
    if site_id is None:
        abort(make_response(jsonify(error="site_id must be provided"), 400))
      

    _type_intervention=getByIdOrByName(TypeIntervention, type_intervention)
    if _type_intervention is None:
        _type_intervention = TypeIntervention(name=type_intervention)
        db.session.add(_type_intervention)
        db.session.commit() 
        
    place = Place.query.filter(Place.place_on_site_uuid == place_on_site_uuid).first()
    if place is None:
        place = Place(place_on_site_uuid = place_on_site_uuid, name = place_name )
        db.session.add(place)
        db.session.commit()  
        
    _site=getByIdOrByName(Site, site_id)
    if _site is None:
        abort(make_response(jsonify(error="site is not found"), 400))
        
   
        
    intervention= Intervention.query.filter(Intervention.intervention_on_site_uuid == intervention_on_site_uuid).first()
    if intervention is None:
        intervention = Intervention(
                        intervention_on_site_uuid = intervention_on_site_uuid,
                        name = intervention_name, 
                        site_id = _site.id, 
                        place_id = place.id,
                        version=1,
                        type_intervention_id = _type_intervention.id)
        
        db.session.add(intervention)
    else:
        # print(intervention.to_json())
        intervention.name = intervention_name
        intervention.place_id = place.id
        intervention.version = intervention.version + 1
        intervention.type_intervention_id = _type_intervention.id
        
        
    db.session.commit()  
    
                            
    
     
    # re read intervention, for forms 
    intervention= Intervention.query.filter(Intervention.intervention_on_site_uuid == intervention_on_site_uuid).first()
            
    return jsonify(intervention.to_json()), 201





@app_file_intervention.route("/intervention_values", methods=["GET"])
@jwt_required()
def get_intervention_values():
    
    query_interventionValues = InterventionValues.query
    
    if  'site_id' in request.args:
        
        site_id=request.args.get("site_id")
        _site=getByIdOrByName(Site, site_id)
        if _site is None:
            abort(make_response(jsonify(error="site is not found"), 400))
        query_interventionValues = query_interventionValues.filter(InterventionValues.site_id == _site.id)

    if  'type_intervention_id' in request.args:
        
        type_intervention_id=request.args.get("type_intervention_id")
        _type_intervention=getByIdOrByName(TypeIntervention, type_intervention_id)
        
        if _type_intervention is None:
            abort(make_response(jsonify(error="_type_intervention is not found"), 400))
        query_interventionValues = query_interventionValues.filter(InterventionValues.type_intervention_id == _type_intervention.id)


    interventionValues = query_interventionValues.all()

    return jsonify([item.to_json() for item in interventionValues])


@app_file_intervention.route("/intervention_values/photos", methods=["GET"])
@jwt_required()
def get_intervention_values_photos():
    
    query_interventionValues = InterventionValues.query
    
    if  'site_id' in request.args:
        
        site_id=request.args.get("site_id")
        _site=getByIdOrByName(Site, site_id)
        if _site is None:
            abort(make_response(jsonify(error="site is not found"), 400))
        query_interventionValues = query_interventionValues.filter(InterventionValues.site_id == _site.id)

    if  'type_intervention_id' in request.args:
        
        type_intervention_id=request.args.get("type_intervention_id")
        _type_intervention=getByIdOrByName(TypeIntervention, type_intervention_id)
        
        if _type_intervention is None:
            abort(make_response(jsonify(error="_type_intervention is not found"), 400))
        query_interventionValues = query_interventionValues.filter(InterventionValues.type_intervention_id == _type_intervention.id)

    

    interventionValues = query_interventionValues.all()

    
    
    # else:
        # _site=getByIdOrByName(Site, request.args.get("site_id"))
        # if _site is None:
        #     abort(make_response(jsonify(error="site is not found"), 404))
        # 
        # interventions = Intervention.query.filter(Intervention.site_id==_site.id).all()
        
    return jsonify([item.photos_to_json() for item in interventionValues])


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
    else:
        # print(intervention.to_json())
        interventionValues.name = intervention_name
        interventionValues.place_id = _place.id
        interventionValues.version = interventionValues.version + 1
        interventionValues.site_id = _site.id
        interventionValues.type_intervention_id = _type_intervention.id
        interventionValues.template_text= template_text
        interventionValues.status = status
        interventionValues.num_chrono=num_chrono,
        interventionValues.indice=indice,
        interventionValues.assignee_user_id = assignee_user_id
        
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
