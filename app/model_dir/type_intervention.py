from .. import db
from .mymixin import MyMixin

from sqlalchemy.orm import declarative_base, relationship, backref
import uuid

class TypeIntervention(db.Model, MyMixin):
    
    __tablename__ = 'types_interventions'
    
    type_intervention_uuid       = db.Column(db.String(36), unique=True, default=uuid.uuid4)
    
    interventions   = relationship("Intervention")
     
     
    def to_json(self):
        return {
            'id':                                self.id,
            'name':                              self.name,
            '_internal' :                        self.get_internal(),
            'type_intervention_uuid':            self.type_intervention_uuid,
            
           
        }
        
    def to_json_light(self):
        return {
            'id':                                self.id,
            'name':                              self.name,
            'type_intervention_uuid':            self.type_intervention_uuid,
        }
        
    def name(self):
        return self.name;

   
    
    
from sqlalchemy import event
@event.listens_for(TypeIntervention, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
