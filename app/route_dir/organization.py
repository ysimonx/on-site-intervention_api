from flask import Blueprint, render_template, session,abort, make_response
from ..model_dir.organization import Organization
from flask import jsonify, request, abort
from .. import db, getByIdOrEmail, getByIdOrByName
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

app_file_organization = Blueprint('organization',__name__)


@app_file_organization.route("/organization", methods=["GET"])
def get_organization_list():
    items = Organization.query.all()
    return jsonify([item.to_json() for item in items])


@app_file_organization.route('/organization', methods=['POST'])
def create_user():
    if not request.json:
        abort(make_response(jsonify(error="no json provided in request"), 400))

    organization_name = request.json.get('name', None)
    if organization_name is None:
        abort(make_response(jsonify(error="missing organization_name parameter"), 400))
     
    organization = Organization(
        name=organization_name
    )

    db.session.add(organization)
    db.session.commit()
    return jsonify(organization.to_json()), 201