from .. import db
from .mymixin import MyMixin

from sqlalchemy.orm import declarative_base, relationship, backref
import uuid


class Formulaire(db.Model, MyMixin):
    __tablename__ = 'formulaires'
    
    formulaire_uuid     = db.Column(db.String(255), unique=True)
    formulaire_data     = db.Column(db.Text())
    formulaire_data_md5 = db.Column(db.String(32))
    average_latitude    = db.Column(db.Float)
    average_longitude   = db.Column(db.Float)
    intervention_id     = db.Column(db.String(36), db.ForeignKey("interventions.id"))
    
    def to_json(self):
        return {
            'id': self.id,
            'name':                 self.name,
            '_internal' :           self.get_internal(),
            'formulaire_uuid':      self.formulaire_uuid,
            'formulaire_data':      self.formulaire_data,
            'formulaire_data_md5':  self.formulaire_data_md5,
            'intervention_id':      self.intervention_id,
            'average_latitude':     self.average_latitude,
            'average_longitude':    self.average_longitude,
            
        }
        
    def to_json_light(self):
        return {
            'id': self.id,
            'name':                 self.name,
            'formulaire_uuid':      self.formulaire_uuid,
            'formulaire_data':      self.formulaire_data,
            'formulaire_data_md5':  self.formulaire_data_md5,
            'intervention_id':      self.intervention_id,
            'average_latitude':     self.average_latitude,
            'average_longitude':    self.average_longitude,
        }


from sqlalchemy import event
@event.listens_for(Formulaire, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
