from .. import db
from .mymixin import MyMixin

from sqlalchemy.orm import declarative_base, relationship, backref
import uuid

class Section(db.Model, MyMixin):
    
    __tablename__ = 'sections'
    
    
    section_on_site_uuid   = db.Column(db.String(36), index=True)
    section_type           = db.Column(db.String(100), index=True)
    section_name           = db.Column(db.String(100), index=True)
    form_on_site_uuid      = db.Column(db.String(36),  index=True)
    form_id                = db.Column(db.String(36),  db.ForeignKey("forms.id"), nullable=True)
    intervention_id        = db.Column(db.String(36),  db.ForeignKey("interventions.id"), nullable=True)
    
    section_order_in_form  = db.Column(db.Integer, default=1)
    
    fields                 = relationship("Field")
                                                                                     
   
    
    def to_json(self):
        dict_fields={}
        for field in self.fields:
            dict_fields[field.field_order_in_section]= field.to_json_light()
        return {
            'id':                           self.id,
            'section_name':                 self.section_name,
            'section_type':                 self.section_type ,
            '_internal' :                   self.get_internal(),
            'fields': dict_fields,   
            
        }
        
    def to_json_light(self):
        return {
            'id':                       self.id,
             'section_name':                 self.section_name,
            '_internal' :                   self.get_internal(),
        }

   
    
    
from sqlalchemy import event
@event.listens_for(Section, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
