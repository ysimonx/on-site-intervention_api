from flask import Blueprint, render_template, session,abort, current_app, make_response

import json
import jsonpickle
import uuid
import numpy
import os
from config import config

from ..model_dir.photo import Photo
from ..model_dir.field import Field
from ..model_dir.report import Report
from flask import jsonify, request, abort, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from ..thingsboard.connector_thingsboard import ThingsboardConnector

from .. import db,  getByIdOrByName, getByIdOrFilename
app_file_field= Blueprint('field',__name__)

from sqlalchemy import inspect

tb=ThingsboardConnector()


@app_file_field.route("/field", methods=["GET"])
@jwt_required()
def get_fields():
    fields = Field.query.all()
    return jsonify([item.to_json() for item in fields])


@app_file_field.route("/field/<id>", methods=["GET"])
@jwt_required()
def get_field(id):
    field = Field.query.get(id)
    print(field.reports)
    if field is None:
        abort(make_response(jsonify(error="field is not found"), 404))
    return jsonify(field.to_json())

@app_file_field.route("/field/<id>", methods=["DELETE"])
@jwt_required()
def delete_field(id):
    field = Field.query.get(id)
    if field is None:
        abort(make_response(jsonify(error="field is not found"), 404))
    db.session.delete(field)
    db.session.commit()
    return jsonify({'result': True, 'id': id})


#   {
#    "field_on_site_uuid": "field_on_site_uuid_value_with_photo_14",
#    "field_data": "{\"hauteur\": 100}",
#    "field_data_md5": "field_data_md5_value",
#    "report_on_site_uuid": "report_on_site_uuid_value",
#    "average_latitude": 0.1,
#    "average_longitude": 0.2,
#    "photos_on_site_uuid": [
#        "photo_on_site_uuid_valueb"
#    ]
#   }


#   {
#    "field_on_site_uuid": "field_on_site_uuid_value_with_photo_14",
#    "field_name": "hauteur"
#    "field_value": "100"
#    "field_type": "double/string/json/boolean"
#    "report_on_site_uuid": "report_on_site_uuid_value",
#    "average_latitude": 0.1,
#    "average_longitude": 0.2,
#    "photos_on_site_uuid": [
#        "photo_on_site_uuid_valueb"
#    ]
#   }


@app_file_field.route('/field', methods=['POST'])
@jwt_required()
def create_field():
    field_on_site_uuid = request.json.get("field_on_site_uuid", None)
    if field_on_site_uuid is None:
        abort(make_response(jsonify(error="missing field_on_site_uuid parameter"), 400))
        
    field = Field.query.filter(Field.field_on_site_uuid == field_on_site_uuid).first()
    if field is not None:
        abort(make_response(jsonify(error="field_on_site_uuid already created"), 400))
        
    field_name          = request.json.get("field_name", None)
    field_value         = request.json.get("field_value", None)
    field_type          = request.json.get("field_type", None)
    report_on_site_uuid = request.json.get("report_on_site_uuid", None)
    report_id           = request.json.get("report_id",None)
    average_latitude    = request.json.get("average_latitude", None)
    average_longitude   = request.json.get("average_longitude", None)
    
    field = Field(
        field_name=field_name,
        field_on_site_uuid=request.json.get('field_on_site_uuid'),
        report_id=report_id,
        field_value=field_value,
        field_type=field_type,
        report_on_site_uuid=report_on_site_uuid,
        average_latitude=average_latitude,
        average_longitude=average_longitude
    )

    db.session.add(field)
    db.session.commit()
    
 
    arr_thingsboard_photos=[]
    photos_on_site_uuid = request.json.get("photos_on_site_uuid", None)
    if photos_on_site_uuid is not None:
        for photo_on_site_uuid in photos_on_site_uuid:
            photo = Photo.query.filter(Photo.photo_on_site_uuid == photo_on_site_uuid).first()
            if photo is not None:
                
                # update de la clé étrangère photo->field et annule et écrasement de photo.field_on_site_uuid
                photo.field_id=field.id 
                photo.field_on_site_uuid=field.field_on_site_uuid
                db.session.commit()
                
                # ajoute dans un tableau des photos pour remonter thingsboard
                arr_thingsboard_photos.append(photo)    
                current_app.logger.debug('photo found while creating field with photo_on_site_uuid = ' + photo_on_site_uuid)
            else:
                current_app.logger.error('photo not found while creating field with photo_on_site_uuid = ' + photo_on_site_uuid)      
    db.session.commit()
    
    # update Thingsboard
    tb.createAsset(instance=field)
    for photo in arr_thingsboard_photos:
        tb.linkAssets(instanceFrom=field, instanceTo=photo)
    
    
    current_app.logger.info('field created for field_on_site_uuid=' + field_on_site_uuid)
    return jsonify({ "message":"ok"}), 201


