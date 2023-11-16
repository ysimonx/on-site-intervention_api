from .. import db
from .mymixin import MyMixin

from sqlalchemy.orm import declarative_base, relationship, backref
from sqlalchemy import inspect
from .type_field import TypeField

import uuid
import json

class Field(db.Model, MyMixin):
    __tablename__ = 'fields'
    
    field_on_site_uuid          = db.Column(db.String(255), unique=True)
    report_on_site_uuid         = db.Column(db.String(36),  index=True)
    report_id                   = db.Column(db.String(36),  db.ForeignKey("reports.id"), nullable=True)
    type_field_id               = db.Column(db.String(36),  db.ForeignKey("types_fields.id"), nullable=True)
    field_name                  = db.Column(db.String(255), index=True)
    field_value                 = db.Column(db.String(255), index=True)
    average_latitude            = db.Column(db.Float)
    average_longitude           = db.Column(db.Float)
    
    
    photos                      = relationship("Photo",   
                                                cascade="all, delete", 
                                                backref=backref("photos_backref",lazy="joined"))
    files                       = relationship("File",   
                                                cascade="all, delete", 
                                                backref=backref("files_backref",lazy="joined"))
    

    
    def to_json(self):
        return {
            'id':                   self.id,
            'name':                 self.name,
            '_internal' :           self.get_internal(),
            'field_name':           self.field_name,
            'field_value':          self.field_value,
            'type_field_id':           self.type_field_id,
            'report_id':            self.report_id,
            'average_latitude':     self.average_latitude,
            'average_longitude':    self.average_longitude,
            'photos':               [{"photo": item.to_json_light()} for item in self.photos] ,
            'files':                [{"file": item.to_json_light()} for item in self.files] ,
            'report':               self.report_backref.to_json_light(),
            'type_field':           self.type_field_backref.to_json()
            
        }
        
    def to_json_light(self):
        return {
            'id':                   self.id,
            'name':                 self.name,
            '_internal' :           self.get_internal(),
            'field_name':           self.field_name,
            'field_value':          self.field_value,
            'type_field_id':        self.type_field_id,
            'report_id':            self.report_id,
            'average_latitude':     self.average_latitude,
            'average_longitude':    self.average_longitude,
            'photos':  [{"photo": item.to_json_light()} for item in self.photos],
            'files':                [{"file": item.to_json_light()} for item in self.files] ,
            'type_field':           self.type_field_backref.to_json()
        }

    def get_attributes_for_thingsboard(self):
        dict_attributes=super().get_attributes_for_thingsboard()
        
        # convert field_value to value usefull for thingsboard
        new_value = self.field_value
        if (self.type_field_backref.name == "string"):
            new_value = str(self.field_value)
        if (self.type_field_backref.name == "double"):
            new_value = float(self.field_value)
        if (self.type_field_backref.name == "integer"):
            new_value = int(self.field_value)
        if (self.type_field_backref.name == "boolean"):
            if (self.field_value == "true"):
                new_value = True
            else:
                new_value = False
        if (self.type_field_backref.name == "json"):
            new_value = json.loads(self.field_value)
              
        dict_attributes["field_value"] = new_value

        return dict_attributes
    
from sqlalchemy import event
@event.listens_for(Field, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
    
