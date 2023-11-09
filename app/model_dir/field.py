from .. import db
from .mymixin import MyMixin

from sqlalchemy.orm import declarative_base, relationship, backref
import uuid


class Field(db.Model, MyMixin):
    __tablename__ = 'fields'
    
    field_uuid          = db.Column(db.String(255), unique=True)
    field_data          = db.Column(db.Text())
    field_data_md5      = db.Column(db.String(32))
    intervention_uuid   = db.Column(db.String(255), db.ForeignKey("interventions.intervention_uuid"))
    average_latitude    = db.Column(db.Float)
    average_longitude   = db.Column(db.Float)
    formulaire_id       = db.Column(db.String(36), db.ForeignKey("formulaires.id"))
    
    def to_json(self):
        return {
            'id':                   self.id,
            'name':                 self.name,
            '_internal' :           self.get_internal(),
            'field_uuid':           self.field_uuid,
            'field_data':           self.field_data,
            'field_data_md5':       self.field_data_md5,
            'formulaire_id':        self.formulaire_id,
            'average_latitude':     self.average_latitude,
            'average_longitude':    self.average_longitude,
            'intervention_uuid':    self.intervention_uuid
            
        }
        
    def to_json_light(self):
        return {
            'id':                   self.id,
            'name':                 self.name,
            'field_uuid':           self.field_uuid,
            'field_data':           self.field_data,
            'field_data_md5':       self.field_data_md5,
            'formulaire_id':        self.formulaire_id,
            'average_latitude':     self.average_latitude,
            'average_longitude':    self.average_longitude,
            'intervention_uuid':    self.intervention_uuid
        }


from sqlalchemy import event
@event.listens_for(Field, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
