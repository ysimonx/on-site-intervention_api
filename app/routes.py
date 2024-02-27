import os
import logging
import datetime
import json
import uuid
from flask                      import jsonify, abort, render_template, g, request
from flask_mail                 import Mail
from flask_jwt_extended         import JWTManager, get_jwt_identity, verify_jwt_in_request
from config import config, Config

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

app.config['MAIL_SERVER']               = Config.MAIL_SERVER
app.config['MAIL_PORT']                 = Config.MAIL_PORT 
app.config['MAIL_USE_SSL']              = Config.MAIL_USE_SSL
app.config['MAIL_USERNAME']             = Config.MAIL_USERNAME
app.config['MAIL_PASSWORD']             = Config.MAIL_PASSWORD
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False




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
    
    # 
    try:
        xf = request.headers.get('X-Forwarded-For')
        app.logger.info("before_request X-Forwarded-For : %s", xf)
    except:
        app.logger.info("before_request no X-Forwarded-For")



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
            app.logger.info("before request access token ok")
            current_user_id = get_jwt_identity()
            g.current_user = getByIdOrEmail(obj=User,  id=current_user_id)
            app.logger.info("before request access token email = %s" % g.current_user.email)
    except:
        app.logger.info("before_request except on access token")
        g.current_user = None

    
        
      
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
    # populate_user_data()
    populate_type_field()
    app.logger.info("db init done")
    app.config["JWT_TOKEN_LOCATION"] = ["headers","cookies"] 
    return "ok"
    
@app.route("/api/v1/swagger-ui", methods=["GET"])
def swagger():
    return render_template('swagger.html')

def populate_tenant():

    tenants=["ctei_tenant", "kysoe_tenant"];

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
                       
                    ] 
                }     
            }
        
                
   
        db.session.commit() 
        app.logger.debug("populate users done")
    
    
   