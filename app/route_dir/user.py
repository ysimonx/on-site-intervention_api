from flask import g, Blueprint, render_template, session,abort, make_response, current_app
from ..model_dir.mymixin import User, Role
from ..model_dir.company import Company
from ..model_dir.tenant import Tenant
from ..model_dir.site import Site
from ..model_dir.type_intervention import TypeIntervention, TypeInterventionSite
from config import config, Config
from flask_mail import Mail, Message


import random
import string


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
    current_app.logger.info("login attempt for %s", email)
    user = getByIdOrEmail(obj=User,  id=email)
    
    if user is None:
        abort(make_response(jsonify(error="error login"), 401))
    
    if user.active == False:    
        abort(make_response(jsonify(error="account desactivated"), 401))
    
    result_check = user.check_password(password)
    if not result_check:
        if user.new_password is None:
            abort(make_response(jsonify(error="error password"), 401))
        else:
            result_check = user.check_new_password(password)
            if result_check:
                user.password = user.new_password
                user.new_password = None
                db.session.add(user)
                db.session.commit()
            else:
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


@app_file_user.route('/user/reset_password', methods=['POST'])
def reset_password():
    if not request.json:
        abort(make_response(jsonify(error="missing json body"), 400))
        
    if not 'email' in request.json:
        abort(make_response(jsonify(error="missing email parameter"), 400))
  
    attempt_email = request.json.get('email')
    
    current_app.logger.info("reset_password attempt for %s", attempt_email)
    _user = getByIdOrEmail(obj=User, id=attempt_email)
    if _user is None:
          abort(make_response(jsonify(error="error"), 400))
    
    # get random password pf length 8 with letters, digits, and symbols
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(20))

    current_app.logger.info("password is >%s<", password)
    _user.new_password=password
    _user.hash_new_password()
    db.session.add(_user)  
    db.session.commit()
                        
    
    msg = Message(subject='Password reset required',
                  sender= Config.MAIL_FROM,
                  recipients=[_user.email],
                  charset='utf-8')
    
    text = "here is your new password : %s" % password
    msg.body = text.encode('utf-8')
    with current_app.app_context():
        mail = Mail()
        mail.send(msg)
    
    return jsonify({"message":"password changed and email sent"}),200
    

@app_file_user.route("/user/me", methods=["GET"])
@jwt_required()
def get_user_me():
    return (User.me().to_json()), 200


@app_file_user.route("/user/me/config", methods=["GET"])
@jwt_required()
def get_user_config():
    
    # qui je suis
    if g.current_user is None:
         abort(make_response(jsonify(error="g.current_user is none"), 400))
         
         
    me = g.current_user.to_json()
    #
    my_tenants=g.current_user.tenants_administrator
    
 
    # detail des sites qui me concernent
    dict_my_sites={}
    
    json_user_sites=[]
    sites = Site.query.all()
    for site in sites:
        json_site = site.to_json()
        tenant_id = site.tenant_id
        if tenant_id is not None:
            _tenant=getByIdOrByName(obj=Tenant, id=tenant_id)
            json_site["tenant"]=_tenant.to_json_light()
        if site.id in me["sites_roles"].keys(): # ceux pour lesquels j'ai un role
           json_user_sites.append(json_site)
           dict_my_sites[site.id]=json_site
        else:
            if _tenant is not None:
                if _tenant.admin_tenant_user_id==g.current_user.id:
                    # ceux pour lesquels je suis admin du Tenant
                    json_user_sites.append(json_site)
                    dict_my_sites[site.id]=json_site
    
    _types_intervention = config["types_interventions"]
       
      
    result={
            "user": me,
            "site_member_of": [{"site" : item} for item in json_user_sites],
            "tenant_administrator_of" : [{"tenant": item.to_json_light()} for item in my_tenants] ,
            "config_types_intervention": _types_intervention
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
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if user is None:
        msg = ("user %s is none on refresh token, should not happen" % current_user_id)
        current_app.logger.info(msg)
        abort(make_response(jsonify(error=msg), 401))
            
    current_app.logger.info("user %s can be refresh token", user.email)
    
    if user.active == True:
        ret = {
            'access_token': create_access_token(identity=current_user_id)
        }
    
        return jsonify(ret), 200
    
    abort(make_response(jsonify(error="account desactivated"), 401))