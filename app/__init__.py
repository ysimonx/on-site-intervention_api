from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_migrate import Migrate



db = SQLAlchemy()

import uuid

def create_app(config_name):
    from flask_cors import CORS
    
    app = Flask(__name__)
    migrate = Migrate(app, db)
    
    CORS(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    return app

def getByIdOrByName(obj, id, tenant_id=None, site_id=None):
    result = None
    try:
        uuid.UUID(str(id))
        result = obj.query.get(id)
        return result
    except ValueError:
        # print("valueerror")
        result = obj.query.filter(obj.name==id)
        
        if tenant_id is not None:
            result = result.filter(obj.tenant_id==tenant_id)
        
        if site_id is not None:
            result = result.filter(obj.site_id==site_id)
        
        
        return result.first()
    
    return None

def getByIdOrEmail(obj, id):
    result = None
    try:
        uuid.UUID(str(id))
        result = obj.query.get(id)
    except ValueError:
        result = obj.query.filter(obj.email==id).first()
    return result

def getByIdOrFilename(obj, id):
    result = None
    try:
        uuid.UUID(str(id))
        result = obj.query.get(id)
    except ValueError:
        result = obj.query.filter(obj.filename==id).first()
    return result
    
    
