from flask import Blueprint, render_template, session,abort, current_app, make_response

import uuid
import numpy
import os
from config import config

from ..model_dir.intervention import Intervention
from ..model_dir.field import Field
from ..model_dir.photo import Photo

from ..model_dir.report import Report
from flask import jsonify, request, abort, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity

from .. import db,  getByIdOrByName, getByIdOrFilename

from ..thingsboard.connector_thingsboard import ThingsboardConnector

app_file_report= Blueprint('report',__name__)





@app_file_report.route("/report", methods=["GET"])
@jwt_required()
def get_reports():
    reports = Report.query.all()
    return jsonify([item.to_json() for item in reports])


@app_file_report.route("/report/<id>", methods=["GET"])
@jwt_required()
def get_report(id):
    report = Report.query.get(id)
    if report is None:
        abort(make_response(jsonify(error="report is not found"), 404))
       
    return jsonify(report.to_json())

    
@app_file_report.route("/report/<id>", methods=["DELETE"])
@jwt_required()
def delete_report(id):
    report = Report.query.get(id)
    if report is None:
        abort(make_response(jsonify(error="report is not found"), 404))
        
    array_instance_deleted=[]
    
    for item_field in report.fields:
        for item_photo in item_field.photos:
            photo = Photo.query.get(item_photo.id)
            if photo is not None:
                db.session.delete(photo)
                array_instance_deleted.append(photo)
                current_app.logger.info('photo deleted id = ' + photo.id)
            
        field = Field.query.get(item_field.id)
        if field is not None:
            db.session.delete(field)
            array_instance_deleted.append(field)
            current_app.logger.info('field deleted id = ' + field.id)
    
    db.session.delete(report)
    array_instance_deleted.append(report)
    current_app.logger.info('report deleted id = ' + report.id)
    
    db.session.commit()
    
     # synchro thingsboard
    tb=ThingsboardConnector()
    for instance in array_instance_deleted:
            tb.deleteAsset(instance=instance)
     
    return jsonify({'result': True})




@app_file_report.route('/report', methods=['PUT', 'POST'])
@jwt_required()
def update_report():
    
    # update report
    report_on_site_uuid = request.json.get("report_on_site_uuid", None)
    if report_on_site_uuid is None:
        abort(make_response(jsonify(error="missing report_on_site_uuid parameter"), 400))
        
    report = Report.query.filter(Report.report_on_site_uuid == report_on_site_uuid).first()
    if report is None:
        report_name                 = request.json.get("report_name", None)
        average_latitude            = request.json.get("average_latitude", None)
        average_longitude           = request.json.get("average_longitude", None)
        intervention_on_site_uuid   = request.json.get("intervention_on_site_uuid", None)
        report = Report(
            report_on_site_uuid=report_on_site_uuid,
            report_name=report_name,
            intervention_on_site_uuid=intervention_on_site_uuid,
            average_latitude=average_latitude,
            average_longitude=average_longitude
        )
        db.session.add(report)
        db.session.commit()
    else:
        report.report_name                 = request.json.get("report_name",        report.report_name)
        report.average_latitude            = request.json.get("average_latitude",   report.average_latitude)
        report.average_longitude           = request.json.get("average_longitude",  report.average_longitude)
        report.intervention_on_site_uuid   = request.json.get("intervention_on_site_uuid", report.intervention_on_site_uuid)
        db.session.commit()
    
    arr_children_fields=[]
    dict_children_photos={}
    
    fields = request.json.get("fields", None)
    if (fields is not None):
        for itemfield in fields:
                field = Field.query.filter(Field.field_on_site_uuid == itemfield["field_on_site_uuid"]).first()
                
                if field is None:
                    field = Field(
                        report_id           = report.id,
                        report_on_site_uuid = report.report_on_site_uuid,
                    )
              
                if "field_name" in itemfield:
                    field.field_name          = itemfield["field_name"]
                if "field_on_site_uuid" in itemfield:
                    field.field_on_site_uuid  = itemfield["field_on_site_uuid"]
                if "field_value" in itemfield:
                    field.field_value         = itemfield["field_value"]
                if "field_type" in itemfield:
                    field.field_type          = itemfield["field_type"]
                if "average_latitude" in itemfield:
                    field.average_latitude    = itemfield["average_latitude"]
                if "average_longitude" in itemfield:
                    field.average_longitude   = itemfield["average_longitude"]

                db.session.add(field)
                db.session.commit()
                arr_children_fields.append(field)
                
                if "photos_on_site_uuid" in itemfield:
                    photos_on_site_uuid = itemfield["photos_on_site_uuid"]
                    
                    arr_photos_linked=[]
                    for photo_on_site_uuid in photos_on_site_uuid:
                        
                        photo = Photo.query.filter(Photo.photo_on_site_uuid == photo_on_site_uuid).first()
                        if photo is not None:
                            
                            # update de la clé étrangère photo->field et annule et écrasement de photo.field_on_site_uuid
                            photo.field_id=field.id 
                            photo.field_on_site_uuid=field.field_on_site_uuid
                            db.session.commit()
                            # ajoute dans un tableau des photos pour remonter thingsboard
                            arr_photos_linked.append(photo) 
                            
                    dict_children_photos[field.id]=arr_photos_linked
                     
    
    
    # synchro thingsboard
    tb=ThingsboardConnector()
    asset = tb.syncAsset(instance=report)
    for field in arr_children_fields:
            tb.syncAsset(instance=field)
            tb.linkAssets(instanceFrom=report, instanceTo=field)
            dict_photos=dict_children_photos[field.id]
            for photo in dict_photos:
                tb.linkAssets(instanceFrom=field, instanceTo=photo)
                tb.saveAttribute(instance=photo, dict_attributes={"field_id": field.id})
              
    return jsonify({ "message":"ok"}), 200

"""
@app_file_report.route('/report', methods=['POST'])
@jwt_required()
def create_report():
    
    # creation report
    report_on_site_uuid = request.json.get("report_on_site_uuid", None)
    if report_on_site_uuid is None:
        abort(make_response(jsonify(error="missing report_on_site_uuid parameter"), 400))
        
    report = Report.query.filter(Report.report_on_site_uuid == report_on_site_uuid).first()
    if report is not None:
        abort(make_response(jsonify(error="report_on_site_uuid already created"), 400))
    
    report_name                 = request.json.get("report_name", None)
    average_latitude            = request.json.get("average_latitude", None)
    average_longitude           = request.json.get("average_longitude", None)
    intervention_on_site_uuid   = request.json.get("intervention_on_site_uuid", None)
    report = Report(
        report_on_site_uuid=report_on_site_uuid,
        report_name=report_name,
        intervention_on_site_uuid=intervention_on_site_uuid,
        average_latitude=average_latitude,
        average_longitude=average_longitude
    )
    db.session.add(report)
    db.session.commit()
    
    # fields management 
    arr_fields_created=[]
    dict_photos_for_field={}
    
    fields = request.json.get("fields", None)
    if (fields is not None):
        for item in fields:
                
                field = Field(
                    report_id           = report.id,
                    report_on_site_uuid = report.report_on_site_uuid,
                    
                    field_name          = item["field_name"],
                    field_on_site_uuid  = item["field_on_site_uuid"],
                    field_value         = item["field_value"],
                    field_type          = item["field_type"],
                    average_latitude    = item["average_latitude"],
                    average_longitude   = item["average_longitude"]
                )
                db.session.add(field)
                db.session.commit()
                
                arr_photos_linked=[]
                if "photos_on_site_uuid" in item:
                    photos_on_site_uuid = item["photos_on_site_uuid"]
                    
                    for photo_on_site_uuid in photos_on_site_uuid:
                        photo = Photo.query.filter(Photo.photo_on_site_uuid == photo_on_site_uuid).first()
                        if photo is not None:
                            
                            # update de la clé étrangère photo->field et annule et écrasement de photo.field_on_site_uuid
                            photo.field_id=field.id 
                            photo.field_on_site_uuid=field.field_on_site_uuid
                            db.session.commit()
                
                            # ajoute dans un tableau des photos pour remonter thingsboard
                            arr_photos_linked.append(photo) 
                            
                    dict_photos_for_field[field.id]=arr_photos_linked
                                
                
                arr_fields_created.append(field)
    
    # resultat ici : 
    # - - - - - - - - 
    # report : contient l'instance report de classe Report
    #   --> arr_fields_created : contient la liste des instances Field créés pour ce report
    #          --> dict_photos_for_field : contient la liste des instances Photo deja uploadées pour chacun de ces fields            
 
    # synchro thingsboard
    tb=ThingsboardConnector()
    tb.syncAsset(instance=report)
    for field in arr_fields_created:
            tb.syncAsset(instance=field)
            tb.linkAssets(instanceFrom=report, instanceTo=field)
            dict_photos=dict_photos_for_field[field.id]
            for photo in dict_photos:
                tb.linkAssets(instanceFrom=field, instanceTo=photo)
                tb.saveAttribute(instance=photo, dict_attributes={"field_id": field.id})
    
    return jsonify({ "message":"ok"}), 201
"""