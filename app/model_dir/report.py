from .. import db
from .mymixin import MyMixin

from sqlalchemy.orm import declarative_base, relationship, backref
import uuid


class Report(db.Model, MyMixin):
    __tablename__ = 'reports'
    
    report_on_site_uuid         = db.Column(db.String(255), unique=True)
    report_name                 = db.Column(db.String(255), index=True)
    average_latitude            = db.Column(db.Float)
    average_longitude           = db.Column(db.Float)
    intervention_on_site_uuid   = db.Column(db.String(36))
    intervention_id             = db.Column(db.String(36), db.ForeignKey("interventions.id"))
    
    fields                      = relationship("Field",   
                                                cascade="all, delete", 
                                                backref=backref("reports",lazy="joined")
                                            )
   

    def to_json(self):
        return {
            'id':                             self.id,
            'name':                           self.name,
            '_internal' :                     self.get_internal(),
            'report_on_site_uuid':            self.report_on_site_uuid,
            'report_name':                    self.report_name,
            'intervention_on_site_uuid':      self.intervention_on_site_uuid,
            'intervention_id':                self.intervention_id,
            'average_latitude':               self.average_latitude,
            'average_longitude':              self.average_longitude,
            
        }
        
    def to_json_light(self):
        return {
            'id':                             self.id,
            'name':                           self.name,
            '_internal' :                     self.get_internal(),
            'report_on_site_uuid':            self.report_on_site_uuid,
            'report_name':                    self.report_name,
            'intervention_on_site_uuid':      self.intervention_on_site_uuid,
            'intervention_id':                self.intervention_id,
            'average_latitude':               self.average_latitude,
            'average_longitude':              self.average_longitude,
        }
        
    def get_attributes_for_thingsboard(self):
        dict_attributes=super().get_attributes_for_thingsboard()
        # remove relationships
        del dict_attributes["fields"]
        return dict_attributes
        


from sqlalchemy import event
@event.listens_for(Report, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
