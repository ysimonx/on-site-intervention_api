from .. import db
from .mymixin import MyMixin

from sqlalchemy.orm import declarative_base, relationship, backref
import uuid

class TypeField(db.Model, MyMixin):
    
    __tablename__ = 'types_fields'
    
    type_field_uuid       = db.Column(db.String(255), unique=True)
    
    fields   = relationship("Field")
     
    fields                      = relationship("Field",   
                                                cascade="all, delete", 
                                                backref=backref("type_field_backref",lazy="joined")
                                            )
   
   
    def to_json(self):
        return {
            'id':                                self.id,
            'name':                              self.name,
            '_internal' :                        self.get_internal(),
            'type_field_uuid':            self.type_field_uuid,
        }
        
    def to_json_light(self):
        return {
            'id':                                self.id,
            'name':                              self.name,
            '_internal' :                        self.get_internal(),
            'type_field_uuid':            self.type_field_uuid,
        }

   
    
    
from sqlalchemy import event
@event.listens_for(TypeField, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
