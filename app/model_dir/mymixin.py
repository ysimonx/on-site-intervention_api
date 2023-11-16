from .. import db

from sqlalchemy import event
from sqlalchemy.orm import declarative_base, relationship, declared_attr
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, verify_jwt_in_request
import uuid
from datetime import date, datetime
from sqlalchemy import inspect

def formatted_date_iso(date):
    if date is None:
        return None
    return date.isoformat()
    

class MyMixin(object):
    id              = db.Column(db.String(36), primary_key=True, default=uuid.uuid4)
    name            = db.Column(db.String(255), index=True)

    time_created    = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    time_updated    = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    owner_user_id   = db.Column(db.String(36), nullable=True, index=True, default="")
    
    
    def map_owner(mapper, connect, target):
        verify_jwt_in_request(optional=True)
        current_user = get_jwt_identity()
        if (not current_user is None):
            target.owner_user_id = current_user
            
    def get_internal(self):

        
        return {
                
                'time_created_utc': formatted_date_iso(self.time_created),
                'time_updated_utc': formatted_date_iso(self.time_updated),
                'owner_user_id':    self.owner_user_id
            }
        
        
    def get_attributes_for_thingsboard(self):
        
        dict_attributes={}
        mapper = inspect(self)
        for column in mapper.attrs:
            dict_attributes[column.key]=column.value
        return dict_attributes
        
        
        
@event.listens_for(MyMixin, 'before_insert')
def do_stuff(mapper, connect, target):

    verify_jwt_in_request(optional=True)
    current_user = get_jwt_identity()
    if (not current_user is None):
        target.owner_user_id = current_user
    