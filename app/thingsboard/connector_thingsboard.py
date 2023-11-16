# Importing models and REST client class from Community Edition version
from tb_rest_client.rest_client_ce import *
# Importing the API exception
from tb_rest_client.rest import ApiException

from flask import current_app
from sqlalchemy.orm.interfaces import *

from types import NoneType
import datetime

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
        
        self.rest_client= RestClientCE(base_url=self.url)
            
        try:
                # Auth with credentials
                self.rest_client.login(username=self.username, password=self.password)
        except ApiException as e:
                current_app.logger.exception(e.reason)
                return
        
        
    def linkAssets(self, instanceFrom: Any, instanceTo: Any):
        
        asset_name_from  = instanceFrom.__class__.__name__ + "_" + instanceFrom.id
        asset_name_to    = instanceTo.__class__.__name__ + "_" + instanceTo.id
        
        # Creating the REST client object with context manager to get auto token refresh

        try:   
            asset_from = self.rest_client.get_tenant_asset(asset_name_from)
            asset_to = self.rest_client.get_tenant_asset(asset_name_to)
            
            
            # Creating relations from device to asset
            relation = EntityRelation(_from=asset_from.id, to=asset_to.id, type="Contains")
            self.rest_client.save_relation(relation)
        
        except ApiException as e:
            current_app.logger.exception(e.reason)
    
     
    def saveAttribute(self, instance:Any, dict_attributes: Any):
        asset_name=instance.__class__.__name__ + "_" + instance.id
        
        # Creating the REST client object with context manager to get auto token refresh
    
        try:
            asset = self.rest_client.get_tenant_asset(asset_name)
        except ApiException as e:
            if (e.status==404):
                asset=None
            else:
                current_app.logger.exception(e.reason)
                
        # 
        if asset is not None:
            self.rest_client.save_entity_attributes_v2(asset.id, "SERVER_SCOPE", dict_attributes  )
        

         
    def updateAssetAttributesValues(self, instance: Any):
        
        asset_name=instance.__class__.__name__ + "_" + instance.id
        
        
        try:
            asset = self.rest_client.get_tenant_asset(asset_name)
            dict_attributes=instance.get_attributes_for_thingsboard()
            cloud_attributes = self.rest_client.get_attributes(asset.id, keys=','.join(dict_attributes.keys()))
            
            cloud_attributes_updated={}
            for attribute_key in dict_attributes.keys():
                bln_found=False
                for cloud_attribute in cloud_attributes:
                    if cloud_attribute["key"] == attribute_key:
                        bln_found=True
                        if cloud_attribute["value"] != dict_attributes[attribute_key]:
                            # need update of this attribute value
                            cloud_attributes_updated[attribute_key] = dict_attributes[attribute_key]
                            
                if bln_found == False:
                    # need insert this new attribute key and value
                    cloud_attributes_updated[attribute_key]= dict_attributes[attribute_key]
            
            self.rest_client.save_entity_attributes_v2(asset.id, "SERVER_SCOPE", cloud_attributes_updated  )
            return asset
        except ApiException as e:
            if (e.status==404):
                asset=None
                return asset
            else:
                current_app.logger.exception(e.reason)
                raise Exception("already exists")


    def deleteAsset(self, instance:Any):
        asset_profile=instance.__class__.__name__
        asset_name=instance.__class__.__name__ + "_" + instance.id
        
         # est-ce que l'asset existe ?
        try:
            asset = self.rest_client.get_tenant_asset(asset_name)
        except ApiException as e:
            if (e.status==404):
                asset=None
            else:
                current_app.logger.exception(e.reason)
        
        self.rest_client.delete_asset(asset_id=asset.id)
        current_app.logger.info("asset {} deleted".format(asset_name))
        
        
          
    # syncAsset : create or update Asset on Cloud and update attributes values     
    def syncAsset(self, instance: Any):
        
        asset_profile=instance.__class__.__name__
        asset_name=instance.__class__.__name__ + "_" + instance.id
        
        
        # est-ce que le profile existe ?
        try:        
            # recherche sur le nom du profile d'asset
            asset_profile_list = self.rest_client.get_asset_profile_infos(page_size=1, page=0, text_search=asset_profile, sort_property=None, sort_order=None)
            if (len(asset_profile_list.data) == 0):
                asset_profile = AssetProfile(name=asset_profile)
                asset_profile = self.rest_client.save_asset_profile(asset_profile)
            else:
                asset_profile = asset_profile_list.data[0] 
        except ApiException as e:
            current_app.logger.exception(e.reason)
            
        # est-ce que l'asset existe ?
        try:
            asset = self.rest_client.get_tenant_asset(asset_name)
        except ApiException as e:
            if (e.status==404):
                asset=None
            else:
                current_app.logger.exception(e.reason)

        
        # non, alors je le créé  
        if asset is None:
            try:
                asset = Asset(name=asset_name, asset_profile_id=asset_profile.id)
                asset = self.rest_client.save_asset(asset)
                current_app.logger.info("Asset was created")

            except ApiException as e:
                current_app.logger.exception(e.reason)
                raise Exception(e)
        
        # je mets à jour ses attributs
        self.updateAssetAttributesValues(instance)
            
        return asset

    def getArboInstance(self, instance):
        
            # 2 types de data à synchroniser dans le cloud : 
            # les assets et les relations entre les assets          
            instances=[]
            instanceslinks=[]

            # nous allons synchroniser l'instance passée en asset
            instances.append(instance)
            
            # balayons les relations de niveau 0
            relationships_items = inspect(instance.__class__).relationships.items()
            for relationships_item in relationships_items:
                relationshipName, relationshipProperty=relationships_item
               
                if relationshipProperty.direction == ONETOMANY:
                    items_niv1 = getattr(instance, relationshipName)
                    for item_niv1 in items_niv1:
                        instances.append(item_niv1)
                        instanceslinks.append({"from":instance, "to": item_niv1})
                        
                        # balayons les relations de niveau 1
                        relationships_items_niv1 = inspect(item_niv1.__class__).relationships.items()
                        for relationships_item_niv1 in relationships_items_niv1:
                            relationshipName_niv1, relationshipProperty_niv1=relationships_item_niv1
                            
                            if relationshipProperty_niv1.direction == ONETOMANY:
                                items_niv2 = getattr(item_niv1, relationshipName_niv1)
                                for item_niv2 in items_niv2:
                                    instances.append(item_niv2)
                                    instanceslinks.append({"from":item_niv1, "to": item_niv2})
            
            return instances, instanceslinks
        
    # cette fonction prend une instance d'objet
    # et la synchronise dans thingsboard 
    # avec 2 niveaux de relations One To Many
    def syncAssetsFromInstanceAndChildren(self, instance):     

            # 2 types de data à synchroniser dans le cloud : 
            # les assets et les relations entre les assets          
            instance_to_sync, instances_to_link=self.getArboInstance(instance)
            
            # je synchronise les assets
            for instance in instance_to_sync:   
                self.syncAsset(instance=instance)
                
            # je synchronise les relations entre les assets
            for instance_to_link in instances_to_link:
                self.linkAssets(instanceFrom=instance_to_link["from"], instanceTo=instance_to_link["to"])
            

    
            
    # cette fonction prend une instance d'objet
    # et la synchronise dans thingsboard 
    # avec 2 niveaux de relations One To Many
    def delAssetsFromInstanceAndChildren(self, instance):     

            # 2 types de data à synchroniser dans le cloud : 
            # les assets et les relations entre les assets          
            instance_to_sync, instances_to_link=self.getArboInstance(instance)
            
            # je synchronise les assets
            for instance in instance_to_sync:   
                self.deleteAsset(instance=instance)
                
            

if __name__ == '__main__':
    tb=ThingsboardConnector()
    x = tb.syncAsset("profileB","assetC3")
    print(x)