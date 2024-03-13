from .. import db

from .mymixin import MyMixin

class Event(db.Model, MyMixin):
    __tablename__ = 'events'

    object                      = db.Column(db.String(255), index=True, nullable=False)
    object_id                   = db.Column(db.String(36),  index=True, nullable=False)
    action                      = db.Column(db.String(255), index=True, nullable=False)
    value_before                = db.Column(db.String(255), nullable=True)
    value_after                 = db.Column(db.String(255), nullable=True)
    description                 = db.Column(db.String(255), index=True, nullable=True)
    datetime_notification_sent  = db.Column(db.DateTime(timezone=True), nullable=True)
    datetime_notification_read  = db.Column(db.DateTime(timezone=True), nullable=True)
   
    def to_json(self):
        return {
            'id':                           self.id,
            '_internal' :                   self.get_internal(),
            'object':                       self.object,
            'object_id':                    self.object_id,
            'action':                       self.action,   
            'value_before':                       self.value_before,
            'value_after':                       self.value_after,
            'description':                       self.description
            
        }
        
    def to_json_light(self):
        return {
            'id':                           self.id,
            '_internal' :                   self.get_internal(),
        }

from sqlalchemy import event
@event.listens_for(Event, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
