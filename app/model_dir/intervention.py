from .. import db, getByIdOrByName
from ..model_dir.site import Site
from ..model_dir.type_intervention import TypeIntervention, TypeInterventionSite
from .mymixin import MyMixin, User
import json
from sqlalchemy.orm import declarative_base, relationship, backref
import uuid
from flask import request, url_for, current_app

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
    
    # numero de chrono de ce type d'intervention et pour ce site
    # note : toutes les interventions qui ont le meme numero de chrono regroupent
    # la meme intervention, qui evolue au fil de l'eau et dont l'évolution est suivie
    # par l'indice 
    num_chrono                  = db.Column(db.Integer, index=True)
    
    # indice de cette intervention (en cas de reprise/continuité d'une intervention qui aurait le meme numero de chrono)
    # limitée à 2 lettres a-b-c-d-e ... z ... -aa-ab-ac-ad ....
    indice                      = db.Column(db.String(2))
    
    average_latitude            = db.Column(db.Float);
    average_longitude           = db.Column(db.Float);
    
   
    # 
    
    # status (workflow) de l'intervention
    status                      = db.Column(db.String(50), index=True, nullable=True)
    
    dict_of_custom_fields_values  = db.Column(db.Text)
     
    place                       = db.relationship("Place", viewonly=True)
    type_intervention           = db.relationship("TypeIntervention", viewonly=True)
    site                        = db.relationship("Site", viewonly=True)
    assignee_user               = db.relationship("User", viewonly=True)
    fields_values               = db.relationship("FieldValue", viewonly=True)
    
    def to_dict(self):
        host="https://{}".format(request.headers.get('X-Forwarded-Host'))
        
        data={
            "id":self.id,
            "feb_url":"{}{}".format(host, url_for('backoffice.get_interventions_values_id', id=self.id)),
            "site":self.site.name, 
            "type_intervention":self.type_intervention.name,
            "status":self.status,
            "assignee_email": self.assignee_user.email if self.assignee_user is not None else None,
            "registre" :self.name,
            "place": self.place.name,
            "num_chrono":self.num_chrono,
            "indice":self.indice,
           
        }
        columns=["id","feb_url", "site","type_intervention", "assignee_email", "registre", "place", "num_chrono", "indice", ] 
         
        dict_field_values={}
        for item in self.fields_values:
            dict_field_values[item.field_on_site_uuid]=item.value;
            
        site_id=self.site_id
        _site=getByIdOrByName(Site, site_id)
        
        type_intervention_id=site_id=self.type_intervention_id
        _type_intervention=getByIdOrByName(TypeIntervention, type_intervention_id)

        _type_intervention_site = TypeInterventionSite.query.get((_type_intervention.id,_site.id))
        
        
        dictTemplate=json.loads(_type_intervention_site.template_text)
        for form, form_values in dictTemplate["forms"].items():
            for section, section_values in form_values["sections"].items():
                for field, fields_values in section_values["fields"].items():
                    field_name=fields_values["field_name"]
                    
                    columns.append(field_name)
                    if fields_values["field_type"]=="user_from_role":
                        columns.append("{}.company".format(field_name))
                        columns.append("{}.firstname".format(field_name))
                        columns.append("{}.lastname".format(field_name))
                        columns.append("{}.phone".format(field_name))
                        columns.append("{}.email".format(field_name))
                    field_on_site_uuid=fields_values["field_on_site_uuid"]
                    if field_on_site_uuid in dict_field_values.keys():
                        value  = dict_field_values[field_on_site_uuid]
                        value = value.replace('\r', '')
                        value = value.replace('\n', ' - ')
                        data[field_name] = value
                        if fields_values["field_type"]=="user_from_role":
                            if value != "":
                                _user = getByIdOrByName(obj=User, id=value)
                                if _user is not None:
                                    data["{}.company".format(field_name)]=_user.company.name
                                    
                                    data["{}.firstname".format(field_name)]=_user.firstname
                                    data["{}.lastname".format(field_name)]=_user.lastname
                                    data["{}.phone".format(field_name)]=str(_user.phone)
                                    data["{}.email".format(field_name)]=_user.email
                    else:
                        data[field_name] = None
        result={
            "columns": columns,
            "data": data
        }
        
        return result       
        
        
    def to_json(self):
        dict_field_values={}
        for item in self.fields_values:
            dict_field_values[item.field_on_site_uuid]=item.value;
        
        json_custom_fields_values = self.dict_of_custom_fields_values
        if json_custom_fields_values is None:
            json_custom_fields_values = {}
        else:
            json_custom_fields_values= json.loads(self.dict_of_custom_fields_values)
            
        return {
            'id':                             self.id,
            'intervention_name':              self.name,
            '_internal' :                     self.get_internal(),
            'intervention_values_on_site_uuid':                self.intervention_values_on_site_uuid,
            'site':                           self.site.to_json_light(),
            'type_intervention':              self.type_intervention.to_json(),
            'place':                          self.place.to_json(),
            'version':                        self.version, 
            'hashtag':                        self.hashtag,
            'assignee_user_id':                 self.assignee_user_id,
            'assignee_user':                None if self.assignee_user is None else self.assignee_user.to_json_ultra_light(),
            'field_on_site_uuid_values':      dict_field_values,
            'status':                         self.status,
            'num_chrono':                       self.num_chrono,
            'indice':                           self.indice,
            'average_latitude' :                self.average_latitude,
            'average_longitude' :               self.average_longitude,
            'custom_fields_values':             json_custom_fields_values
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
            'site_id':       self.site.id,
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
            'status':                         self.status,
            'num_chrono':                       self.num_chrono,
            'indice':                           self.indice,
            'custom_fields_values':             json.loads(self.dict_of_custom_fields_values)
        }
       


from sqlalchemy import event
@event.listens_for(InterventionValues, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    


    
    
from sqlalchemy import event
@event.listens_for(Intervention, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
     
    
