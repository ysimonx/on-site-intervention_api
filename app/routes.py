import os
import logging
import datetime
from flask                      import jsonify, abort, render_template
from flask_mail                 import Mail
from flask_jwt_extended         import JWTManager

from .                          import create_app
from .                          import db, getByIdOrEmail, getByIdOrByName

from app.model_dir.user         import User, Role
from app.model_dir.company      import Company
from app.model_dir.tenant       import Tenant
from app.model_dir.type_field   import TypeField

from .route_dir.event           import app_file_event
from .route_dir.notification    import app_file_notification
from .route_dir.user            import app_file_user
from .route_dir.company         import app_file_company
from .route_dir.tenant          import app_file_tenant
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



app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.config['DEBUG'] = True

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"]           = "super-secret"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] =  datetime.timedelta(seconds=3600) # 1 heure
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
url_prefix_backoffice = "/backoffice/v1"
app.register_blueprint(app_file_backoffice,
                       url_prefix=url_prefix_backoffice)

"""
@app.before_request
def before_request():
    app.logger.info("before_request")

@app.after_request
def after_request(response):
    app.logger.info("after_request")
    return response
"""


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
    # db.drop_all()
    db.create_all()
    populate_tenant()
    populate_user_data()
    populate_type_field()
    app.logger.info("db init done")
    return "ok"
    
@app.route("/api/v1/swagger-ui", methods=["GET"])
def swagger():
    return render_template('swagger.html')


def populate_tenant():

    tenants=["sandbox","iter","arkema","total"];

    for newtenant in tenants:
            test=getByIdOrByName(Tenant, newtenant)
            if test is None:
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

    dataCompany =  {
                "kysoe": [
                    { 
                         "email": "yannick.simon@gmail.com", 
                         "password": "12345678", 
                         "firstname":"Yannick", 
                         "lastname":"Simon" ,
                         "roles": ["admin","toy"]
                    },
                ]    
                }
    
       
    for company, users in dataCompany.items():
        _company = getByIdOrByName(obj=Company, id=company)
        if _company is None:
            _company = Company( name = company)
            db.session.add(_company)
            app.logger.debug("company added %s", _company.name)
         
        for user in users:
            _user = getByIdOrEmail(obj=User, id=user["email"])
            if _user is None:
                _user = User(email= user["email"], password= user["password"], company_id = _company.id, firstname=user["firstname"], lastname=user["lastname"])
                _user.hash_password()
                db.session.add(_user)  
                app.logger.debug("user added %s", _user.email)
            else:
                _user.company_id = _company.id
                _user.firstname = user["firstname"]
                _user.lastname = user["lastname"]
                _user.password = user["password"]
                _user.hash_password()
                app.logger.debug("user updated %s", _user.email)
            for role in user["roles"]:
                _role = getByIdOrByName(Role, role)
                if _role is None:
                    _role = Role(name=role)
                    db.session.add(_role)
                    app.logger.debug("role added %s", _role.name)
                _user.roles.append(_role)

        #   
    db.session.commit() 
    app.logger.debug("populate users done")
   
    