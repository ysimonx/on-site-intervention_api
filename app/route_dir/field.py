from flask import Blueprint, render_template, session,abort, current_app

import uuid
import numpy
import os
from config import config

from ..model_dir.field import Field
from ..model_dir.report import Report
from flask import jsonify, request, abort, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from .. import db,  getByIdOrByName, getByIdOrFilename
app_file_field= Blueprint('field',__name__)

import cv2



@app_file_field.route("/field", methods=["GET"])
def get_fields():
    fields = Field.query.all()
    return jsonify([item.to_json() for item in fields])


@app_file_field.route("/field/<id>", methods=["GET"])
@jwt_required()
def get_field(id):
    field = Field.query.get(id)
    if field is None:
        abort(404, "field is not found")
    return jsonify(field.to_json())

@app_file_field.route("/field/<id>", methods=["DELETE"])
@jwt_required()
def delete_field(id):
    field = Field.query.get(id)
    if field is None:
        abort(404, "field is not found")
    db.session.delete(field)
    db.session.commit()
    return jsonify({'result': True, 'id': id})


@app_file_field.route('/field', methods=['POST'])
@jwt_required()
def create_field():
    field_on_site_uuid = request.json.get("field_on_site_uuid", None)
    if field_on_site_uuid is None:
        abort(400, "miss field_on_site_uuid parameter")
        
    field = Field.query.filter(Field.field_on_site_uuid == field_on_site_uuid).first()
    if field is not None:
        abort(400, "miss field_on_site_uuid already created")
    
    field_data          = request.json.get("field_data", None)
    field_data_md5      = request.json.get("field_data_md5", None)
    report_on_site_uuid = request.json.get("field_data_md5", None)
    report_id           = request.json.get("report_id",None)
    average_latitude    = request.json.get("average_latitude", None)
    average_longitude   = request.json.get("average_longitude", None)
    
    field = Field(
        field_on_site_uuid=request.json.get('field_on_site_uuid'),
        report_id=report_id,
        field_data=field_data,
        field_data_md5=field_data_md5,
        report_on_site_uuid=report_on_site_uuid,
        average_latitude=average_latitude,
        average_longitude=average_longitude
        )
    
    db.session.add(field)
    db.session.commit()
    return jsonify({ "message":"ok"}), 201


