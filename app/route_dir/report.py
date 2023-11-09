from flask import Blueprint, render_template, session,abort, current_app

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
        abort(404, "report is not found")
    return jsonify(report.to_json())

@app_file_report.route("/report/<id>", methods=["DELETE"])
@jwt_required()
def delete_report(id):
    report = Report.query.get(id)
    if report is None:
        abort(404, "report is not found")
    db.session.delete(report)
    db.session.commit()
    return jsonify({'result': True, 'id': id})
