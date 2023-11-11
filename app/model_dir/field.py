from .. import db
from .mymixin import MyMixin

from sqlalchemy.orm import declarative_base, relationship, backref
from sqlalchemy import inspect

import uuid


class Field(db.Model, MyMixin):
    __tablename__ = 'fields'
    
    field_on_site_uuid          = db.Column(db.String(255), unique=True)
    field_data                  = db.Column(db.Text())
    field_data_md5              = db.Column(db.String(32))
    report_on_site_uuid         = db.Column(db.String(36), index=True)
    report_id                   = db.Column(db.String(36), db.ForeignKey("reports.id"), nullable=True)
    average_latitude            = db.Column(db.Float)
    average_longitude           = db.Column(db.Float)
    
    def to_json(self):
        return {
            'id':                   self.id,
            'name':                 self.name,
            '_internal' :           self.get_internal(),
            'field_on_site_uuid':   self.field_on_site_uuid,
            'field_data':           self.field_data,
            'field_data_md5':       self.field_data_md5,
            'report_id':            self.report_id,
            'average_latitude':     self.average_latitude,
            'average_longitude':    self.average_longitude,
        }
        
    def to_json_light(self):
        return {
            'id':                   self.id,
            'name':                 self.name,
            '_internal' :           self.get_internal(),
            'field_on_site_uuid':   self.field_on_site_uuid,
            'field_data':           self.field_data,
            'field_data_md5':       self.field_data_md5,
            'report_id':            self.report_id,
            'average_latitude':     self.average_latitude,
            'average_longitude':    self.average_longitude,
        }


from sqlalchemy import event
@event.listens_for(Field, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
