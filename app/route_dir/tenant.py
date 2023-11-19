from flask import Blueprint, render_template, session,abort, make_response
from ..model_dir.tenant import Tenant
from flask import jsonify, request, abort
from .. import db, getByIdOrEmail, getByIdOrByName
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

app_file_tenant = Blueprint('tenant',__name__)


@app_file_tenant.route("/tenant", methods=["GET"])
def get_tenant_list():
    items = Tenant.query.all()
    return jsonify([item.to_json() for item in items])


@app_file_tenant.route('/tenant', methods=['POST'])
def create_user():
    if not request.json:
        abort(make_response(jsonify(error="no json provided in request"), 400))

    tenant_name = request.json.get('name', None)
    if tenant_name is None:
        abort(make_response(jsonify(error="missing tenant_name parameter"), 400))
     
    tenant = Tenant(
        name=tenant_name
    )

    db.session.add(tenant)
    db.session.commit()
    return jsonify(tenant.to_json()), 201