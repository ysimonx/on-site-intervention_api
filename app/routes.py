import os
import logging
import datetime
import json
import uuid
from flask                      import jsonify, abort, render_template, g, request
from flask_mail                 import Mail
from flask_jwt_extended         import JWTManager, get_jwt_identity, verify_jwt_in_request
from config import config

from .                          import create_app
from .                          import db, getByIdOrEmail, getByIdOrByName

from app.model_dir.mymixin        import User, Role
from app.model_dir.company      import Company
from app.model_dir.tenant       import Tenant
from app.model_dir.site import Site
from app.model_dir.type_field   import TypeField
from app.model_dir.place        import Place
from app.model_dir.intervention import Intervention
from app.model_dir.section      import Section
from app.model_dir.field        import Field
from app.model_dir.form         import Form



from app.model_dir.type_intervention   import TypeIntervention, TypeInterventionSite

from .route_dir.tenant          import app_file_tenant
from .route_dir.site    import app_file_site
from .route_dir.event           import app_file_event
from .route_dir.notification    import app_file_notification
from .route_dir.user            import app_file_user
from .route_dir.company         import app_file_company

from .route_dir.photo           import app_file_photo
from .route_dir.file            import app_file_file
from .route_dir.intervention    import app_file_intervention
from .route_dir.type_intervention import app_file_type_intervention
from .route_dir.place           import app_file_place
from .route_dir.form          import app_file_form
from .route_dir.form_template import app_file_form_template
from .route_dir.field           import app_file_field
from .route_dir.field_histo     import app_file_field_histo
from .route_dir.backoffice      import app_file_backoffice
from .route_dir.role            import app_file_role
from .route_dir.section         import app_file_section



app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.config['DEBUG'] = True

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"]           = "super-secret"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] =  datetime.timedelta(seconds=3600)          # 1 heure
app.config["JWT_TOKEN_LOCATION"]        = ["headers", "cookies"]                    # le token "access_token" est envoyé en header ou en cookie
app.config["JWT_COOKIE_SECURE"]         = False                                     # should be True in production (need https)
app.config["JWT_CSRF_IN_COOKIES"]       = False                                     # do not send "csrf_access_token" by set-cookies
app.config["JWT_CSRF_METHODS"]          = [ "GET","POST", "PUT", "PATCH", "DELETE"] # need this CSRF method when client is web app, 
app.config["JWT_COOKIE_SAMESITE"]       = "Lax"


jwt = JWTManager(app)

# Setup upload folder
UPLOAD_FOLDER = 'static'
app.config['MAX_CONTENT_LENGTH']        = 16 * 1000 * 1000
app.config['UPLOAD_FOLDER']             = UPLOAD_FOLDER

# Setup Mail
app.config['MAIL_SERVER']               = 'smtp.example.com'
app.config['MAIL_PORT']                 = 465
app.config['MAIL_USE_SSL']              = True
app.config['MAIL_USERNAME']             = 'username'
app.config['MAIL_PASSWORD']             = 'password'
mail = Mail(app)

# Setup Routes
url_prefix = "/api/v1"

app.register_blueprint(app_file_user,
                       url_prefix=url_prefix)
app.register_blueprint(app_file_event,
                       url_prefix=url_prefix)
app.register_blueprint(app_file_notification,
                       url_prefix=url_prefix)
app.register_blueprint(app_file_company,
                       url_prefix=url_prefix)
app.register_blueprint(app_file_photo,
                       url_prefix=url_prefix)
app.register_blueprint(app_file_file,
                       url_prefix=url_prefix)
app.register_blueprint(app_file_place,
                       url_prefix=url_prefix)
app.register_blueprint(app_file_intervention,
                       url_prefix=url_prefix)
app.register_blueprint(app_file_form,
                       url_prefix=url_prefix)
app.register_blueprint(app_file_field,
                       url_prefix=url_prefix)
app.register_blueprint(app_file_field_histo,
                       url_prefix=url_prefix)
app.register_blueprint(app_file_tenant,
                       url_prefix=url_prefix)
app.register_blueprint(app_file_role,
                       url_prefix=url_prefix)
app.register_blueprint(app_file_form_template,
                       url_prefix=url_prefix)
app.register_blueprint(app_file_site,
                       url_prefix=url_prefix)
app.register_blueprint(app_file_section,
                       url_prefix=url_prefix)

url_prefix_backoffice = "/backoffice/v1"
app.register_blueprint(app_file_backoffice,
                       url_prefix=url_prefix_backoffice)


@app.before_request
def before_request():
    g.current_user = None
    g.current_tenant = None
    
    try:
        tenant_id=request.args.get("tenant_id")
        if tenant_id is not None:
            g.current_tenant = getByIdOrByName(obj=Tenant, id=tenant_id)
        else:
            g.current_tenant = getByIdOrByName(obj=Tenant, id=config["default_tenant_config"])
    except:
        g.current_tenant = None
            
    try:
        res = verify_jwt_in_request(optional=True)
        if res is not None:
            current_user_id = get_jwt_identity()
            g.current_user = getByIdOrEmail(obj=User,  id=current_user_id)
    except:
        g.current_user = None
    
    #print(g.current_user)
    #print(g.current_tenant)
        
      
@app.after_request
def after_request(response):
    if g.current_user is not None:
        app.logger.info("user_id is "+ g.current_user.id)
    else:
       app.logger.info("no user")  
    return response


# Setup log folder
@app.before_first_request
def before_first_request():

    log_level = logging.INFO
 
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

    for handler in app.logger.handlers:
        app.logger.removeHandler(handler)
 
    root        = os.path.dirname(os.path.abspath(__file__))
    log_dir     = os.path.join(root, 'logs')
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    log_file    = os.path.join(log_dir, 'app.log')
    handler = logging.FileHandler(log_file)
    handler.setLevel(log_level)
    handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s"
        ))
    
    app.logger.addHandler(handler)
    app.logger.setLevel(log_level)



@app.route("/api/v1/init", methods=["GET"])
def init():
    print(app.config["JWT_TOKEN_LOCATION"] )
    app.config["JWT_TOKEN_LOCATION"] = ["headers"] 
    # db.drop_all()
    db.create_all()
    populate_tenant()
    populate_user_data()
    populate_type_intervention()
    populate_type_field()
    app.logger.info("db init done")
    app.config["JWT_TOKEN_LOCATION"] = ["headers","cookies"] 
    return "ok"
    
@app.route("/api/v1/swagger-ui", methods=["GET"])
def swagger():
    return render_template('swagger.html')

def populate_tenant():

    tenants=["ctei", "kysoe"];

    for newtenant in tenants:
            tenant=getByIdOrByName(Tenant, newtenant, None)
            if tenant is None:
                tenant = Tenant( name = newtenant)
                db.session.add(tenant)
                app.logger.debug("tenant added %s", tenant.name)
    db.session.commit()
  
  
def populate_type_field():

    types=["double", "string", "boolean", "integer", "json"];
    for type in types:
            type_field = TypeField( name = type)
            db.session.add(type_field)
            app.logger.debug("type_field added %s", type_field.name)
    db.session.commit()
    
def populate_type_intervention():
    
    
    types_interventions= config["types_interventions"]
    


    list=[
        {"type_intervention":"scaffolding request", "site":"trets","config":json.dumps(types_interventions["scaffolding request"], indent=4)},
          {"type_intervention":"calorifuge", "site":"trets","config":json.dumps(types_interventions["calorifuge"], indent=4)},
          {"type_intervention":"scaffolding request", "site":"iter","config":json.dumps(types_interventions["scaffolding request"], indent=4)},
          {"type_intervention":"scaffolding request", "site":"sandbox","config":json.dumps(types_interventions["scaffolding request"], indent=4)},
          {"type_intervention":"calorifuge", "site":"iter","config":json.dumps(types_interventions["calorifuge"], indent=4)},
          {"type_intervention":"calorifuge", "site":"sandbox","config":json.dumps(types_interventions["calorifuge"], indent=4) } 
          ];
    for item in list:
            _type_intervention=getByIdOrByName(TypeIntervention, item["type_intervention"], None)
            if _type_intervention is None:
                _type_intervention = TypeIntervention( name =item["type_intervention"])
                db.session.add(_type_intervention)
                app.logger.debug("_type_intervention added %s", _type_intervention.name)
            db.session.commit()    
            _site=getByIdOrByName(Site, item["site"], None)

            _type_intervention_site = TypeInterventionSite.query.get((_type_intervention.id,_site.id))
            if _type_intervention_site is None:
                (_type_intervention_site) = TypeInterventionSite(
                    type_intervention_id=_type_intervention.id,
                    site_id=_site.id,
                    template_text=item["config"]
                )
                db.session.add(_type_intervention_site)
            else:
                 _type_intervention_site.template_text=item["config"]
      
            update_sites_interventions_templates(_site, _type_intervention, json.loads(item["config"]))
                
            
                
    db.session.commit()
    
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
            
            print("------------------")
            print(form_values)
            
            sections=form_values["sections"]
            if sections is not None:
                for key_sections in sections.keys():
                    print("Section #", key_sections)
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
                   
                    
                    fields=section_values["fields"]
                    if fields is not None:
                        for key_field in fields.keys():
                            print("Field #", key_field)
                            field_attributes=fields[key_field]
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
                                    # field_type=field_type,
                                    field_order_in_section=int(key_field)
                                )
                                db.session.add(_field)
                               #  db.session.commit()
                            
    db.session.commit()                
                        

    
def populate_user_data():
        print("to")
        dataTenant =  {
                 "kysoe_tenant": {
                    "tenant_admin_user": {
                                    "email": "yannick.simon@gmail.com", 
                                    "password": "12345678", 
                                    "phone": "+33651556170",
                                    "firstname":"Yannick", 
                                    "lastname":"Simon",
                                    "company": "kysoe",
                    },
                    "sites": [
                        {"site":
                            { 
                            "name": "trets",
                            "users": [
                                {"user":
                                    { 
                                    "email": "yannick.simon@gmail.com", 
                                    "password": "12345678", 
                                    "phone": "+33651556170",
                                    "firstname":"Yannick", 
                                    "lastname":"Simon",
                                    "company": "kysoe",
                                    "sites_roles":  config["roles"]
                                    }
                                },
                                {"user":
                                    { 
                                    "email": "luc.henquinet@ctei.fr", 
                                    "password": "12345678", 
                                    "phone": "+33651556170",
                                    "firstname":"Luc", 
                                    "lastname":"Henquinet",
                                    "company": "ctei",
                                    "sites_roles":  config["roles"]
                                    }
                                }
                            ]
                            }
                        }
                    ]
                 },   
                "ctei_tenant": {
                    "tenant_admin_user": {
                                    "email": "luc.henquinet@ctei.fr", 
                                    "password": "12345678", 
                                    "phone": "+33651556170",
                                    "firstname":"Luc", 
                                    "lastname":"Henquinet",
                                    "company": "ctei",
                    },
                    "sites": [
                        {"site":
                            { 
                            "name": "iter",
                            
                            "users": [
                                {"user":
                                    { 
                                    "email": "yannick.simon@gmail.com", 
                                    "password": "12345678", 
                                    "phone": "+33651556170",
                                    "firstname":"Yannick", 
                                    "lastname":"Simon",
                                    "company": "kysoe",
                                    "sites_roles": config["roles"]
                                    }
                                },
                                {"user":
                                    { 
                                    "email": "luc.henquinet@ctei.fr", 
                                    "password": "12345678", 
                                    "phone": "+33651556170",
                                    "firstname":"Luc", 
                                    "lastname":"Henquinet",
                                    "company": "ctei",
                                    "sites_roles":  config["roles"]
                                    }
                                }
                            ]
                            }
                        }
                        ,
                        {"site": 
                            {
                            "name": "sandbox",
                            "users": [
                                {"user":
                                    { 
                                    "email": "yannick.simon@gmail.com", 
                                    "password": "12345678", 
                                    "phone": "+33651556170",
                                    "firstname":"Yannick", 
                                    "lastname":"Simon",
                                    "company": "kysoe",
                                    "sites_roles": config["roles"]
                                    }
                                },
                                {"user":
                                    { 
                                    "email": "luc.henquinet@ctei.fr", 
                                    "password": "12345678", 
                                    "phone": "+33651556170",
                                    "firstname":"Luc", 
                                    "lastname":"Henquinet",
                                    "company": "ctei",
                                    "sites_roles": config["roles"]
                                    }
                                }
                            ]
                            }
                        }
                    ] 
                }     
            }
        
       
        for tenant, itemtenant in dataTenant.items():
            _admin_tenant_user = getByIdOrEmail(obj=User, id=itemtenant["tenant_admin_user"]["email"])
            if _admin_tenant_user is None:
                _admin_tenant_user = User(
                        email= itemtenant["tenant_admin_user"]["email"],
                        password= itemtenant["tenant_admin_user"]["password"],
                        tenant_id = None,
                    )
                _admin_tenant_user.hash_password()
                db.session.add(_admin_tenant_user)  
                app.logger.info("_admin_tenant_user added %s", _admin_tenant_user.email)
            else:
                app.logger.info("_admin_tenant_user exists %s", _admin_tenant_user.email)
                
            _tenant = getByIdOrByName(obj=Tenant, id=tenant, tenant_id=None)
            if _tenant is None:
                _tenant = Tenant( name = tenant, admin_tenant_user_id=_admin_tenant_user.id )
                db.session.add(_tenant)
                app.logger.info("tenant added %s", _tenant.name)
            else:
                _tenant.admin_tenant_user_id=_admin_tenant_user.id
                app.logger.info("tenant updated %s", _tenant.name)
            db.session.commit() 
                
            
            for item in itemtenant["sites"]:
                itemsite=item["site"]
                site_name = itemsite["name"]
                app.logger.info("- site %s", site_name)
                _site = getByIdOrByName(obj= Site, id=site_name,  tenant_id=_tenant.id)
                if _site is None:
                    _site = Site(
                                        name = site_name,
                                        tenant_id = _tenant.id
                                    )
                    db.session.add(_site)
                    db.session.commit() 
                            
                for item2 in itemsite["users"]:
                    itemuser = item2["user"]
                    app.logger.info("- site %s - user %s", site_name, itemuser["email"])
                    _company = getByIdOrByName(obj=Company, id=itemuser["company"], tenant_id=_tenant.id)
                    if _company is None:
                        _company = Company(
                            name = itemuser["company"],
                            tenant_id = _tenant.id
                            )
                        db.session.add(_company)
                        app.logger.info("- site %s - user %s - company %s added", site_name, itemuser["email"], _company.name)
                        db.session.commit() 
                    else:
                        app.logger.info("- site %s - user %s - company %s exists", site_name, itemuser["email"], _company.name)
                        
                        
                    _user = getByIdOrEmail(obj=User, id=itemuser["email"])
                    if _user is None:
                        _user = User(
                                    email= itemuser["email"],
                                    password= itemuser["password"],
                                    phone= itemuser["phone"],
                                    tenant_id = None,
                                    company_id = _company.id,
                                    firstname=itemuser["firstname"],
                                    lastname=itemuser["lastname"]
                                )
                        _user.hash_password()
                        db.session.add(_user)  
                        app.logger.info("user added %s", _user.email)
                    else:
                        _user.tenant_id     = None
                        _user.firstname     = itemuser["firstname"]
                        _user.lastname      = itemuser["lastname"]
                        _user.password      = itemuser["password"]
                        _user.phone         = itemuser["phone"]
                        _user.company_id    = _company.id
                        _user.hash_password()
                        app.logger.info("user updated %s", _user.email)
                    
                    # _user.roles.clear()
                        
                    for role_name in itemuser["sites_roles"]:
                        app.logger.debug("role %s",role_name)
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
                            app.logger.debug("role added %s", _role.name)
                        _user.roles.append(_role)
                        app.logger.debug("role added %s for user %s", _role.name, _user.email)
                        

                
   
        db.session.commit() 
        app.logger.debug("populate users done")
    
    
   