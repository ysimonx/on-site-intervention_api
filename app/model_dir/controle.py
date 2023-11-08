from .. import db
from .mymixin import MyMixin

from sqlalchemy.orm import declarative_base, relationship, backref
import uuid
import enum
from sqlalchemy import Enum


dict_controle = {
       0 : "à faire",   # "InterventionControleStatusEnum.non_saisi"
       1 : "en cours",  # "InterventionControleStatusEnum.en_cours
       2 : "accepté",   # "InterventionControleStatusEnum.accepte
       3 : "refusé",    # "InterventionControleStatusEnum.refuse
       4 : "à refaire",  # "InterventionControleStatusEnum.a_refaire
       5 : "non applicable"  # "InterventionControleStatusEnum.non_applicable
}

dict_controle_for_moe = {
        0 : "en attente de validation",   # "InterventionControleStatusEnum.non_saisi"
        1 : "en cours de validation",  # "InterventionControleStatusEnum.en_cours
        2 : "validé",   # "InterventionControleStatusEnum.accepte
        3 : "refusé",    # "InterventionControleStatusEnum.refuse
        4 : "en attente de revalidation",  # "InterventionControleStatusEnum.a_refaire
        5 : "non applicable"  # "InterventionControleStatusEnum.non_applicable
}

dict_EnumInverse = {
    0: "non_saisi",
    1: "en_cours",
    2: "accepte", 
    3: "refuse",
    4: "a_refaire",
    5: "non_applicable"
}

class InterventionControleStatusEnum(enum.Enum):
    non_saisi = 0
    en_cours = 1
    accepte = 2
    refuse = 3
    a_refaire = 4
    non_applicable = 5
   

class Controle(db.Model, MyMixin):
    __tablename__ = 'controle'
    
    intervention_uuid = db.Column(db.String(255), db.ForeignKey("interventions.intervention_uuid"))
    controle_status = db.Column( Enum(InterventionControleStatusEnum), default=InterventionControleStatusEnum.non_saisi)
    adresse = db.Column(db.String(255))             # ex: 215 ancien chemin de peynier  
    zip     = db.Column(db.String(6))               # ex: 13530
    ville   = db.Column(db.String(255))             # ex: TRETS
    numero_fiscal_local = db.Column(db.String(255)) # ex: 131100492373 
    surface_m2 = db.Column(db.Integer);             # ex: 133
    attendus = db.Column(db.Text())
    commentaires = db.Column(db.Text())
    
    
    def to_json(self):
        return {
            'id': self.id,
            '_internal' : self.get_internal(),
            'intervention_uuid': self.intervention_uuid,
            'controle_status': dict_controle_for_moe[self.controle_status.value],
            'adresse': self.adresse,
            'zip': self.zip,
            'ville': self.ville,
            'numero_fiscal_local': self.numero_fiscal_local,
            'surface_m2': self.surface_m2,
            'attendus': self.attendus,
            'commentaires': "" if self.commentaires == "None" else self.commentaires
            
        }
        
    def to_json_light(self):
        return {
            'id': self.id,
            'intervention_uuid': self.intervention_uuid,
            'controle_status': dict_controle_for_moe[self.controle_status.value],
            'adresse': self.adresse,
            'zip': self.zip,
            'ville': self.ville,
            'numero_fiscal_local': self.numero_fiscal_local,
            'surface_m2': self.surface_m2,
            'attendus': self.attendus,
            'commentaires': "" if self.commentaires == "None" else self.commentaires
        }


from sqlalchemy import event
@event.listens_for(Controle, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
