from .. import db
from .mymixin import MyMixin

from sqlalchemy.orm import declarative_base, relationship, backref
import uuid
import json
import enum
from sqlalchemy import Enum

dict_controle_field = {
       0 : "non_saisi",  
       1 : "satisfaisant",  
       2 : "non_satisfaisant",  
       3 : "non_verifiable",  
       4 : "non_applicable" 
}

dict_controle_field_for_export = {
       0 : "NO",  
       1 : "SA",  
       2 : "NS",  
       3 : "NV",  
       4 : "NA" 
}


class ControleStatusEnum(enum.Enum):
    non_saisi = 0
    satisfaisant = 1
    non_satisfaisant = 2
    non_verifiable = 3
    non_applicable = 4


class FieldHisto(db.Model, MyMixin):
    __tablename__ = 'fields_histo'
    
    field_uuid= db.Column(db.String(255),index=True)
    field_data = db.Column(db.Text())
    field_data_md5 = db.Column(db.String(32), index=True)
    intervention_uuid = db.Column(db.String(255), db.ForeignKey("interventions.intervention_uuid"))
    average_latitude= db.Column(db.Float)
    average_longitude= db.Column(db.Float)
    formulaire_id  = db.Column(db.String(36), db.ForeignKey("formulaires.id"))
    controle_status = db.Column( Enum(ControleStatusEnum), default=ControleStatusEnum.non_saisi)
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            '_internal' : self.get_internal(),
            'field_uuid': self.field_uuid,
            'field_data': json.loads(self.field_data),
            'field_data_md5': self.field_data_md5,
            'formulaire_id': self.formulaire_id,
            'average_latitude': self.average_latitude,
            'average_longitude': self.average_longitude,
            'intervention_uuid': self.intervention_uuid,
            'controle_status': self.controle_status
            
        }
        
    def to_json_light(self):
        return {
            'id': self.id,
            'name': self.name,
            'field_uuid': self.field_uuid,
            'field_data': json.loads(self.field_data),
            'field_data_md5': self.field_data_md5,
            'formulaire_id': self.formulaire_id,
            'average_latitude': self.average_latitude,
            'average_longitude': self.average_longitude,
            'intervention_uuid': self.intervention_uuid,
            'controle_status': self.controle_status.value
        }


from sqlalchemy import event
@event.listens_for(FieldHisto, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
