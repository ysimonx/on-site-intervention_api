from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import config




db = SQLAlchemy()

import uuid

def create_app(config_name):
    from flask_cors import CORS
    
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    return app

def getByIdOrByName(obj, id, tenant_id, organization_id=None):
    result = None
    try:
        uuid.UUID(str(id))
        result = obj.query.get(id)
    except ValueError:
        result = obj.query.filter(obj.name==id)
        
        if tenant_id is not None:
            result = result.filter(obj.tenant_id==tenant_id)
        
        if organization_id is not None:
            result = result.filter(obj.organization_id==organization_id)
        
        
    return result.first()

def getByIdOrEmail(obj, id, tenant_id):
    result = None
    try:
        uuid.UUID(str(id))
        result = obj.query.get(id)
    except ValueError:
        if tenant_id is None:
            result = obj.query.filter(obj.email==id).first()
        else:
            result = obj.query.filter(obj.email==id).filter(obj.tenant_id==tenant_id).first()
    return result

def getByIdOrFilename(obj, id):
    result = None
    try:
        uuid.UUID(str(id))
        result = obj.query.get(id)
    except ValueError:
        result = obj.query.filter(obj.filename==id).first()
    return result
    
    
