from flask import Blueprint, render_template, session,abort, make_response
from ..model_dir.organization import Organization
from ..model_dir.user import User
from ..model_dir.tenant import Tenant

from flask import jsonify, request, abort
from .. import db, getByIdOrEmail, getByIdOrByName

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

app_file_organization = Blueprint('organization',__name__)


@app_file_organization.route("/organization", methods=["GET"])
@jwt_required() 
def get_organization_list():
    _user = User.me()
    items = Organization.query.filter(Organization.tenant_id == _user.get_internal()["tenant_id"]).all()
    return jsonify([item.to_json() for item in items])


@app_file_organization.route('/organization', methods=['POST'])
@jwt_required()
def create_organization():
    if not request.json:
        abort(make_response(jsonify(error="no json provided in request"), 400))

    organization_name = request.json.get('name', None)
    if organization_name is None:
        abort(make_response(jsonify(error="missing organization_name parameter"), 400))

    _user = User.me()
     
    organization = Organization(
        name=organization_name,
        tenant_id = _user.get_internal()["tenant_id"]
    )

    db.session.add(organization)
    db.session.commit()
    return jsonify(organization.to_json()), 201