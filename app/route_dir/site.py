from flask import Blueprint, render_template, session,abort, make_response, current_app
from ..model_dir.site import Site
from ..model_dir.mymixin         import User, Role
from ..model_dir.tenant import Tenant
from ..model_dir.intervention import InterventionValues
from ..model_dir.place import Place

from ..model_dir.field import FieldValue

from ..model_dir.type_intervention import TypeIntervention, TypeInterventionSite
import json

from flask import jsonify, request, abort, g
from .. import db, getByIdOrEmail, getByIdOrByName

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

from config import config

app_file_site = Blueprint('site',__name__)


@app_file_site.route("/site", methods=["GET"])
@jwt_required() 
def get_site_list():
    
    print(g.current_user)
    # TO DO
    # je dois trouver les sites pour lesquels j'ai des roles ...
    items = Site.query.all()
    return jsonify([item.to_json() for item in items])


@app_file_site.route("/site/<id>", methods=["GET"])
@jwt_required() 
def get_site(id):
    
    print(g.current_user)
    _site = Site.query.get(id)
    if _site is None:
        abort(make_response(jsonify(error="site not found"), 404))

    json_site = _site.to_json()

    tenant_id = _site.tenant_id
    if tenant_id is not None:
        _tenant=getByIdOrByName(obj=Tenant, id=tenant_id)
        json_site["tenant"]=_tenant.to_json_light()
        
    return jsonify(json_site),200


@app_file_site.route("/site/<site_id>/lists", methods=["POST"])
@jwt_required() 
def post_site_lists(site_id):
    
    _site = Site.query.get(site_id)
    if _site is None:
        abort(make_response(jsonify(error="site not found"), 404))

    dict_of_lists = request.json.get('dict_of_lists', None)
    if dict_of_lists is None:
        abort(make_response(jsonify(error="missing dict_of_lists parameter"), 400))
    
    print(dict_of_lists)
    _site.dict_of_lists = json.dumps(dict_of_lists)
    db.session.commit()
    
    return jsonify(_site.to_json()),200


@app_file_site.route("/site/<site_id>/user", methods=["POST"])
@jwt_required() 
def post_site_user(site_id):
    
    print(g.current_user)
    _site = Site.query.get(site_id)
    if _site is None:
        abort(make_response(jsonify(error="site not found"), 404))

    tenant_id = _site.tenant_id
    if tenant_id is not None:
        _tenant=getByIdOrByName(obj=Tenant, id=tenant_id)
    
    if not request.json:
        abort(make_response(jsonify(error="no json provided in request"), 400))

    user_email = request.json.get('user_email', None)
    if user_email is None:
        abort(make_response(jsonify(error="missing user_email parameter"), 400))


    roles = request.json.get('roles', None)
    if roles is None:
                abort(make_response(jsonify(error="missing roles parameter"), 400))
                
     
    _user = getByIdOrEmail(obj=User, id=user_email)
    if _user is None:
        _user = User(
                    email= user_email,
                    password= "12345678",
                    tenant_id = None
                )
        _user.hash_password()
        db.session.add(_user)  
        db.session.commit()
        current_app.logger.info("user added %s", _user.email)
    
    # je créé tous les roles nécessaires et supprime tous les roles attribués à ce user pour ce site 
    for role in _site.roles:
        current_app.logger.info("role %s",role.name)
        _role = getByIdOrByName(
            obj=Role, 
            id=role.name, 
            tenant_id=_tenant.id, 
            site_id=_site.id
        )
        if _role is not None:
            current_app.logger.info("role exists %s", _role.name)
        else:
            _role = Role(
                name=role_name, 
                tenant_id=_tenant.id,
                site_id=_site.id
            )
            db.session.add(_role)
            current_app.logger.info("role added %s", _role.name)
            db.session.commit()
                            
                            
        result = db.session.execute('delete from users_roles where role_id= :val and user_id= :val2', {'val': _role.id, 'val2':_user.id})
        current_app.logger.info("delete role '%s' for site '%s' for user '%s'", _role.name, _site.name, _user.email)

    for role_name in roles:
        current_app.logger.info("role %s",role_name)
        _role = getByIdOrByName(
            obj=Role, 
            id=role_name, 
            tenant_id=_tenant.id, 
            site_id=_site.id
        )
        _user.roles.append(_role)
        db.session.commit()
        
    db.session.commit()
    return jsonify(_site.to_json()),200


@app_file_site.route("/site/<site_id>/user", methods=["DELETE"])
@jwt_required() 
def rm_site_user(site_id):
    
    print(g.current_user)
    _site = Site.query.get(site_id)
    if _site is None:
        abort(make_response(jsonify(error="site not found"), 404))

    tenant_id = _site.tenant_id
    if tenant_id is not None:
        _tenant=getByIdOrByName(obj=Tenant, id=tenant_id)

    if not request.json:
        abort(make_response(jsonify(error="no json provided in request"), 400))

    user_email = request.json.get('user_email', None)
    if user_email is None:
        abort(make_response(jsonify(error="missing user_email parameter"), 400))
            
     
    _user = getByIdOrEmail(obj=User, id=user_email)
    if _user is None:
        abort(make_response(jsonify(error="this user_email is not found"), 400))

    
    for role in _site.roles:
        current_app.logger.info("role %s",role.name)
        _role = getByIdOrByName(
            obj=Role, 
            id=role.name, 
            tenant_id=_tenant.id, 
            site_id=_site.id
        )
        if _role is not None:
            result = db.session.execute('delete from users_roles where role_id= :val and user_id= :val2', {'val': _role.id, 'val2':_user.id})
            current_app.logger.info("delete role '%s' for site '%s' for user '%s'", _role.name, _site.name, _user.email)

    db.session.commit()
    return jsonify(_site.to_json()),200



@app_file_site.route("/site/<site_id>", methods=["DELETE"])
@jwt_required() 
def del_site(site_id):
    
    print(g.current_user)
    # TO DO
    # je dois trouver les sites pour lesquels j'ai des roles ...
    _site = Site.query.get(site_id)
    if _site is None:
        abort(make_response(jsonify(error="site not found"), 404))

    types_interventions_site = TypeInterventionSite.query.filter(TypeInterventionSite.site_id == _site.id).all()
    print(types_interventions_site)
    for _type_intervention_site in types_interventions_site:
        db.session.delete(_type_intervention_site)
    
    roles = Role.query.filter(Role.site_id == _site.id).all()
    print(roles)
    for _role in roles:
        # do : delete from users_roles where role_id=_role.id
        result = db.session.execute('delete from users_roles where role_id= :val', {'val': _role.id})
        
        # puis enfin
        db.session.delete(_role)
    
    intervention_values = InterventionValues.query.filter(InterventionValues.site_id == _site.id).all()
    for _intervention_values in intervention_values:
        field_values = FieldValue.query.filter(FieldValue.intervention_values_id==_intervention_values.id).all()
        for _field_values in field_values:
            db.session.delete(_field_values)
        db.session.delete(_intervention_values)
    
    places = Place.query.filter(Place.site_id == _site.id).all()
    for place in places:
        db.session.delete(place)
    
        
    db.session.delete(_site)
    db.session.commit()
    return jsonify({'result': True, 'id': id}),200




@app_file_site.route('/site', methods=['POST'])
@jwt_required()
def create_site():
    if not request.json:
        abort(make_response(jsonify(error="no json provided in request"), 400))

    site_name = request.json.get('site_name', None)
    if site_name is None:
        abort(make_response(jsonify(error="missing site_name parameter"), 400))

    tenant_id = request.json.get('tenant_id', None)
    if site_name is None:
        abort(make_response(jsonify(error="missing tenant_id parameter"), 400))

    _tenant=getByIdOrByName(obj=Tenant, id=tenant_id)
    if _tenant is None:
        abort(make_response(jsonify(error="this tenant is unknown"), 400))
        
    _user = User.me()
    # _user = g._current_user
    if len(_user.tenants_administrator) < 1:
        abort(make_response(jsonify(error="you're not a Tenant administrator"), 400))
    
    if (_user.tenants_administrator[0].id != _tenant.id):
         abort(make_response(jsonify(error="you're not this Tenant administrator"), 400))
         
    _site=getByIdOrByName(obj=Site, id=site_name, tenant_id = _tenant.id)
    if _site is None:
        _site = Site(
            name=site_name,
            tenant_id = _tenant.id
        )
        db.session.add(_site)
        db.session.commit()
    
    _types_intervention = config["types_interventions"]
    for type_intervention_name, item in _types_intervention.items():
        print(type_intervention_name)
        _type_intervention=getByIdOrByName(obj=TypeIntervention, id=type_intervention_name)
        if _type_intervention is not None:
            print(_type_intervention.to_json())
        
            _type_intervention_site = TypeInterventionSite.query.get((_type_intervention.id,_site.id))
            if _type_intervention_site is None:
                
                _type_intervention_site = TypeInterventionSite(
                    type_intervention_id=_type_intervention.id,
                    site_id=_site.id,
                    template_text=json.dumps(item)
                )
                db.session.add(_type_intervention_site)
            else:
                _type_intervention_site.template_text=json.dumps(item)
                db.session.commit()
    
    
    # j'ajoute tous les roles par defaut    
    for role_name in config["roles"]:
        _role = getByIdOrByName(
                            obj=Role, 
                            id=role_name, 
                            tenant_id=_tenant.id, 
                            site_id=_site.id
                        )
        if _role is None:
                            _role = Role(
                                name=role_name, 
                                tenant_id=_tenant.id,
                                site_id=_site.id
                            )
                            db.session.add(_role)
                            db.session.commit() 
        
        
    # j'ajoute tous le role "admin" par defaut au _user (moi)
    
    _role = getByIdOrByName(
                            obj=Role, 
                            id="admin", 
                            tenant_id=_tenant.id, 
                            site_id=_site.id
                        )
    if _role is None:
                            _role = Role(
                                name="admin", 
                                tenant_id=_tenant.id,
                                site_id=_site.id
                            )
                            db.session.add(_role)
                            db.session.commit() 
    _user.roles.append(_role)
    

    db.session.commit() 
     
    return jsonify(_site.to_json()), 201
    # return jsonify({"message":"ok"}), 201