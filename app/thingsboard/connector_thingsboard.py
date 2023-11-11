# Importing models and REST client class from Community Edition version
from tb_rest_client.rest_client_ce import *
# Importing the API exception
from tb_rest_client.rest import ApiException

import logging
import os
from sqlalchemy import inspect


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')



class Thingsboard():

    # ThingsBoard REST API URL
    url = "https://cloud.kysoe.com"

    # Default Tenant Administrator credentials
    username = "yannick.simon+sandbox@kysoe.com"
    password = "sandbox"


    def __init__(self):
        self.url = os.getenv('TB_URL')
        self.username = os.getenv('TB_TENANT_USER')
        self.password = os.getenv('TB_TENANT_PASSWORD')
        
        
    def createAsset(self, instance):
    
        
        asset_profile=instance.__class__.__name__
        asset_name=instance.__class__.__name__ + "_" + instance.id
        
        # Creating the REST client object with context manager to get auto token refresh
        with RestClientCE(base_url=self.url) as rest_client:
            try:
                # Auth with credentials
                rest_client.login(username=self.username, password=self.password)
            except ApiException as e:
                logging.exception(e)

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
                logging.exception(e)
            
            # est-ce que l'asset existe ?
            try:
                asset = rest_client.get_tenant_asset(asset_name)
                raise Exception("already exists")
            except ApiException as e:
                if (e.status==404):
                    asset=None
                else:
                    logging.exception(e.status)
             

            # non, alors je le créé  
            if asset is None:
                try:
                    default_asset_profile_id = rest_client.get_default_asset_profile_info().id
                    asset = Asset(name=asset_name, asset_profile_id=asset_profile.id)
                    asset = rest_client.save_asset(asset)
                    logging.info("Asset was created")
                    
                except ApiException as e:
                    logging.exception(e)
                    raise Exception(e)
            else:
                raise Exception("asset creation failed")

            dict_attributes={}
            mapper = inspect(instance)
            for column in mapper.attrs:
                dict_attributes[column.key]=column.value
        
            rest_client.save_entity_attributes_v2(asset.id, "SERVER_SCOPE", dict_attributes  )
            
            return asset
 

if __name__ == '__main__':
    tb=Thingsboard()
    x = tb.createAsset("profileB","assetC3")
    print(x)