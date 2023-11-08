from .. import db
from .mymixin import MyMixin

from sqlalchemy.orm import declarative_base, relationship, backref
import uuid


class Intervention(db.Model, MyMixin):
    __tablename__ = 'interventions'
    
    intervention_uuid= db.Column(db.String(255), unique=True)
    intervention_name = db.Column(db.String(255))
    intervention_data_md5 = db.Column(db.String(32))
    average_latitude= db.Column(db.Float);
    average_longitude= db.Column(db.Float);
    place_id  = db.Column(db.String(36), db.ForeignKey("places.id"));
    
    place         = relationship("Place", viewonly=True, back_populates="interventions")
    
    controles            = relationship("Controle", backref=backref("controles",lazy="joined"))
    
    formulaires   = relationship("Formulaire",   
                                cascade="all, delete", 
                                backref=backref("formulaires",lazy="joined")
                                )
    
    fields = relationship("Field",   
                                cascade="all, delete", 
                                backref=backref("fields",lazy="joined")
                                )
    
    fields_histo = relationship("FieldHisto",   
                                cascade="all, delete", 
                                backref=backref("fields_histo",lazy="joined")
                                )
    
    
    def to_json(self):
        return {
            'id': self.id,
            '_internal' : self.get_internal(),
            'intervention_uuid': self.intervention_uuid,
            'intervention_name': self.intervention_name,
            'intervention_data_md5': self.intervention_data_md5,
            'place': self.place.to_json_light(),
            'average_latitude': self.average_latitude,
            'average_longitude': self.average_longitude,
            'formulaires':  [{"formulaire": item.to_json_light()} for item in self.formulaires],    
            'controles':  [{"controle": item.to_json_light()} for item in self.controles],   
            'fields':  [{"field": item.to_json_light()} for item in self.fields],
            'fields_histo':  [{"field": item.to_json_light()} for item in self.fields_histo],  
        }
        
    def to_json_light(self):
        return {
            'id': self.id,
            'place_id': self.place_id,
            'intervention_name': self.intervention_name,
            'intervention_data_md5': self.intervention_data_md5,
            'place': self.place.to_json_light(),
            'average_latitude': self.average_latitude,
            'average_longitude': self.average_longitude,
            'controles':  [{"controle": item.to_json_light()} for item in self.controles],   
        }

   
    
    
from sqlalchemy import event
@event.listens_for(Intervention, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
