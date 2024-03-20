from .. import db,  getByIdOrByName
from .mymixin import user_role
import uuid
import json
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
    
    dict_of_lists   =  db.Column(db.Text)
    dict_of_lists_for_places = db.Column(db.Text)
    
    roles = db.relationship('Role')
    types_interventions = db.relationship('TypeInterventionSite')
    
    maxutc = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
        
    def to_json(self):
        
        res_dict_of_custom_fields={}
        for item in self.types_interventions:
            if item.dict_of_custom_fields is not None:
                res_dict_of_custom_fields[item.type_intervention.name] = json.loads(item.dict_of_custom_fields)
            else:
                res_dict_of_custom_fields[item.type_intervention.name] = {}
         
        print(res_dict_of_custom_fields)
        
        if self.dict_of_lists is None:
            dict_of_lists={}
        else:
            dict_of_lists =json.loads(self.dict_of_lists)
            
        if self.dict_of_lists_for_places is None:
            dict_of_lists_for_places={}
        else:
            dict_of_lists_for_places=json.loads(self.dict_of_lists_for_places)
            
        return {
            'id':               self.id,
            '_internal' :       self.get_internal(),
            'name':             self.name,
            'dict_of_lists':    dict_of_lists,
            'dict_of_lists_for_places': dict_of_lists_for_places,
            'maxutc':           self.maxutc,
            'roles'         :   [{item.name: item.to_json_light()} for item in self.roles] ,
            'types_interventions_dict_of_custom_fields':   res_dict_of_custom_fields
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

    def get_urlName(self):
        
        return self.name.replace(" ","-").lower()
    
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
    
