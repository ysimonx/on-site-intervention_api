from flask import Blueprint, render_template, session,abort, current_app, make_response


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
from ..thingsboard.connector_thingsboard import Thingsboard

from .. import db,  getByIdOrByName, getByIdOrFilename
app_file_field= Blueprint('field',__name__)

tb=Thingsboard()


@app_file_field.route("/field", methods=["GET"])
def get_fields():
    fields = Field.query.all()
    return jsonify([item.to_json() for item in fields])


@app_file_field.route("/field/<id>", methods=["GET"])
@jwt_required()
def get_field(id):
    field = Field.query.get(id)
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


@app_file_field.route('/field', methods=['POST'])
@jwt_required()
def create_field():
    field_on_site_uuid = request.json.get("field_on_site_uuid", None)
    if field_on_site_uuid is None:
        abort(make_response(jsonify(error="missing field_on_site_uuid parameter"), 400))
        
    field = Field.query.filter(Field.field_on_site_uuid == field_on_site_uuid).first()
    if field is not None:
        abort(make_response(jsonify(error="field_on_site_uuid already created"), 400))
        
    field_name          = request.json.get("name", None)
    field_data          = request.json.get("field_data", None)
    field_data_md5      = request.json.get("field_data_md5", None)
    report_on_site_uuid = request.json.get("report_on_site_uuid", None)
    report_id           = request.json.get("report_id",None)
    average_latitude    = request.json.get("average_latitude", None)
    average_longitude   = request.json.get("average_longitude", None)
    
    field = Field(
        name=field_name,
        field_on_site_uuid=request.json.get('field_on_site_uuid'),
        report_id=report_id,
        field_data=field_data,
        field_data_md5=field_data_md5,
        report_on_site_uuid=report_on_site_uuid,
        average_latitude=average_latitude,
        average_longitude=average_longitude
    )
    
    db.session.add(field)
    
    tb_photos=[]
    photos_on_site_uuid = request.json.get("photos_on_site_uuid", None)
    if photos_on_site_uuid is not None:
        
        for photo_on_site_uuid in photos_on_site_uuid:
            print(photo_on_site_uuid)
            photo = Photo.query.filter(Photo.photo_on_site_uuid == photo_on_site_uuid).first()
            if photo is not None:
                print("photo found !")    
                tb_photos.append(photo)    
            else:
                print("photo not found !")
    
    db.session.commit()
   
    tb.createAsset(instance=field)
    
    # link des photos si besoin
    for photo in tb_photos:
        tb.linkAssets(instanceFrom=field, instanceTo=photo)
        
    return jsonify({ "message":"ok"}), 201


