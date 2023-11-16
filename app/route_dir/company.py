from flask import Blueprint, render_template, session,abort, make_response
from ..model_dir.company import Company
from flask import jsonify, request, abort
from .. import db, getByIdOrEmail, getByIdOrByName
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

app_file_company = Blueprint('company',__name__)


@app_file_company.route("/company", methods=["GET"])
def get_company_list():
    items = Company.query.all()
    return jsonify([item.to_json() for item in items])


@app_file_company.route('/company', methods=['POST'])
def create_user():
    if not request.json:
        abort(make_response(jsonify(error="no json provided in request"), 400))

    company_name = request.json.get('name', None)
    if company_name is None:
        abort(make_response(jsonify(error="missing company_name parameter"), 400))
     
    company = Company(
        name=company_name
    )

    db.session.add(company)
    db.session.commit()
    return jsonify(company.to_json()), 201