from flask import Blueprint, abort, make_response


from ..model_dir.form_template import FormTemplate
from flask import jsonify, abort
from flask_jwt_extended import jwt_required

from .. import db
app_file_form_template= Blueprint('form_template',__name__)




@app_file_form_template.route("/form_template", methods=["GET"])
def get_form_templates():
    form_templatex = FormTemplate.query.all()
    return jsonify([item.to_json() for item in form_templatex])


@app_file_form_template.route('/form_template', methods=['POST'])
@jwt_required()
def create_form_template():
    return jsonify({ "message":"ok"}), 201
    


@app_file_form_template.route("/form_template/<id>", methods=["GET"])
@jwt_required()
def get_form_template(id):
    form_template = FormTemplate.query.get(id)
    if form_template is None:
        abort(make_response(jsonify(error="form_template is not found"), 404))
    return jsonify(form_template.to_json())

@app_file_form_template.route("/form_template/<id>", methods=["DELETE"])
@jwt_required()
def delete_form_template(id):
    form_template = FormTemplate.query.get(id)
    if form_template is None:
       abort(make_response(jsonify(error="form_template is not found"), 404))
    db.session.delete(form_template)
    db.session.commit()
    return jsonify({'result': True, 'id': id})
