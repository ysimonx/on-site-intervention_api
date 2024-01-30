from .. import db,  getByIdOrByName
from .mymixin import user_role
import uuid
from flask import Flask, abort, make_response, request, jsonify
from sqlalchemy.orm import declarative_base, relationship, backref

from .mymixin import MyMixin

def formatted_date_iso(date):
    if date is None:
        return None
    return date.isoformat()


class Site(db.Model, MyMixin):
    __tablename__ = 'sites'
   
    id              = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    name            = db.Column(db.String(255), index=True)

    time_created    = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    time_updated    = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    
    roles = db.relationship('Role')
     
        
    def to_json(self):
        return {
            'id':               self.id,
            '_internal' :       self.get_internal(),
            'name':             self.name,
            'roles'         :  [{item.name: item.to_json_light()} for item in self.roles] 
        
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

    def getSite():
        _site = Site.query.filter(Site.name=="sandbox").first()
        return _site
    
    def getRequestSite():
    
        #
        # TODO
        # should verify that this user is an authorized one for this site
        # should verify that this user has a role able to upload photo
        # 
    
        if request.is_json:
            if not 'site_id' in request.json:
                abort(make_response(jsonify(error="missing site_id parameter"), 400))
            site_id                   = request.json.get('site_id')
        else:
            if not 'site_id' in request.form:
                abort(make_response(jsonify(error="missing site_id parameter"), 400))   
            site_id                   = request.form.get('site_id')  
              
            
        site=getByIdOrByName(Site, site_id)
        if site is None:
            abort(make_response(jsonify(error="site not found"), 400))
            
        return site
        
from sqlalchemy import event
@event.listens_for(Site, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
