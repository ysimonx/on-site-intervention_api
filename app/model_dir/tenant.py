from .. import db,  getByIdOrByName
import uuid
from flask import Flask, abort, make_response, request, jsonify
from sqlalchemy.orm import declarative_base, relationship, backref


class Tenant(db.Model):
    __tablename__ = 'tenants'
   
    id              = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    name            = db.Column(db.String(255), index=True)

    time_created    = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    time_updated    = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    
    def to_json(self):
        return {
            'id':               self.id,
            '_internal' :       self.get_internal(),
            'name':     self.name,
        }

    def to_json_light(self):
        return {
            'id':               self.id,
            'name':             self.name
        }
        
    def to_json_anonymous(self):
        return {
            'id':               self.id,
        }

    def getTenant():
        _tenant = Tenant.query.filter(Tenant.name=="sandbox").first()
        return _tenant
    
    def getRequestTenant():
    
        #
        # TODO
        # should verify that this user is an authorized one for this tenant
        # should verify that this user has a role able to upload photo
        # 
    
        if request.is_json:
            if not 'tenant_id' in request.json:
                abort(make_response(jsonify(error="missing tenant_id parameter"), 400))
            tenant_id                   = request.json.get('tenant_id')
        else:
            if not 'tenant_id' in request.form:
                abort(make_response(jsonify(error="missing tenant_id parameter"), 400))   
            tenant_id                   = request.form.get('tenant_id')  
              
        print("tenant_id =", tenant_id)     
            
        tenant=getByIdOrByName(Tenant, tenant_id)
        if tenant is None:
            abort(make_response(jsonify(error="tenant not found"), 400))
            
        return tenant
        