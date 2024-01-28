from flask import Blueprint, render_template, session,abort, make_response, current_app
from ..model_dir.mymixin import User, Role
from ..model_dir.company import Company
from ..model_dir.tenant import Tenant
from ..model_dir.organization import Organization
from ..model_dir.type_intervention import TypeIntervention, TypeInterventionOrganization

from flask import jsonify, request, abort
from .. import db, getByIdOrEmail, getByIdOrByName
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    create_refresh_token,
    get_jwt_identity, set_access_cookies, get_csrf_token
)
import json

app_file_user = Blueprint('user',__name__)


# cf : https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/
# https://flask-jwt-extended.readthedocs.io/en/stable/api/?highlight=get_jwt_identity#verify-tokens-in-request
# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
#
# exemple
# {
#    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4Njc3MTQ1MCwianRpIjoiYmY2MDZhNTctMjk2Mi00MGJjLWFkYjctODgzMTY3Yjg2NWNkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjJlYWNjYjY1LTY2YWYtNGQ3Yi05NGYyLTJjMmY5OGFhMWVkMSIsIm5iZiI6MTY4Njc3MTQ1MCwiZXhwIjoxNjg2Nzc1MDUwfQ.l5ZJRqJDakFEcvlA0hiKfmXzBrjoQnR60_GesVC4DGs",
#    "result_check": true
#}


@app_file_user.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    tenant_id = request.json.get("tenant_id", None)
    
    if tenant_id is None:
        abort(make_response(jsonify(error="error login tenant_id missing in request"), 401))
        
        
    _tenant = getByIdOrByName(obj=Tenant, id=tenant_id, tenant_id=None)
    
    user = getByIdOrEmail(obj=User,  id=email)
    
    if user is None:
        abort(make_response(jsonify(error="error login"), 401))
    
    if user.active == False:    
        abort(make_response(jsonify(error="account desactivated"), 401))
    
    result_check = user.check_password(password)
    if not result_check:
        abort(make_response(jsonify(error="error password"), 401))
        
    
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    csrf_refresh_token =  get_csrf_token(access_token)
    response =  jsonify(
        access_token=access_token,
        refresh_token=refresh_token, 
        csrf_refresh_token=csrf_refresh_token,
        result_check=result_check,
        roles= [item.name for item in user.roles] 
    )
    
    # cf https://flask-jwt-extended.readthedocs.io/en/stable/token_locations.html
    set_access_cookies(response, access_token)

    return response

@app_file_user.route("/user", methods=["GET"])
@jwt_required()
def get_user_list():
    items = User.query.all()
    return jsonify([item.to_json() for item in items])

@app_file_user.route("/user/active", methods=["GET"])
@jwt_required()
def get_user_active_list():
    items = User.query.filter(User.active == True).all()
    return jsonify([item.to_json() for item in items])




@app_file_user.route("/user/me", methods=["GET"])
@jwt_required()
def get_user_me():
    return (User.me().to_json()), 200


@app_file_user.route("/user/me/config", methods=["GET"])
@jwt_required()
def get_user_config():
    
    # qui je suis
    me = User.me().to_json()
    
    # detail des organizations qui me concernent
    user_organizations=[]
    organizations = Organization.query.all()
    for organization in organizations:
        if organization.name in me["organizations_roles"].keys():
           user_organizations.append(organization)
    
    
    dict_types_interventions_organizations={}
       
    _types_interventions_organizations = TypeInterventionOrganization.query.all()
    for _type_intervention_organization in _types_interventions_organizations:
        if _type_intervention_organization.organization.name in me["organizations_roles"].keys():
            if _type_intervention_organization.organization.name in dict_types_interventions_organizations.keys():
                content = dict_types_interventions_organizations[_type_intervention_organization.organization.name]
            else:
                content={}
            content[_type_intervention_organization.type_intervention.name]=json.loads(_type_intervention_organization.template_text)
            dict_types_interventions_organizations[_type_intervention_organization.organization.name]=content
            # current_app.logger.info(_type_intervention_organization.organization.name)
            # current_app.logger.info(_type_intervention_organization.type_intervention.name)
    
    r = json.dumps(dict_types_interventions_organizations)   
    result={
            "user": me,
            "organizations": [{"organization" : user_organization.to_json()} for user_organization in user_organizations],
            "config_organization_type_intervention": dict_types_interventions_organizations
            }
    
    return (result), 200




# curl -H "Content-Type: application/json" -X POST -d '{"name": "ysimonx"}' http://localhost:5000/user
@app_file_user.route('/user', methods=['POST'])
def create_user():
    if not request.json:
        abort(make_response(jsonify(error="missing json body"), 400))
        
    if not 'email' in request.json:
        abort(make_response(jsonify(error="missing email parameter"), 400))
    
    if not 'password' in request.json:
        abort(make_response(jsonify(error="missing password parameter"), 400))
    
    tenant = getByIdOrByName(obj=Tenant, id=request.json.get('tenant_id'))
    if tenant is None:
        abort(make_response(jsonify(error="tenant is not found"), 400))
  

    company = getByIdOrByName(obj=Company, id=request.json.get('company'), tenant_id=tenant.id)
    if company is None:
        company = Company(
            name=request.json.get('company'),
            tenant_id=tenant.id
        )
        db.session.add(company)
        db.session.commit()
       
    user = getByIdOrEmail(obj=User, id=request.json.get('email'))
    if user is not None:
        user.phone = request.json.get('phone')
        user.tenant_id = None, # user must not be associated to a specific tenant
        user.password = request.json.get('password')
        user.hash_password()   
    else:
        user = User(
            email=          request.json.get('email'),
            password =      request.json.get('password'),
            company_id =    company.id,
            tenant_id = None, # user must not be associated to a specific tenant
            phone =         request.json.get('phone')
            )

        user.hash_password()
        db.session.add(user)
    
    db.session.commit()
    return jsonify(user.to_json()), 201

       


@app_file_user.route('/token/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    print(user.active)
    if user.active == True:
        ret = {
            'access_token': create_access_token(identity=current_user)
        }
    
        return jsonify(ret), 200
    
    abort(make_response(jsonify(error="account desactivated"), 401))