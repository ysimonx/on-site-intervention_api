from .. import db
from .mymixin import MyMixin

from sqlalchemy.orm import declarative_base, relationship, backref
from sqlalchemy import inspect

import uuid
import json

class Field(db.Model, MyMixin):
    __tablename__ = 'fields'
    
    field_on_site_uuid          = db.Column(db.String(255), unique=True)
    report_on_site_uuid         = db.Column(db.String(36), index=True)
    report_id                   = db.Column(db.String(36), db.ForeignKey("reports.id"), nullable=True)
    field_name                  = db.Column(db.String(255), index=True)
    field_value                 = db.Column(db.String(255), index=True)
    field_type                  = db.Column(db.String(255), index=True)
    average_latitude            = db.Column(db.Float)
    average_longitude           = db.Column(db.Float)
    
    
    photos                      = relationship("Photo",   
                                                cascade="all, delete", 
                                                backref=backref("photos",lazy="joined"))
    
    

    
    def to_json(self):
        return {
            'id':                   self.id,
            'name':                 self.name,
            '_internal' :           self.get_internal(),
            'field_name':           self.field_name,
            'field_value':          self.field_value_as_string,
            'field_type':           self.field_type,
            'report_id':            self.report_id,
            'average_latitude':     self.average_latitude,
            'average_longitude':    self.average_longitude,
        }
        
    def to_json_light(self):
        return {
            'id':                   self.id,
            'name':                 self.name,
            '_internal' :           self.get_internal(),
            'field_name':           self.field_name,
            'field_value':          self.field_value_as_string,
            'field_type':           self.field_type,
            'report_id':            self.report_id,
            'average_latitude':     self.average_latitude,
            'average_longitude':    self.average_longitude,
        }

    def get_attributes_for_thingsboard(self):
        dict_attributes=super().get_attributes_for_thingsboard()
        
        # remove relationship
        del dict_attributes["photos"]
        
        # convert field_value to value usefull for thingsboard
        new_value = self.field_value
        if (self.field_type == "string"):
            new_value = str(self.field_value)
        if (self.field_type == "double"):
            new_value = float(self.field_value)
        if (self.field_type == "integer"):
            new_value = int(self.field_value)
        if (self.field_type == "boolean"):
            if (self.field_value == "true"):
                new_value = True
            else:
                new_value = False
        if (self.field_type == "json"):
            new_value = json.loads(self.field_value)
              
        dict_attributes["field_value"] = new_value

        return dict_attributes
    
from sqlalchemy import event
@event.listens_for(Field, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
    
