from flask import Blueprint, render_template, session,abort, make_response, current_app
from ..model_dir.site import Site
from ..model_dir.mymixin         import User, Role
from ..model_dir.tenant import Tenant
from ..model_dir.intervention import InterventionValues, Intervention
from ..model_dir.place import Place
from ..model_dir.company import Company


from ..model_dir.field import FieldValue, Field
from ..model_dir.form import Form
from ..model_dir.section import Section

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
    
    # TO DO
    # je dois trouver les sites pour lesquels j'ai des roles ...
    sites = Site.query.all()
    return jsonify([item.to_json() for item in sites])


@app_file_site.route("/site/<id>", methods=["GET"])
@jwt_required() 
def get_site(id):
    
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
    
    _site.dict_of_lists = json.dumps(dict_of_lists)
    db.session.commit()
    
    return jsonify(_site.to_json()),200


@app_file_site.route("/site/<site_id>/custom_fields", methods=["POST"])
@jwt_required() 
def post_site_custom_fields(site_id):
    
    _site = Site.query.get(site_id)
    if _site is None:
        abort(make_response(jsonify(error="site not found"), 404))

    dict_of_custom_fields = request.json.get('dict_of_custom_fields', None)
    if dict_of_custom_fields is None:
        abort(make_response(jsonify(error="missing dict_of_custom_fields parameter"), 400))
    
    type_intervention = request.json.get('type_intervention', None)
    if type_intervention is None:
        abort(make_response(jsonify(error="missing type_intervention parameter"), 400))
    
    formulaire_json = request.json.get('formulaire', None)
    if formulaire_json is None:
        abort(make_response(jsonify(error="missing formulaire parameter"), 400))
    
    _form = Form.query.filter(Form.form_on_site_uuid == formulaire_json["form_on_site_uuid"]).first()
    if _form is None:
        abort(make_response(jsonify(error="formulaire not found"), 400))
    
    
    _type_intervention=getByIdOrByName(obj=TypeIntervention, id=type_intervention)
    if _type_intervention is None:
        abort(make_response(jsonify(error="type_intervention not found"), 400))
        
    
    _type_intervention_site = TypeInterventionSite.query.get((_type_intervention.id,_site.id))
    if _type_intervention_site is None:
        abort(make_response(jsonify(error="_type_intervention_site not found"), 400)) 
        
    result={ "forms":{ } }
    if _type_intervention_site.dict_of_custom_fields is not None:
        try:
            result=json.loads(_type_intervention_site.dict_of_custom_fields)
        except:
            current_app.logger.info("_type_intervention_site.dict_of_custom_fields FAILS !")
            # result={}
    else:
        current_app.logger.info("_type_intervention_site.dict_of_custom_fields is None")
    
    if "forms" in result:
        jsonforms=result["forms"]
    else:
        jsonforms={}
    
    jsonCustomFields={ "form_name": _form.form_name, "custom_fields" : dict_of_custom_fields }
    current_app.logger.info(jsonCustomFields)
    jsonforms[_form.form_on_site_uuid]=jsonCustomFields
    result["forms"]=jsonforms
    
    _type_intervention_site.dict_of_custom_fields=json.dumps(result)
    db.session.commit()
    current_app.logger.info("_type_intervention_site updated")
       
    return jsonify(_type_intervention_site.to_json()),201



@app_file_site.route("/site/<site_id>/lists_for_places", methods=["POST"])
@jwt_required() 
def post_site_lists_for_places(site_id):
    
    _site = Site.query.get(site_id)
    if _site is None:
        abort(make_response(jsonify(error="site not found"), 404))

    dict_of_lists_for_places = request.json.get('dict_of_lists_for_places', None)
    if dict_of_lists_for_places is None:
        abort(make_response(jsonify(error="missing dict_of_lists_for_places parameter"), 400))
    
    _site.dict_of_lists_for_places = json.dumps(dict_of_lists_for_places)
    db.session.commit()
    
    
    return jsonify(_site.to_json()),201



@app_file_site.route("/site/<site_id>/user", methods=["POST"])
@jwt_required() 
def post_site_user(site_id):
    
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

    user_firstname = request.json.get('user_firstname', None)
    user_lastname = request.json.get('user_lastname', None)
    user_phone =  request.json.get('user_phone', None)
    user_company = request.json.get('user_company', None)
    
            
        
    roles = request.json.get('roles', None)
    if roles is None:
                abort(make_response(jsonify(error="missing roles parameter"), 400))
                
    _company=None
    if user_company is not None:
        current_app.logger.info("user company given %s", user_company)
        _company=getByIdOrByName(obj=Company, id=user_company, tenant_id=None)
        current_app.logger.info(_company)
        if _company is None:
            _company=Company(
                name=user_company,
                tenant_id=None)
            db.session.add(_company)
            db.session.commit()
        
    _user = getByIdOrEmail(obj=User, id=user_email)
    if _user is None:
        _user = User(
                    email= user_email,
                    firstname=user_firstname,
                    lastname=user_lastname,
                    phone=user_phone,
                    password= "12345678",
                    tenant_id = None
                    
                )
        if _company is not None:
            _user.company_id = _company.id
            
        _user.hash_password()
        db.session.add(_user)  
        db.session.commit()
        current_app.logger.info("user added %s", _user.email)
    else:
        if user_firstname is not None and user_firstname != "":
            
            _user.firstname = user_firstname
        if user_lastname is not None  and user_lastname != "":
            _user.lastname  = user_lastname
        if user_phone is not None  and user_phone != "":
            _user.phone  = user_phone
        if user_company is not None  and user_company != "":
            _user.company_id = _company.id
        db.session.commit()
        
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
    return jsonify(_site.to_json()),201


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
    
    # TO DO
    # je dois trouver les sites pour lesquels j'ai des roles ...
    _site = Site.query.get(site_id)
    if _site is None:
        abort(make_response(jsonify(error="site not found"), 404))

    types_interventions_site = TypeInterventionSite.query.filter(TypeInterventionSite.site_id == _site.id).all()
    current_app.logger.info(types_interventions_site)
    for _type_intervention_site in types_interventions_site:
        db.session.delete(_type_intervention_site)
    
    roles = Role.query.filter(Role.site_id == _site.id).all()
    current_app.logger.info(roles)
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
    return jsonify({"result": "ok", "id":site_id}),200


@app_file_site.route('/site/templates/update', methods=['POST'])
@jwt_required()
def update_all_sites_templates():

    sites = Site.query.all()
    for _site in sites:
         process_sites_interventions_templates(_site)
    return jsonify({"result": "ok"}),200    
         
    
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
    
    process_sites_interventions_templates(_site)
                
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
        
        
    # j'ajoute tous les roles "admin" et "site administrator" par defaut au _user (moi)
    
    roles=["admin", "site administrator"]
    for rolename in roles:
        _role = getByIdOrByName(
                                obj=Role, 
                                id=rolename, 
                                tenant_id=_tenant.id, 
                                site_id=_site.id
                            )
        if _role is None:
                                _role = Role(
                                    name=rolename, 
                                    tenant_id=_tenant.id,
                                    site_id=_site.id
                                )
                                db.session.add(_role)
                                db.session.commit() 
                                
        _user.roles.append(_role)
        

    db.session.commit() 
     
    return jsonify(_site.to_json()), 201
    # return jsonify({"message":"ok"}), 201
    
    
    
def process_sites_interventions_templates(_site):
    
    # _roles = Role.query.filter(Role.site_id == _site.id).all()
    
    roles = config["roles"]
    for role_name in roles:
        current_app.logger.info(role_name)
        _role = Role.query.filter(Role.site_id == _site.id).filter(Role.name == role_name).first()
        if _role is None:
            _role=Role(site_id=_site.id, name=role_name)
            db.session.add(_role)
            current_app.logger.info("role {} added".format(role_name))
    db.session.commit()
        
        
    _types_intervention = config["types_interventions"]
    for type_intervention_name, item in _types_intervention.items():
        current_app.logger.info(type_intervention_name)
        _type_intervention=getByIdOrByName(obj=TypeIntervention, id=type_intervention_name)
        if _type_intervention is not None:
            current_app.logger.info(_type_intervention.to_json())
        
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

            update_sites_interventions_templates(_site, _type_intervention, item);
            
                    
    
def update_sites_interventions_templates( _site,  _type_intervention, template ):
      
    intervention_on_site_uuid = template["intervention_on_site_uuid"]
    intervention_name = template["type_intervention"]
    forms = template["forms"]
          
    intervention= Intervention.query.filter(Intervention.intervention_on_site_uuid == intervention_on_site_uuid).first()
    if intervention is None:
        intervention = Intervention(
                        intervention_on_site_uuid = intervention_on_site_uuid,
                        name = intervention_name, 
                        type_intervention_id = _type_intervention.id)
        
        db.session.add(intervention)
    else:
        # print(intervention.to_json())
        intervention.name = intervention_name
        intervention.type_intervention_id = _type_intervention.id
        
        
    db.session.commit()  
    
    if forms is not None:
        for key_form in  forms.keys():
            form_values =forms[key_form]
            form_name = form_values["form_name"]
            form_on_site_uuid = form_values["form_on_site_uuid"]
            _form= Form.query.filter(Form.form_on_site_uuid == form_on_site_uuid).first()
            if _form is None:
                _form=Form( 
                       intervention_id = intervention.id,
                       name=intervention_on_site_uuid+"_form_"+form_name,
                       form_name= form_name, 
                       form_on_site_uuid=form_on_site_uuid,
                       form_order= int(key_form))
                db.session.add(_form)
                # db.session.commit()
            
            current_app.logger.info("------------------")
            
            sections=form_values["sections"]
            if sections is not None:
                for key_sections in sections.keys():
                    current_app.logger.info("Section #%s", key_sections)
                    
                    section_values=sections[key_sections]
                    section_on_site_uuid = section_values['section_on_site_uuid']
                    section_name=section_values['section_name']
                    section_type=section_values['section_type']
                    
                    _section= Section.query.filter(Section.section_on_site_uuid == section_on_site_uuid).first()
                    if _section is None:
                        _section=Section(
                            form_id=_form.id,
                            intervention_id = intervention.id,
                            section_on_site_uuid=section_on_site_uuid,
                            section_name=section_name,
                            section_type=section_type,
                            section_order_in_form=int(key_sections)
                        )
                        db.session.add(_section)
                        # db.session.commit()
                    else:
                            _section.section_name=section_name,
                            
                    
                    
                    fields=section_values["fields"]
                    if fields is not None:
                        for key_field in fields.keys():
                            current_app.logger.info("Field #%s", key_field)
                            field_attributes=fields[key_field]
                            
                            current_app.logger.info(field_attributes)
                            field_on_site_uuid = field_attributes['field_on_site_uuid']
                            field_name         = field_attributes['field_name']
                            field_type         = field_attributes['field_type']
                            field_order_in_section=int(key_field)
                            
                            _field= Field.query.filter(Field.field_on_site_uuid == field_on_site_uuid).first()
                            if _field is None:
                                _field=Field(
                                    section_id=_section.id,
                                    intervention_id = intervention.id,
                                    field_on_site_uuid=field_on_site_uuid,
                                    field_name=field_name,
                                    field_type=field_type,
                                    field_order_in_section=int(key_field)
                                )
                                db.session.add(_field)
                            else:
                                current_app.logger.info("update !")
                                _field.field_type=field_type
                                _field.field_name=field_name
                                db.session.add(_field)
    db.session.commit()                
   