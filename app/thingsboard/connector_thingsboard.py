# Importing models and REST client class from Community Edition version
from tb_rest_client.rest_client_ce import *
# Importing the API exception
from tb_rest_client.rest import ApiException

from flask import current_app



import os
from sqlalchemy import inspect



class ThingsboardConnector():

    # ThingsBoard REST API URL
    url = "https://cloud.kysoe.com"

    # Default Tenant Administrator credentials
    username = "yannick.simon+sandbox@kysoe.com"
    password = "sandbox"

    def __init__(self):
        self.url = os.getenv('TB_URL')
        self.username = os.getenv('TB_TENANT_USER')
        self.password = os.getenv('TB_TENANT_PASSWORD')
        
        
    def linkAssets(self, instanceFrom: Any, instanceTo: Any):
        
        asset_name_from  = instanceFrom.__class__.__name__ + "_" + instanceFrom.id
        asset_name_to    = instanceTo.__class__.__name__ + "_" + instanceTo.id
        
        # Creating the REST client object with context manager to get auto token refresh
        with RestClientCE(base_url=self.url) as rest_client:
            try:
                # Auth with credentials
                rest_client.login(username=self.username, password=self.password)
            except ApiException as e:
                current_app.logger.exception(e.reason)
                return

            try:   
                asset_from = rest_client.get_tenant_asset(asset_name_from)
                asset_to = rest_client.get_tenant_asset(asset_name_to)
                
               
                # Creating relations from device to asset
                relation = EntityRelation(_from=asset_from.id, to=asset_to.id, type="Contains")
                rest_client.save_relation(relation)
            
            except ApiException as e:
                current_app.logger.exception(e.reason)
     
     
    def saveAttribute(self, instance:Any, dict_attributes: Any):
        asset_name=instance.__class__.__name__ + "_" + instance.id
        
        # Creating the REST client object with context manager to get auto token refresh
        with RestClientCE(base_url=self.url) as rest_client:
            try:
                # Auth with credentials
                rest_client.login(username=self.username, password=self.password)
            except ApiException as e:
                current_app.logger.exception(e.reason)
                
            try:
                asset = rest_client.get_tenant_asset(asset_name)
            except ApiException as e:
                if (e.status==404):
                    asset=None
                else:
                    current_app.logger.exception(e.reason)
                    
            # 
            if asset is not None:
                rest_client.save_entity_attributes_v2(asset.id, "SERVER_SCOPE", dict_attributes  )
            

         

    def createAsset(self, instance: Any):
    
        
        asset_profile=instance.__class__.__name__
        asset_name=instance.__class__.__name__ + "_" + instance.id
        
        # Creating the REST client object with context manager to get auto token refresh
        with RestClientCE(base_url=self.url) as rest_client:
            try:
                # Auth with credentials
                rest_client.login(username=self.username, password=self.password)
            except ApiException as e:
                current_app.logger.exception(e.reason)
          
         
            # est-ce que le profile existe ?
            try:        
                # recherche sur le nom du profile d'asset
                asset_profile_list = rest_client.get_asset_profile_infos(page_size=1, page=0, text_search=asset_profile, sort_property=None, sort_order=None)
                if (len(asset_profile_list.data) == 0):
                    asset_profile = AssetProfile(name=asset_profile)
                    asset_profile = rest_client.save_asset_profile(asset_profile)
                else:
                    asset_profile = asset_profile_list.data[0] 
            except ApiException as e:
                current_app.logger.exception(e.reason)
                
            # est-ce que l'asset existe ?
            try:
                asset = rest_client.get_tenant_asset(asset_name)
                raise Exception("already exists")
            except ApiException as e:
                if (e.status==404):
                    asset=None
                else:
                    current_app.logger.exception(e.reason)

             

            # non, alors je le créé  
            if asset is None:
                try:
                    default_asset_profile_id = rest_client.get_default_asset_profile_info().id
                    asset = Asset(name=asset_name, asset_profile_id=asset_profile.id)
                    asset = rest_client.save_asset(asset)
                    current_app.logger.info("Asset was created")

                except ApiException as e:
                    current_app.logger.exception(e.reason)
                    raise Exception(e)
            else:
                raise Exception("asset creation failed")

            dict_attributes=instance.get_attributes_for_thingsboard()
            
            rest_client.save_entity_attributes_v2(asset.id, "SERVER_SCOPE", dict_attributes  )
            
            return asset
 

if __name__ == '__main__':
    tb=ThingsboardConnector()
    x = tb.createAsset("profileB","assetC3")
    print(x)