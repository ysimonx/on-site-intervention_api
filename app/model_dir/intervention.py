from .. import db
from .mymixin import MyMixin
import json
from sqlalchemy.orm import declarative_base, relationship, backref
import uuid

class Intervention(db.Model, MyMixin):
    
    __tablename__ = 'interventions'
    
    intervention_on_site_uuid   = db.Column(db.String(36), index=True)
    type_intervention_id        = db.Column(db.String(36), db.ForeignKey("types_interventions.id"));
    type_intervention           = relationship("TypeIntervention",         viewonly=True)
    forms                       = relationship("Form")
    
    
    def to_json(self):
        dict_forms={}
        for form in self.forms:
            dict_forms[form.form_order]= form.to_json_light()
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
    
    # id : identifiant qui provient de la classe MyMixin
    
    # identifiant "local" au device dans lequel l'intervention est créée 
    intervention_values_on_site_uuid = db.Column(db.String(36), index=True, unique=True)
    
    # identifiant de l'emplacement de l'intervention
    place_id                    = db.Column(db.String(36), db.ForeignKey("places.id"));
    
    # version des données enregistrées pour cette invention
    version                     = db.Column(db.Integer, default=1)
    
    # site industriel auquel l'intervention est rattachée
    site_id                     = db.Column(db.String(36), db.ForeignKey("sites.id"))
    
    # type de l'intervention (scaffolding request, calo, etc ...)
    type_intervention_id        = db.Column(db.String(36), db.ForeignKey("types_interventions.id"));
    
    # a qui est assignée l'intervention (parmi les coordinateurs)
    assignee_user_id            = db.Column(db.String(36), db.ForeignKey("users.id"))
    
    # compteur de creation de l'intervention (#1, #2, #3, etc ... par site industriel)
    hashtag                     = db.Column(db.Integer, default=1, index=True)
    
    # 
    # template_text             = db.Column(db.Text)
    
    # status (workflow) de l'intervention
    status                      = db.Column(db.String(50), index=True, nullable=True)
    
    place                       = db.relationship("Place", viewonly=True)
    type_intervention           = db.relationship("TypeIntervention", viewonly=True)
    site                        = db.relationship("Site", viewonly=True)
    assignee_user               = db.relationship("User", viewonly=True)
    fields_values               = db.relationship("FieldValue", viewonly=True)
    
    def to_json(self):
        dict_field_values={}
        for item in self.fields_values:
            dict_field_values[item.field_on_site_uuid]=item.value;
        
        return {
            'id':                             self.id,
            'intervention_name':              self.name,
            '_internal' :                     self.get_internal(),
            'intervention_values_on_site_uuid':                self.intervention_values_on_site_uuid,
            'site':                           self.site.to_json(),
            'type_intervention':              self.type_intervention.to_json(),
            'place':                          self.place.to_json(),
            'version':                        self.version, 
            'hashtag':                        self.hashtag,
            'assignee_user_id':             self.assignee_user_id,
            'assignee_user':                None if self.assignee_user is None else self.assignee_user.to_json_ultra_light(),
            # 'template_text':                  self.template_text,
            'field_on_site_uuid_values':      dict_field_values,
            'status':                         self.status
        }
    
    def photos_to_json(self):
        photos_total=[]
        for item in self.fields_values:
            if item.field.field_type == "gallery":
                if item.value is not None:
                    try:
                        photos=json.loads(item.value)    
                    except:
                        photos=[]
                    for photo in photos:
                             photos_total.append(photo);
                            
        return {
            'site_id':                        self.site.id,
            'photos':        photos_total
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
            'site_id':                self.site_id,
            'place_id':                       self.place_id,
            'place_name':                     self.place.name,
            'version':                        self.version,
            'site_name':              self.site.name,
            'type_intervention_name':         self.type_intervention.name,
            'hashtag':                        self.hashtag,
            'assignee_user_id':             self.assignee_user_id,
            'assignee_user':                None if self.assignee_user is None else self.assignee_user.to_json_ultra_light(),
            'field_on_site_uuid_values':      dict_field_values,
            'status':                         self.status
        }
       


from sqlalchemy import event
@event.listens_for(InterventionValues, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    


    
    
from sqlalchemy import event
@event.listens_for(Intervention, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
     
    
