from .. import db
from .mymixin import MyMixin

from sqlalchemy.orm import declarative_base, relationship, backref
import uuid


class Form(db.Model, MyMixin):
    __tablename__ = 'forms'
    
    form_on_site_uuid           = db.Column(db.String(36), unique=True)
    form_name                   = db.Column(db.String(255), index=True)
    form_order                  = db.Column(db.Integer, default=1)
    average_latitude            = db.Column(db.Float)
    average_longitude           = db.Column(db.Float)
    intervention_on_site_uuid   = db.Column(db.String(36))
    intervention_id             = db.Column(db.String(36), db.ForeignKey("interventions.id"))
    
    fields                      = relationship("Field",   
                                                cascade="all, delete", 
                                                backref=backref("form_backref",lazy="joined")                                        )
   
    sections                    =      relationship("Section")
    

    def to_json(self):
        return {
            'id':                             self.id,
            'name':                           self.name,
            '_internal' :                     self.get_internal(),
            'form_on_site_uuid':              self.form_on_site_uuid,
            'form_name':                      self.form_name,
            'form_order':                     self.form_order,
            'intervention_on_site_uuid':      self.intervention_on_site_uuid,
            'intervention_id':                self.intervention_id,
            'average_latitude':               self.average_latitude,
            'average_longitude':              self.average_longitude,
            'fields':  [{"field": item.to_json_light()} for item in self.fields] ,
            'sections':  [{"section": item.to_json_light()} for item in self.sections] ,
        }
        
    def to_json_light(self):
        return {
            'form_on_site_uuid':            self.form_on_site_uuid,
            'form_name':                    self.form_name,
            'form_order':                   self.form_order
        }
       


from sqlalchemy import event
@event.listens_for(Form, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
