from .. import db
from .mymixin import MyMixin

from sqlalchemy.orm import declarative_base, relationship, backref
import uuid

class Intervention(db.Model, MyMixin):
    
    __tablename__ = 'interventions'
    
    intervention_on_site_uuid   = db.Column(db.String(36), index=True)
    type_intervention_id        = db.Column(db.String(36), db.ForeignKey("types_interventions.id"));
    type_intervention           = relationship("TypeIntervention",         viewonly=True)
    forms                       = relationship("Form")
    
    
    def to_json(self):
        # print(self.forms)
        dict_forms={}
        for form in self.forms:
            dict_forms[form.form_order]= form.to_json_light()
        print(dict_forms)
        return {
            'id':                           self.id,
            'intervention_name':            self.name,
            '_internal' :                   self.get_internal(),
            'intervention_on_site_uuid':    self.intervention_on_site_uuid,
            'forms': dict_forms,   
            'type_intervention':            self.type_intervention.to_name()
        }
        
    def to_json_light(self):
        return {
            'id':                           self.id,
            'intervention_name':            self.name,
            'intervention_on_site_uuid':    self.intervention_on_site_uuid,
            'type_intervention':            self.type_intervention.to_name()
        }

   

class InterventionValues(db.Model, MyMixin):
    __tablename__ = 'interventions_values'
    
    intervention_values_on_site_uuid = db.Column(db.String(36), index=True)
    place_id                    = db.Column(db.String(36), db.ForeignKey("places.id"));
    version                     = db.Column(db.Integer, default=1)
    
    organization_id             = db.Column(db.String(36), db.ForeignKey("organizations.id"))
    type_intervention_id        = db.Column(db.String(36), db.ForeignKey("types_interventions.id"));
    supervisor_user_id          = db.Column(db.String(36), db.ForeignKey("users.id"))
    hashtag                     = db.Column(db.Integer, default=1, index=True)
    
    place                       = db.relationship("Place", viewonly=True)
    type_intervention           = db.relationship("TypeIntervention", viewonly=True)
    organization                = db.relationship("Organization", viewonly=True)
    supervisor_user             = db.relationship("User", viewonly=True)
    
    template_text               = db.Column(db.Text)
    fields_values               = db.relationship("FieldValues", viewonly=True)
    
    def to_json(self):
        dict_field_values={}
        for item in self.fields_values:
            
            dict_field_values[item.field_on_site_uuid]=item.value;
            
        
        return {
            'id':                             self.id,
            'intervention_name':              self.name,
            '_internal' :                     self.get_internal(),
            'intervention_values_on_site_uuid':                self.intervention_values_on_site_uuid,
            'organization':                   self.organization.to_json(),
            'type_intervention':                   self.type_intervention.to_json(),
            'place':                          self.place.to_json(),
            'version':                        self.version, 
            'hashtag':                        self.hashtag,
            'supervisor_user_id':             self.supervisor_user_id,
            'supervisor_user':                None if self.supervisor_user is None else self.supervisor_user.to_json_ultra_light(),
            'template_text':                  self.template_text,
            'field_on_site_uuid_values':                  dict_field_values
        }
        
    def to_json_light(self):
      dict_field_values={}
      for item in self.fields_values:
            
            dict_field_values[item.field_on_site_uuid]=item.value;
            
            
      return {
            'id':                             self.id,
            'intervention_name':              self.name,
            'intervention_values_on_site_uuid':                self.intervention_values_on_site_uuid,
            'type_intervention_id':           self.type_intervention_id,
            'organization_id':                self.organization_id,
            'place_id':                       self.place_id,
            'place_name':                     self.place.name,
            'version':                        self.version,
            'organization_name':              self.organization.name,
            'type_intervention_name':         self.type_intervention.name,
            'hashtag':                        self.hashtag,
            'supervisor_user_id':             self.supervisor_user_id,
            'supervisor_user':                None if self.supervisor_user is None else self.supervisor_user.to_json_ultra_light(),
            'template_text':                    self.template_text,
            'field_on_site_uuid_values':                  dict_field_values
        }
       


from sqlalchemy import event
@event.listens_for(InterventionValues, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    


    
    
from sqlalchemy import event
@event.listens_for(Intervention, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
     
    
