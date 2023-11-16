from .. import db

from .mymixin import MyMixin

class Notification(db.Model, MyMixin):
    __tablename__ = 'notifications'

    notification_on_site_uuid          = db.Column(db.String(36), unique=True)
    
    def to_json(self):
        return {
            'id':                           self.id,
            '_internal' :                   self.get_internal(),
            'notification_on_site_uuid':           self.notification_on_site_uuid,
        }
        
    def to_json_light(self):
        return {
            'id':                           self.id,
            '_internal' :                   self.get_internal(),
        }

from sqlalchemy import event
@event.listens_for(Notification, 'before_insert')
def do_stuff1(mapper, connect, target):
    MyMixin.map_owner(mapper, connect, target)
    
