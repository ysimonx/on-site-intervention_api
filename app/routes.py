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
from app.model_dir.organization import Organization
from app.model_dir.type_field   import TypeField
from app.model_dir.place        import Place
from app.model_dir.intervention import Intervention
from app.model_dir.section      import Section
from app.model_dir.field        import Field
from app.model_dir.form         import Form



from app.model_dir.type_intervention   import TypeIntervention, TypeInterventionOrganization

from .route_dir.tenant          import app_file_tenant
from .route_dir.organization    import app_file_organization
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
app.register_blueprint(app_file_organization,
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
    
    tenant_id=request.args.get("tenant_id")
    if tenant_id is not None:
        g.current_tenant = getByIdOrByName(obj=Tenant, id=tenant_id)
    else:
        g.current_tenant = getByIdOrByName(obj=Tenant, id=config["default_tenant_config"])
            
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
    # db.create_all()
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

    tenants=["fidwork"];

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
    
    
    types_interventions= {
        "scaffolding request": {  
            "type_intervention": "scaffolding request",
            "intervention_on_site_uuid": "67ecd9b0-ff04-4eae-80fa-c55c2c3a45bf",
            "forms": {
                "1" :{"form_name":"initial request",
                      "form_on_site_uuid": "9f1f20e3-d3cd-4a58-97fc-2e42a4d7b736",
                      "sections": {
                          "1": { "section_name" : "initial request rub a",
                                 "section_type" : "section type 1",
                                 "section_on_site_uuid": "ef637435-30fe-4a3f-941f-f29a8df8f865",
                                 "fields": {
                                     "1": { "field_name": "field aa",
                                           "field_type": "field_type 1","field_on_site_uuid":"46d8ccd9-5580-4c92-b9cc-eebb76b9c57c"},
                                     "2": { "field_name": "field ab",
                                           "field_type": "field_type 1","field_on_site_uuid":"0b3f2281-cb74-4122-bdb5-353214e7c611"},
                                     "3": { "field_name": "field ac",
                                           "field_type": "field_type 1","field_on_site_uuid":"0b3f2281-cb74-4122-bdb5-353214e7c611"},
                                 }
                                },
                                 
                          "2": { "section_name" : "initial request rub b",
                                "section_type" : "section type 2",
                                "section_on_site_uuid": "6b8b8b4c-8bca-4697-8c3c-6b70d4fd9b51",
                                 "fields": {
                                     "1": { "field_name": "field ba",
                                           "field_type": "field_type 1","field_on_site_uuid":"0b3f2281-cb74-4122-bdb5-353214e7c611"},
                                     "2": { "field_name": "field bb",
                                           "field_type": "field_type 1","field_on_site_uuid":"30a238fe-5de1-48c6-b91a-3d177124f634"},
                                     "3": { "field_name": "field bc",
                                           "field_type": "field_type 1","field_on_site_uuid":"f249bf91-9bfd-4516-96a5-94bd31e9e391"},
                                 } },
                          "3": { "section_name" : "initial request rub c",
                                "section_type" : "section type 3",
                                "section_on_site_uuid": "83ce8e7f-1c28-4270-bede-9bd5dcd6ab0e",
                                 "fields": {
                                     "1": { "field_name": "field ca",
                                           "field_type": "field_type 1","field_on_site_uuid":"9d4f8747-f238-4c41-81b7-b16adb97d9c7"},
                                     "2": { "field_name": "field cb",
                                           "field_type": "field_type 1","field_on_site_uuid":"7669d2b9-e626-4acc-842c-6922d2737a1f"},
                                     "3": { "field_name": "field cc",
                                           "field_type": "field_type 1","field_on_site_uuid":"d76e74ca-b7ce-463c-b833-4ba45585d224"},
                                 } },
                     }
                    },
                "2" :{"form_name":"visit",
                      "form_on_site_uuid": "a81c475c-3b9d-40da-839d-56eeee06e85a",
                      "sections": {
                          "1": { "section_name" : "Techniques",
                                "section_type" : "section type 1",
                                "section_on_site_uuid": "11b19f92-b590-44d5-b29c-4144b709bd9b",
                                 "fields": {
                                    "1": { "field_name":"scaff_type",
                                           "field_label":"Type",
                                           "field_type":"list",
                                           "field_on_site_uuid":"e28cbc05-2f4b-46f5-acca-c147ae8a1db8",
                                           "values": [
                                               "Fixe",
                                               "Roulant",
                                               "Balisage en dur",
                                               "Protection", 
                                               "Potence",
                                               "Escalier",
                                               "Autre"
                                            ] 
                                    },
                                     "2": { "field_name":"visit_date",
                                           "field_label":"Visit Date",
                                           "field_type":"date",
                                           "field_on_site_uuid":"a1d5131d-d8bc-4783-8c0b-fb81f5e4a459",
                                           "default_value":"now"
                                          
                                    }
                                 }
                                },
                          "2": { "section_name" : "Dimensions",
                                "section_type" : "section type 1",
                                "section_on_site_uuid": "de3b8182-df35-4c6a-9aea-8d652efd8142",
                                 "fields": {
                                      "1": { "field_name":"scaff_charge_exploitation_prevue",
                                           "field_label":"Charge Exploit prévue",
                                           "field_type":"list",
                                           "field_on_site_uuid":"43f30456-0f0d-4fef-842c-01f869f85cdd",
                                           "values": [
                                               "Classe 3 (répartis 250kg/m2)",
                                               "Classe 4 et 5 (300kg/m2>répartis<450kg/m2)",
                                               "Classe 6 (450 Kg/m2>répartis<600kg/m2)",
                                               "autre(à renseigner dans commentaire)", 
                                               
                                            ] 
                                        },
                                      "2": { "field_name":"scaff_conforme_notice",
                                           "field_label":"Conforme Notice",
                                           "field_type":"switch",
                                           "field_on_site_uuid":"fb737b8d-db58-418f-a69f-b437539cdec6",
                                           "value_on": "oui",
                                           "value_off": "non"
                                      },
                                      "3": { "field_name":"visit_date_reception_prevue",
                                           "field_label":"Date Réception prévue",
                                           "field_type":"date",
                                           "field_on_site_uuid":"4d83d71d-adfe-45f8-968c-5d9761f4c288",
                                           "default_value":"j+15",
                                      },
                                     "4": { "field_name": "scaff_width",
                                            "field_label": "Longueur",
                                           "field_type": "integer",
                                           "field_on_site_uuid":"8dd3f411-6f67-43c4-9d9d-1d420cc6bc68"
                                           },
                                     "5": { "field_name": "scaff_depth",
                                           "field_label": "Largeur",
                                           "field_type": "integer",
                                           "field_on_site_uuid":"0b1a49af-757f-4127-a0fb-f525d2f71f70"},
                                     "6": { "field_name": "scaff_height",
                                            "field_label": "Hauteur",
                                           "field_type": "integer",
                                           "field_on_site_uuid":"29c05fa8-c1d6-4026-bd4a-356a1e0eca7b"},
                                      "7": { "field_name":"scaff_nb_planchers_travail",
                                           "field_label":"Nombre de planchers travail",
                                           "field_type":"list",
                                           "field_on_site_uuid":"552460e5-b326-4cba-816c-e84202f1f83c",
                                           "values": [
                                               "1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"
                                            ] 
                                    },
                                 }
                                },
                                 
                         
                            
                        }
                    },
                "3" :{"form_name":"commissioning",
                      "form_on_site_uuid": "e773e72b-e00e-4fcc-b6be-fbfb70307351",
                      "sections": {
                          "1": { "section_name" : "commissioning rub a",
                                "section_type" : "section type 1",
                                "section_on_site_uuid": "7c1b3d74-b98a-43a5-9520-dee3a22f7dcb",
                                 "fields": {
                                     "1": { "field_name": "field aa",
                                           "field_type": "field_type 1","field_on_site_uuid":"27f76c97-0ea7-4274-ae09-62748bfc4a33"},
                                     "2": { "field_name": "field ab",
                                           "field_type": "field_type 1","field_on_site_uuid":"f1ee438e-580f-4760-a748-6621f3c32ecf"},
                                     "3": { "field_name": "field ac",
                                           "field_type": "field_type 1","field_on_site_uuid":"54dfe367-ba00-40e6-9eb1-cda38bc7d896"},
                                 }
                                },
                                 
                          "2": { "section_name" : "commissioning rub b",
                                "section_type" : "section type 1",
                                "section_on_site_uuid": "9d33f2b7-6543-4738-b974-1892ce675260",
                                 "fields": {
                                     "1": { "field_name": "field ba",
                                           "field_type": "field_type 1","field_on_site_uuid":"f00da6cd-aa31-49bd-a2f0-a85fe275240e"},
                                     "2": { "field_name": "field bb",
                                           "field_type": "field_type 1","field_on_site_uuid":"20a26c7c-321f-407d-ba39-2b6ca7c623dc"},
                                     "3": { "field_name": "field bc",
                                           "field_type": "field_type 1","field_on_site_uuid":"e9f823c0-956d-4cf9-b3e6-cd13e58f1551"},
                                 } },
                          "3": { "section_name" : "commissioning rub c",
                                "section_type" : "section type 1",
                                "section_on_site_uuid": "0d19ba0a-1af3-4f7d-9243-b7ae04634c39",
                                 "fields": {
                                     "1": { "field_name": "field ca",
                                           "field_type": "field_type 1","field_on_site_uuid":"5c69d56e-fdb6-4bd3-8973-620479e4045f"},
                                     "2": { "field_name": "field cb",
                                           "field_type": "field_type 1","field_on_site_uuid":"2d502bd6-7e18-4018-8821-1b7d66b7fe03"},
                                     "3": { "field_name": "field cc",
                                           "field_type": "field_type 1","field_on_site_uuid":"672e17c1-9aec-4a54-a2a0-35b5c59fdb55"},
                                 } },
                     }
                      },
                "4" :{"form_name":"rapport de vérifications",
                      "form_on_site_uuid": "3e5a68a0-ac2f-4bf0-9f96-e2cf205b658e",
                      "sections": {
                          "1": { "section_name" : "rapport de vérifications rub a",
                                 "section_type" : "section type 1",
                                 "section_on_site_uuid": "0d19ba0a-1af3-4f7d-9243-b7ae04634c39",
                                 "fields": {
                                     "1": { "field_name": "field aa",
                                           "field_type": "field_type 1","field_on_site_uuid":"11aa7a09-14ff-4766-b1ba-e541a25ed9e5"},
                                     "2": { "field_name": "field ab",
                                           "field_type": "field_type 1","field_on_site_uuid":"398e5a3c-d583-4265-ba40-e01dd2a1c28a"},
                                     "3": { "field_name": "field ac",
                                           "field_type": "field_type 1","field_on_site_uuid":"042089d1-6b32-49cf-b3a7-1e86e68e26e4"},
                                 }
                                },
                                 
                          "2": { "section_name" : "rapport de vérifications rub b",
                                 "section_type" : "section type 1",
                                 "section_on_site_uuid": "8f21a7d9-854e-4faf-8f26-180b7b5cc6c3",
                                 "fields": {
                                     "1": { "field_name": "field ba",
                                           "field_type": "field_type 1","field_on_site_uuid":"6312e0e9-2210-4487-8c7c-8e210448b6f3"},
                                     "2": { "field_name": "field bb",
                                           "field_type": "field_type 1","field_on_site_uuid":"8940a306-5532-440e-b43b-cce0538b8820"},
                                     "3": { "field_name": "field bc",
                                           "field_type": "field_type 1","field_on_site_uuid":"eafc1f34-c858-441c-b061-86d799547651"},
                                 } },
                          "3": { "section_name" : "rapport de vérifications rub c",
                                 "section_type" : "section type 1",
                                 "section_on_site_uuid": "026d86e1-7256-4fb9-a306-e413fbd925cc",
                                 "fields": {
                                     "1": { "field_name": "field ca",
                                           "field_type": "field_type 1","field_on_site_uuid":"bdc1b557-039c-42db-9f59-adcaf25435f0"},
                                     "2": { "field_name": "field cb",
                                           "field_type": "field_type 1","field_on_site_uuid":"7a24e3d4-fbf4-40a8-85ae-4dc0be6faf1d"},
                                     "3": { "field_name": "field cc",
                                           "field_type": "field_type 1","field_on_site_uuid":"7a24e3d4-fbf4-40a8-85ae-4dc0be6faf1d"},
                                 } },
                     }}
            }
        },
        "calorifuge": {  
            "type_intervention": "calorifuge",
            "intervention_on_site_uuid": "5ceba891-670a-40ea-ba7f-87bd4597dbde",
            "forms": {
                "1" :{"form_name":"initial request 2",
                      "form_on_site_uuid": "b89cf79e-36d2-4a65-ad01-479dc2e769f8",
                       "sections": {}},
                "2" :{"form_name":"visit 2",
                      "form_on_site_uuid": "f35f3474-2d1d-407f-ac72-1b70f89ff08f",
                       "sections": {}},
                "3" :{"form_name":"commissioning 2",
                      "form_on_site_uuid": "6c4480f5-8e95-4a9b-9bcc-254e76d682c",
                       "sections": {}},
                "4" :{"form_name":"rapport de vérifications 2",
                      "form_on_site_uuid": "47d8d1e6-9273-4286-8de3-ba6d80233b4f",
                       "sections": {}}
            }
        }
    }
    


    list=[ 
          {"type_intervention":"scaffolding request", "organization":"iter","config":json.dumps(types_interventions["scaffolding request"], indent=4)},
          {"type_intervention":"scaffolding request", "organization":"sandbox","config":json.dumps(types_interventions["scaffolding request"], indent=4)},
          {"type_intervention":"calorifuge", "organization":"iter","config":json.dumps(types_interventions["calorifuge"], indent=4)},
          {"type_intervention":"calorifuge", "organization":"sandbox","config":json.dumps(types_interventions["calorifuge"], indent=4) } 
          ];
    for item in list:
            _type_intervention=getByIdOrByName(TypeIntervention, item["type_intervention"], None)
            if _type_intervention is None:
                _type_intervention = TypeIntervention( name =item["type_intervention"])
                db.session.add(_type_intervention)
                app.logger.debug("_type_intervention added %s", _type_intervention.name)
            db.session.commit()    
            _organization=getByIdOrByName(Organization, item["organization"], None)

            _type_intervention_organization = TypeInterventionOrganization.query.get((_type_intervention.id,_organization.id))
            if _type_intervention_organization is None:
                (_type_intervention_organization) = TypeInterventionOrganization(
                    type_intervention_id=_type_intervention.id,
                    organization_id=_organization.id,
                    template_text=item["config"]
                )
                db.session.add(_type_intervention_organization)
            else:
                 _type_intervention_organization.template_text=item["config"]
      
            update_organizations_interventions_templates(_organization, _type_intervention, json.loads(item["config"]))
                
            
                
    db.session.commit()
    
def update_organizations_interventions_templates( _organization,  _type_intervention, template ):
      
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
    dataTenant =  {
        
                "fidwork": {
                    "tenant_admin_user": {
                         "email": "yannick.simon@gmail.com", 
                         "password": "12345678" 
                    },
                    "users": [
                    { 
                         "email": "yannick.simon@gmail.com", 
                         "password": "12345678", 
                         "phone": "+33651556170",
                         "firstname":"Yannick", 
                         "lastname":"Simon",
                         "company": "kysoe",
                         "organizations_roles": [
                            {
                             "organization":"sandbox",
                             "roles": ["admin","toy", "supervisor"]
                            },
                            {
                             "organization":"iter",
                             "roles": ["admin","gnass", "supervisor"]
                            }
                         ]
                         
                    },
                ] }
                
                }
    
       
    for tenant, item in dataTenant.items():
        
        _admin_tenant_user = getByIdOrEmail(obj=User, id=item["tenant_admin_user"]["email"])
        if _admin_tenant_user is None:
                _admin_tenant_user = User(
                            email= item["tenant_admin_user"]["email"],
                            password= item["tenant_admin_user"]["password"],
                            tenant_id = None,
                        )
                _admin_tenant_user.hash_password()
                db.session.add(_admin_tenant_user)  
                app.logger.debug("_admin_tenant_user added %s", _admin_tenant_user.email)
        
           
        
        _tenant = getByIdOrByName(obj=Tenant, id=tenant, tenant_id=None)
        if _tenant is None:
            _tenant = Tenant( name = tenant, admin_tenant_user_id=_admin_tenant_user.id )
            db.session.add(_tenant)
        else:
            _tenant.admin_tenant_user_id=_admin_tenant_user.id
        db.session.commit() 
            
        app.logger.debug("tenant added %s", _tenant.name)
         
        for user in item["users"]:
            
            _company = getByIdOrByName(obj=Company, id=user["company"], tenant_id=_tenant.id)
            if _company is None:
                _company = Company(
                    name = user["company"],
                    tenant_id = _tenant.id
                    )
                db.session.add(_company)
                db.session.commit() 
                
                
            _user = getByIdOrEmail(obj=User, id=user["email"])
            if _user is None:
                _user = User(
                            email= user["email"],
                            password= user["password"],
                            phone= user["phone"],
                            tenant_id = None,
                            company_id = _company.id,
                            firstname=user["firstname"],
                            lastname=user["lastname"]
                        )
                _user.hash_password()
                db.session.add(_user)  
                app.logger.debug("user added %s", _user.email)
            else:
                _user.tenant_id     = None
                _user.firstname     = user["firstname"]
                _user.lastname      = user["lastname"]
                _user.password      = user["password"]
                _user.phone         = user["phone"]
                _user.hash_password()
                app.logger.debug("user updated %s", _user.email)
            
            _user.roles.clear()
                
            for organization_role in user["organizations_roles"]:
                organization_name = organization_role["organization"]
                _organization = getByIdOrByName(obj= Organization, id=organization_name,  tenant_id=_tenant.id)
                if _organization is None:
                    _organization = Organization(
                                        name = organization_name,
                                        tenant_id = _tenant.id
                                    )
                    db.session.add(_organization)
                    db.session.commit() 
                
                # annule et remplace les roles
                
                for role_name in organization_role["roles"]:
                    _role = getByIdOrByName(
                        obj=Role, 
                        id=role_name, 
                        tenant_id=_tenant.id, 
                        organization_id=_organization.id
                    )
                    # _role = Role.query.filter(Role.tenant_id==_tenant.id).filter(Role.name==role_name).first()
                    if _role is None:
                        _role = Role(
                            name=role_name, 
                            tenant_id=_tenant.id,
                            organization_id=_organization.id
                        )
                        db.session.add(_role)
                        app.logger.debug("role added %s", _role.name)
                    _user.roles.append(_role)
                
            
                    

        #   
    db.session.commit() 
    app.logger.debug("populate users done")
   
    
   