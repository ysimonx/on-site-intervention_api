from .. import db
from .mymixin import MyMixin

from sqlalchemy.orm import declarative_base, relationship, backref
import uuid


class FormTemplate(db.Model, MyMixin):
    __tablename__ = 'forms_templates'
    
    form_template_on_site_uuid              = db.Column(db.String(36), unique=True)
    
    def to_json(self):
        return {
            'id':                             self.id,
            'name':                           self.name,
            '_internal' :                     self.get_internal(),
            'form_template_on_site_uuid':   self.form_template_on_site_uuid
            
        }
        
    def to_json_light(self):
        return {
            'id':                             self.id,
            'name':                           self.name,
            '_internal' :                     self.get_internal(),
            'form_template_on_site_uuid':       self.form_template_on_site_uuid
        }
       


from sqlalchemy import event
@event.listens_for(FormTemplate, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
