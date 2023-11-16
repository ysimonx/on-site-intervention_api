from flask import Blueprint, render_template, session,abort, current_app, make_response

import uuid
import hashlib
import numpy
import os
from config import config

from ..model_dir.type_field import TypeField
from flask import jsonify, request, abort, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from .. import db,  getByIdOrByName, getByIdOrFilename
app_file_type_field= Blueprint('type_intervention',__name__)

import cv2
import json


@app_file_type_field.route("/type_field", methods=["GET"])
def get_type_field():
    types_interventions = TypeField.query.all()
    return jsonify([item.to_json() for item in types_interventions])


@app_file_type_field.route('/type_field', methods=['POST'])
@jwt_required()
def create_type_field():
    if not request.json:
        abort(make_response(jsonify(error="missing json parameters"), 400))
    
    name = request.json.get('name')
    if name is None:
        abort(make_response(jsonify(error="missing name parameter"), 400))
     
    type_field = TypeField(
        name=name
    )

    db.session.add(type_field)
    db.session.commit()
    return jsonify(type_field.to_json()), 201

@app_file_type_field.route("/type_field/<id>", methods=["GET"])
@jwt_required()
def get_type_field(id):
    type_field = TypeField.query.get(id)
    if type_field is None:
        abort(make_response(jsonify(error="type_field is not found"), 400))

    return jsonify(type_field.to_json())

@app_file_type_field.route("/type_field/<id>", methods=["DELETE"])
@jwt_required()
def delete_type_intervention(id):
    type_field = TypeField.query.get(id)
    if type_field is None:
        abort(make_response(jsonify(error="type_field is not found"), 400))
    db.session.delete(type_field)
    db.session.commit()
    return jsonify({'result': True, 'id': id})
