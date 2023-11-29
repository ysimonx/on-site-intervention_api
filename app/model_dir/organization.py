from .. import db,  getByIdOrByName
import uuid
from flask import Flask, abort, make_response, request, jsonify
from sqlalchemy.orm import declarative_base, relationship, backref

from .mymixin import MyMixin

def formatted_date_iso(date):
    if date is None:
        return None
    return date.isoformat()


class Organization(db.Model, MyMixin):
    __tablename__ = 'organizations'
   
    id              = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    name            = db.Column(db.String(255), index=True)

    time_created    = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    time_updated    = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    
                
    def get_internal(self):

        
        return {
                
                'time_created_utc': formatted_date_iso(self.time_created),
                'time_updated_utc': formatted_date_iso(self.time_updated)
               
            }
        
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

    def getOrganization():
        _organization = Organization.query.filter(Organization.name=="sandbox").first()
        return _organization
    
    def getRequestOrganization():
    
        #
        # TODO
        # should verify that this user is an authorized one for this organization
        # should verify that this user has a role able to upload photo
        # 
    
        if request.is_json:
            if not 'organization_id' in request.json:
                abort(make_response(jsonify(error="missing organization_id parameter"), 400))
            organization_id                   = request.json.get('organization_id')
        else:
            if not 'organization_id' in request.form:
                abort(make_response(jsonify(error="missing organization_id parameter"), 400))   
            organization_id                   = request.form.get('organization_id')  
              
        print("organization_id =", organization_id)     
            
        organization=getByIdOrByName(Organization, organization_id)
        if organization is None:
            abort(make_response(jsonify(error="organization not found"), 400))
            
        return organization
        
from sqlalchemy import event
@event.listens_for(Organization, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
