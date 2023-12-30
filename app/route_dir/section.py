from flask import Blueprint, abort, make_response


from ..model_dir.section import Section
from flask import jsonify, abort
from flask_jwt_extended import jwt_required

from .. import db
app_file_section= Blueprint('section',__name__)




@app_file_section.route("/section", methods=["GET"])
def get_sections():
    sectionx = Section.query.all()
    return jsonify([item.to_json() for item in sectionx])


@app_file_section.route('/section', methods=['POST'])
@jwt_required()
def create_section():
    return jsonify({ "message":"ok"}), 201
    


@app_file_section.route("/section/<id>", methods=["GET"])
@jwt_required()
def get_section(id):
    section = Section.query.get(id)
    if section is None:
        abort(make_response(jsonify(error="section is not found"), 404))
    return jsonify(section.to_json())

@app_file_section.route("/section/<id>", methods=["DELETE"])
@jwt_required()
def delete_section(id):
    section = Section.query.get(id)
    if section is None:
       abort(make_response(jsonify(error="section is not found"), 404))
    db.session.delete(section)
    db.session.commit()
    return jsonify({'result': True, 'id': id})
