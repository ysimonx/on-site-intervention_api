from flask import Blueprint, render_template, session,abort, make_response
from ..model_dir.site import Site
from ..model_dir.mymixin         import User, Role
from ..model_dir.tenant import Tenant
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



@app_file_site.route("/site/<id>", methods=["DELETE"])
@jwt_required() 
def del_site(id):
    
    print(g.current_user)
    # TO DO
    # je dois trouver les sites pour lesquels j'ai des roles ...
    _site = Site.query.get(id)
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