from flask import Blueprint, render_template, session,abort, current_app, make_response

import uuid
import hashlib
import numpy
import os
from config import config

from ..model_dir.type_intervention import TypeIntervention
from flask import jsonify, request, abort, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from .. import db,  getByIdOrByName, getByIdOrFilename
app_file_type_intervention= Blueprint('type_intervention',__name__)

import cv2
import json


@app_file_type_intervention.route("/type_intervention", methods=["GET"])
def get_type_intervention():
    types_interventions = TypeIntervention.query.all()
    return jsonify([item.to_json() for item in types_interventions])


@app_file_type_intervention.route('/type_intervention', methods=['POST'])
@jwt_required()
def create_type_intervention():
    if not request.json:
        abort(make_response(jsonify(error="missing json parameters"), 400))
    
    name = request.json.get('name')
    if name is None:
        abort(make_response(jsonify(error="missing name parameter"), 400))
     
    type_intervention = TypeIntervention(
        name=name
    )

    db.session.add(type_intervention)
    db.session.commit()
    return jsonify(type_intervention.to_json()), 201

@app_file_type_intervention.route("/type_intervention/<id>", methods=["GET"])
@jwt_required()
def get_type_intervention(id):
    type_intervention = TypeIntervention.query.get(id)
    if type_intervention is None:
        abort(make_response(jsonify(error="type_intervention is not found"), 400))

    return jsonify(type_intervention.to_json())

@app_file_type_intervention.route("/intervention/<id>", methods=["DELETE"])
@jwt_required()
def delete_type_intervention(id):
    type_intervention = TypeIntervention.query.get(id)
    if type_intervention is None:
        abort(make_response(jsonify(error="type_intervention is not found"), 400))
    db.session.delete(type_intervention)
    db.session.commit()
    return jsonify({'result': True, 'id': id})
