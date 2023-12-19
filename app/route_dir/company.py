from flask import Blueprint, render_template, session,abort, make_response
from ..model_dir.company import Company
from ..model_dir.mymixin import User
from flask import jsonify, request, abort
from .. import db, getByIdOrEmail, getByIdOrByName
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

app_file_company = Blueprint('company',__name__)


@app_file_company.route("/company", methods=["GET"])
@jwt_required()
def get_company_list():
    items=Company.my_query().all()
    return jsonify([item.to_json() for item in items])

    
@app_file_company.route('/company', methods=['POST'])
@jwt_required()
def create_company():
    if not request.json:
        abort(make_response(jsonify(error="no json provided in request"), 400))

    company_name = request.json.get('name', None)
    if company_name is None:
        abort(make_response(jsonify(error="missing company_name parameter"), 400))
    
    _user = User.me()
        
    company = getByIdOrByName(obj=Company, id=company_name, tenant_id=_user.get_internal()["tenant_id"])
    if company is not None:
            abort(make_response(jsonify(error="company already exists"), 400))
     
    
    
    company = Company(
        name=company_name,
        tenant_id=_user.get_internal()["tenant_id"]
    )

    db.session.add(company)
    db.session.commit()
    return jsonify(company.to_json()), 201