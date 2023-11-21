from flask import Blueprint, abort, make_response


from ..model_dir.report_template import ReportTemplate
from flask import jsonify, abort
from flask_jwt_extended import jwt_required

from .. import db
app_file_report_template= Blueprint('report_template',__name__)




@app_file_report_template.route("/report_template", methods=["GET"])
def get_report_templates():
    report_templatex = ReportTemplate.query.all()
    return jsonify([item.to_json() for item in report_templatex])


@app_file_report_template.route('/report_template', methods=['POST'])
@jwt_required()
def create_report_template():
    return jsonify({ "message":"ok"}), 201
    


@app_file_report_template.route("/report_template/<id>", methods=["GET"])
@jwt_required()
def get_report_template(id):
    report_template = ReportTemplate.query.get(id)
    if report_template is None:
        abort(make_response(jsonify(error="report_template is not found"), 404))
    return jsonify(report_template.to_json())

@app_file_report_template.route("/report_template/<id>", methods=["DELETE"])
@jwt_required()
def delete_report_template(id):
    report_template = ReportTemplate.query.get(id)
    if report_template is None:
       abort(make_response(jsonify(error="report_template is not found"), 404))
    db.session.delete(report_template)
    db.session.commit()
    return jsonify({'result': True, 'id': id})
