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

def getLastModified(values):
    
    tcutc = None
    tuutc = None
    maxutc = None
    for item in values:
        internal = item.get_internal()
        
        if tcutc is None:
            tcutc = internal["time_created_utc"]
            tuutc = internal["time_updated_utc"]
        else:
            if internal["time_created_utc"] is not None:
                if internal["time_created_utc"] > tcutc:
                    tcutc = internal["time_created_utc"]
            if internal["time_updated_utc"] is not None:
                if tuutc is None:
                    tuutc = internal["time_updated_utc"]
                else:
                    if internal["time_updated_utc"] > tuutc:
                        tuutc = internal["time_updated_utc"]
                    
                
    if tcutc is not None:
        maxutc = tcutc
        if tuutc is not None:
            if tuutc > tcutc :
                maxutc = tuutc
    return maxutc
       
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
    
    
    