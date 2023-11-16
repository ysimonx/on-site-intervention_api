from .. import db
from .mymixin import MyMixin

from sqlalchemy.orm import declarative_base, relationship, backref
import uuid

class Intervention(db.Model, MyMixin):
    
    __tablename__ = 'interventions'
    
    intervention_on_site_uuid = db.Column(db.String(255), index=True)
    intervention_data_md5   = db.Column(db.String(32))
    average_latitude        = db.Column(db.Float);
    average_longitude       = db.Column(db.Float);
    place_id                = db.Column(db.String(36), db.ForeignKey("places.id"));
    type_intervention_id    = db.Column(db.String(36), db.ForeignKey("types_interventions.id"));
    
    place                   = relationship("Place",                    viewonly=True, back_populates="interventions")
    type_intervention       = relationship("TypeIntervention",         viewonly=True, back_populates="interventions")
    reports                 = relationship("Report")
    
    
    def to_json(self):
        return {
            'id':                           self.id,
            'name':                         self.name,
            '_internal' :                   self.get_internal(),
            'intervention_on_site_uuid':    self.intervention_on_site_uuid,
            'intervention_data_md5':        self.intervention_data_md5,
            'place':                        self.place.to_json_light(),
            'average_latitude':             self.average_latitude,
            'average_longitude':            self.average_longitude,
            'reports':  [{"reports": item.to_json_light()} for item in self.reports],    
        }
        
    def to_json_light(self):
        return {
            'id':                       self.id,
            'name':                     self.name,
            'place_id':                 self.place_id,
            'intervention_data_md5':    self.intervention_data_md5,
            'place':                    self.place.to_json_light(),
            'average_latitude':         self.average_latitude,
            'average_longitude':        self.average_longitude,
            
        }

   
    
    
from sqlalchemy import event
@event.listens_for(Intervention, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
