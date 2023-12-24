from flask import Blueprint, abort, make_response

import hashlib

from ..model_dir.intervention import Intervention
from ..model_dir.place import Place
from ..model_dir.organization import Organization
from ..model_dir.form import Form
from ..model_dir.field import Field
from ..model_dir.field_histo import FieldHisto
from flask import jsonify, request, abort
from flask_jwt_extended import jwt_required

from .. import db, getByIdOrByName
app_file_intervention= Blueprint('intervention',__name__)

import json


@app_file_intervention.route("/intervention", methods=["GET"])
def get_interventions():
    interventions = Intervention.query.all()
    return jsonify([item.to_json() for item in interventions])


@app_file_intervention.route('/intervention', methods=['POST'])
@jwt_required()
def create_intervention():
    
    if not request.json:
        abort(make_response(jsonify(error="no json provided in request"), 400))


    intervention_on_site_uuid   = request.json.get('intervention_on_site_uuid')
    intervention_name           = request.json.get('intervention_name')
    place_on_site_uuid          = request.json.get('place_on_site_uuid')
    place_name                  = request.json.get('place_name')
    organization_id             = request.json.get('organization_id')
    
    if organization_id is None:
        abort(make_response(jsonify(error="organization_id must be provided"), 400))
        
    place = Place.query.filter(Place.place_on_site_uuid == place_on_site_uuid).first()
    if place is None:
        place = Place(place_on_site_uuid = place_on_site_uuid, name = place_name )
        db.session.add(place)
        db.session.commit()  
        
    _organisation=getByIdOrByName(Organization, organization_id)
    if _organisation is None:
        abort(make_response(jsonify(error="organization is not found"), 400))
        
    intervention= Intervention.query.filter(Intervention.intervention_on_site_uuid == intervention_on_site_uuid).first()
    if intervention is None:
        intervention = Intervention(
                        intervention_on_site_uuid = intervention_on_site_uuid,
                        name = intervention_name, 
                        organization_id = _organisation.id, 
                        place_id = place.id)
        db.session.add(intervention)
        

    db.session.commit()  
    return jsonify(intervention.to_json()), 201


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
