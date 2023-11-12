from .. import db
from .mymixin import MyMixin

from sqlalchemy.orm import declarative_base, relationship, backref
import uuid
import json
import enum
from sqlalchemy import Enum


class FieldHisto(db.Model, MyMixin):
    __tablename__ = 'fields_histo'
    
    field_on_site_uuid          = db.Column(db.String(255), index=True)
    report_on_site_uuid         = db.Column(db.String(36), index=True)
    report_id                   = db.Column(db.String(36), db.ForeignKey("reports.id"), nullable=True)
    field_name                  = db.Column(db.String(255), index=True)
    field_value                 = db.Column(db.String(255), index=True)
    field_type                  = db.Column(db.String(255), index=True)
    average_latitude            = db.Column(db.Float)
    average_longitude           = db.Column(db.Float)
    
    def to_json(self):
        
        return {
            'id'                        : self.id,
            'name'                      : self.name,
            '_internal'                 : self.get_internal(),
            'field_on_site_uuid'        : self.field_on_site_uuid,
            'field_name'                : self.field_name,
            'field_value'               : self.field_value,
            'field_type'                : self.field_type,
            'report_id'                 : self.report_id,
            'report_on_site_uuid'       : self.report_on_site_uuid,
            'average_latitude'          : self.average_latitude,
            'average_longitude'         : self.average_longitude,
            
        }
        
    def to_json_light(self):
        return {
            'id'                        : self.id,
            'name'                      : self.name,
            '_internal'                 : self.get_internal(),
            'field_on_site_uuid'        : self.field_on_site_uuid,
            'field_name'                : self.field_name,
            'field_value'               : self.field_value,
            'field_type'                : self.field_type,
            'report_id'                 : self.report_id,
            'report_on_site_uuid'       : self.report_on_site_uuid,
            'average_latitude'          : self.average_latitude,
            'average_longitude'         : self.average_longitude,
            
        }
        


from sqlalchemy import event
@event.listens_for(FieldHisto, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
