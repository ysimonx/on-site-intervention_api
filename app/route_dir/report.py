from flask import Blueprint, render_template, session,abort, current_app, make_response

import uuid
import numpy
import os
from config import config

from ..model_dir.intervention import Intervention
from ..model_dir.report import Report
from flask import jsonify, request, abort, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from .. import db,  getByIdOrByName, getByIdOrFilename
app_file_report= Blueprint('report',__name__)

import cv2



@app_file_report.route("/report", methods=["GET"])
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
    db.session.delete(report)
    db.session.commit()
    return jsonify({'result': True, 'id': id})



@app_file_report.route('/report', methods=['POST'])
@jwt_required()
def create_report():
    report_on_site_uuid = request.json.get("report_on_site_uuid", None)
    if report_on_site_uuid is None:
        abort(make_response(jsonify(error="missing report_on_site_uuid parameter"), 400))
        
    report = Report.query.filter(Report.report_on_site_uuid == report_on_site_uuid).first()
    if report is not None:
        abort(make_response(jsonify(error="report_on_site_uuid already created"), 400))
    
    report_data          = request.json.get("report_data", None)
    report_data_md5      = request.json.get("report_data_md5", None)
    average_latitude    = request.json.get("average_latitude", None)
    average_longitude   = request.json.get("average_longitude", None)
    intervention_on_site_uuid= request.json.get("intervention_on_site_uuid", None)
    report = Report(
        report_on_site_uuid=report_on_site_uuid,
        intervention_on_site_uuid=intervention_on_site_uuid,
        report_data=report_data,
        report_data_md5=report_data_md5,
        average_latitude=average_latitude,
        average_longitude=average_longitude
        )
    
    db.session.add(report)
    db.session.commit()
    return jsonify({ "message":"ok"}), 201
