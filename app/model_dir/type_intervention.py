from .. import db
from .mymixin import MyMixin

from sqlalchemy.orm import declarative_base, relationship, backref
import uuid

class TypeInterventionSite(db.Model):
    __tablename__ = 'types_interventions_sites'
    
    type_intervention_id = db.Column(db.String(36), db.ForeignKey('types_interventions.id'), primary_key=True)
    site_id = db.Column(db.String(36), db.ForeignKey('sites.id'), primary_key=True)
    template_text=db.Column(db.Text)
    
    type_intervention   = relationship("TypeIntervention")
    site        = relationship("Site")
   
   
    def to_json(self):
        return {
            'type_intervention':            self.type_intervention.name,
            'site':                 self.site.name,
            'template_text':                     self.template_text,
        }
    
    def to_json_config(self):
        return {
            self.site.name: {
                self.type_intervention.name: self.template_text
            }
        }
        
    
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
        
    def to_name(self):
        print(self.name)
        return self.name;

   
    
    
from sqlalchemy import event
@event.listens_for(TypeIntervention, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
