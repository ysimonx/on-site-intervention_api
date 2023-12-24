from .. import db
from .mymixin import MyMixin

from sqlalchemy.orm import declarative_base, relationship, backref
import uuid

class Intervention(db.Model, MyMixin):
    
    __tablename__ = 'interventions'
    
    intervention_on_site_uuid   = db.Column(db.String(36), index=True)
    
    organization_id  = db.Column(db.String(36), db.ForeignKey("organizations.id"))
    

    place_id                    = db.Column(db.String(36), db.ForeignKey("places.id"));
    type_intervention_id        = db.Column(db.String(36), db.ForeignKey("types_interventions.id"));
    
    place                       = relationship("Place",                    viewonly=True, back_populates="interventions")
    type_intervention           = relationship("TypeIntervention",         viewonly=True, back_populates="interventions")
    forms                       = relationship("Form")
    
    
    def to_json(self):
        return {
            'id':                           self.id,
            'name':                         self.name,
            '_internal' :                   self.get_internal(),
            'intervention_on_site_uuid':    self.intervention_on_site_uuid,
            'organization_id':               self.organization_id,
            'place':                        self.place.to_json_light(),
            'forms':  [{"forms": item.to_json_light()} for item in self.forms],    
        }
        
    def to_json_light(self):
        return {
            'id':                       self.id,
            'name':                     self.name,
            'intervention_on_site_uuid':    self.intervention_on_site_uuid,
            'organization_id':               self.organization_id,
            'place_id':                 self.place_id,
            'place':                    self.place.to_json_light(),
        }

   
    
    
from sqlalchemy import event
@event.listens_for(Intervention, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
