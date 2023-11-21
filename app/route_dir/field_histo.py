from flask import Blueprint, render_template, session,abort, current_app, make_response

import uuid
import numpy
import os
import hashlib
import json

from config import config

from ..model_dir.field_histo import FieldHisto
from ..model_dir.form import Form
from flask import jsonify, request, abort, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from .. import db,  getByIdOrByName, getByIdOrFilename
app_file_field_histo= Blueprint('field_histo',__name__)

import cv2

# curl -H "Content-Type: application/json" -X POST -d '{"name": "ysimonx"}' http://localhost:5000/user
@app_file_field_histo.route('/field_histo', methods=['POST'])
def create_field_histo():
    if not request.json:
        abort(make_response(jsonify(error="missing json body"), 400))


    field_uuid=request.json.get("field_uuid")
    intervention_uuid=request.json.get("intervention_uuid")
    field_name=request.json.get("field_name")
    field_json=request.json.get("field_json")
    md5 = hashlib.md5(json.dumps(field_json).encode('utf-8')).hexdigest()
            
    field_histo=FieldHisto(field_uuid = field_uuid, 
                           intervention_uuid=intervention_uuid,
                            name=field_name, 
                            field_data=json.dumps(field_json), 
                            field_data_md5=md5)

    db.session.add(field_histo)
    db.session.commit()
    return jsonify(field_histo.to_json()), 201

@app_file_field_histo.route("/field_histo", methods=["GET"])
def get_fields_histo():
    fields_histo = FieldHisto.query.all()
    return jsonify([item.to_json() for item in fields_histo])


@app_file_field_histo.route("/field_histo/<id>", methods=["GET"])
@jwt_required()
def get_field_histo(id):
    field_histo = FieldHisto.query.get(id)
    if field_histo is None:
        abort(make_response(jsonify(error="field_histo is not found"), 404))
    return jsonify(field_histo.to_json())

@app_file_field_histo.route("/field_histo/<id>", methods=["DELETE"])
@jwt_required()
def delete_field(id):
    field_histo = FieldHisto.query.get(id)
    if field_histo is None:
        abort(make_response(jsonify(error="field_histo is not found"), 404))
    db.session.delete(field_histo)
    db.session.commit()
    return jsonify({'result': True, 'id': id})
