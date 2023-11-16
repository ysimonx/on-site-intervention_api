from .. import db

from .mymixin import MyMixin

class Event(db.Model, MyMixin):
    __tablename__ = 'events'

    event_on_site_uuid          = db.Column(db.String(36), unique=True)
    
    def to_json(self):
        return {
            'id':                           self.id,
            '_internal' :                   self.get_internal(),
            'event_on_site_uuid':           self.event_on_site_uuid,
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
    
