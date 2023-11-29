from flask import Blueprint, render_template, session,abort, make_response
from ..model_dir.company import Company
from ..model_dir.user import User
from flask import jsonify, request, abort
from .. import db, getByIdOrEmail, getByIdOrByName
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

app_file_company = Blueprint('company',__name__)


@app_file_company.route("/company", methods=["GET"])
@jwt_required()
def get_company_list():
    _user = User.me()
    items = Company.query.filter(Company.tenant_id == _user.get_internal()["tenant_id"]).all()
    return jsonify([item.to_json() for item in items])


@app_file_company.route('/company', methods=['POST'])
def create_company():
    if not request.json:
        abort(make_response(jsonify(error="no json provided in request"), 400))

    company_name = request.json.get('name', None)
    if company_name is None:
        abort(make_response(jsonify(error="missing company_name parameter"), 400))
    
    tenant_id = request.json.get("tenant_id", None)
    if tenant_id is None:
        abort(make_response(jsonify(error="error login tenant_id missing in request"), 401))
    
    _tenant = getByIdOrByName(obj=Tenant, id=tenant_id, tenant_id=None)
    
        
    company = Company(
        name=company_name,
        tenant_id=_tenant.id
    )

    db.session.add(company)
    db.session.commit()
    return jsonify(company.to_json()), 201