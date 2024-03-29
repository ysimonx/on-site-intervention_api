import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER               = os.getenv("MAIL_SERVER")
    MAIL_PORT                 = os.getenv("MAIL_PORT")
    MAIL_USE_SSL              = True
    MAIL_USERNAME             = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD             = os.getenv("MAIL_PASSWORD")
    MAIL_FROM                 = os.getenv("MAIL_FROM")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URL")
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")
    SQLALCHEMY_ECHO = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_ECHO = False

# >>> import uuid
# >>> print(uuid.uuid4())

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
    'upload_dir': os.getenv("UPLOAD_DIR"),
    'default_tenant_config': 'ctei',
    "types_interventions": {
        "scaffolding request": {  
            "type_intervention": "scaffolding request",
            "intervention_on_site_uuid": "67ecd9b0-ff04-4eae-80fa-c55c2c3a45bf",
            "mandatory_lists": {
                  "status": 
                        {
                        "type": "fixed",
                        "values":
                              [
                              "initiated",
                              "assigned",
                              "chrono",
                              "commissioned",
                              "cancelled"
                              ]
                        },
                  "actions":
                        {
                        "type": "fixed",
                        "values":
                              [
                                    "Montage échafaudage",
                                    "Modification échafaudage",
                                    "Montage échafaudage roulant",
                                    "Modification échafaudage roulant",
                                    "Montage protection collective",
                                    "Modification protection collective",
                                    "Autres structures"
                              ]
                        },
                  "utilisations":
                        {
                        "type": "fixed",
                        "values":
                              [
                                    "Bardage, isolation par l'extérieur",
                                    "Calorifuge",
                                    "Désamiantage/déplombage ...",
                                    "Electrique",
                                    "Inspection/instrumentation",
                                    "Levage",
                                    "Maçonnerie lourde",
                                    "Peinture/sablage",
                                    "Renfort/soutient (dalle, tuyeauterie, etc.)",
                                    "Tir radio",
                                    "Tuyauterie",
                                    "Autres (accès, ...)"
                              ]
                        },
                   "pmat":
                        {
                        "type": "fixed",
                        "values":
                              [
                                    "< 100 kg",
                                    "> 100 kg (notifie in description the load)",
                                    "Not concerned"
                              ]
                        },
                  "echafaudage-typologie":
                         {
                        "type": "fixed",
                        "values": [
                                   "Echafaudage de pieds",
                                    "Echafaudage roulant",
                                    "Echafaudage suspendu",
                                    "Escalier ou acces sécurisé",
                                    "Protections collectives",
                                    "Balisage de protection",
                                    "Autres"
                              ] 
                        },      
                  "echafaudage-classe-de-service":
                         {
                        "type": "fixed",
                        "values": [
                                   "Classe 2=150Kg/m²",
                                    "Classe 3=200Kg/m²",
                                    "Classe 4=300Kg/m²",
                                    "Classe 5=450Kg/m²",
                                    "Classe 6=600Kg/m²"
                              ] 
                        }, 
                  "echafaudage-nature-appuis":
                        {
                        "type": "fixed",
                        "values": [
                                   "Béton",
                                    "Caillebotis",
                                    "Charpente métallique",
                                    "Terrain naturel",
                                    "Enrobé",
                                    "Remblai"
                              ] 
                        },
                  "type-d-acces" :
                         {
                        "type": "fixed",
                        "values": [
                                    "Accès intérieur par trappes et échelles inclinées",
                                    "Sapine d'acces extérieur trappes et échelles inclinées",
                                    "Sapine d'acces extérieur par escalier",
                                    "Accès extérieur par échelle < 4m"
                              ] 
                        }, 
                   "approvisionnement-materiaux" :
                         {
                        "type": "fixed",
                        "values": [
                                    "Aucun",
                                    "Poulie <80kg",
                                    "Treuil jusqu’à 200kg",
                                    "Potence jusqu’à 500kg",
                                    "Potence > 500kg",
                                    "Monte materiaux>500kg",
                                    "Goulotte à gravats"
                              ] 
                        }, 
                  "protection-personnes-biens-ouvrages":
                        {
                        "type": "fixed",
                        "values": [
                                   "Aucun",
                                    "Filets micro-mailles",
                                    "Bâches thermo",
                                    "Bâches anti-feu",
                                    "Bardage métallique vertical",
                                    "Bardage métallique horizontal",
                                    "Protection plastique  (Brid Guard)"
                              ] 
                        }, 
                  "echafaudage-marque-materiel" : 
                         {
                        "type": "fixed",
                        "values": [
                                   "LAYHER",
                                    "PLETTAC",
                                    "ENTREPOSE"
                              ] 
                        }, 
                  "echafaudage-type-facturation":
                         {
                        "type": "fixed",
                        "values": [
                                   "Forfait",
                                   "Régie",
                                   "Bordereau"
                                   
                              ] 
                        },
                  "entreprise-utilisatrice": 
                        {
                        "type": "administrable_by_site",
                        "values":
                              [
                              
                              ]
                        },
                  "dimensions": 
                        {
                        "type": "administrable_by_site",
                        "values":
                              [
                              
                              ]
                  },
                  "elevation": 
                        {
                        "type": "administrable_by_site",
                        "values":
                              [
                              
                              ]
                  },
            },
            "forms": {
                "1" :{"form_name":"besoin",
                      "form_on_site_uuid": "9f1f20e3-d3cd-4a58-97fc-2e42a4d7b736",
                      "sections": {
                        "1": { "section_name" : "Donneur d'ordre",
                              "section_type" : "section type 1",
                              "section_on_site_uuid": "ef637435-30fe-4a3f-941f-f29a8df8f865",
                              "fields": {
                                    "1": { "field_name":"donneur-ordre",
                                                "field_label":"Donneur d'ordre",
                                                "field_type":"user_from_role",
                                                "field_on_site_uuid":"c49886e4-6729-47cf-9272-b0c54c6caf3d",
                                                "values":["donneur d'ordre"]
                                    },
                              }
                        },
                        "2": { "section_name" : "identification de la demande",
                              "section_type" : "section type 2",
                              "section_on_site_uuid": "68bb7af3-d341-4a74-baa6-2b9a699404cc",
                              "fields": {
                                    "1": { "field_name":"numero-permis-ot",
                                                "field_label":"N°permis/d'OT",
                                                "field_type":"text",
                                                "field_on_site_uuid":"47fdf096-9e96-446a-afde-ab2beb81e5a1",
                                                "values":[]
                                    },
                                    "2": { "field_name":"date-demande",
                                                "field_label":"date de la demande",
                                                "field_type":"date",
                                                "field_on_site_uuid":"2f7b84e7-8d38-4544-9027-c9772089a5d0",
                                                "values":[]
                                    },
                                    "3": { "field_name":"date-mise-a-disposition",
                                                "field_label":"Mise à disposition souhaitée",
                                                "field_type":"date",
                                                "field_on_site_uuid":"10909dee-86da-459f-8094-ee3d199e1631",
                                                "values":[]
                                    },
                                    "4": { "field_name":"duree-mise-a-disposition",
                                                "field_label":"Durée de mise à disposition (jours)",
                                                "field_type":"integer",
                                                "field_on_site_uuid":"34ea515d-0bff-4651-91e7-a7a24b243b6b",
                                                "values":[]
                                    }
                              }
                        },
                        "3": { "section_name" : "échafaudeur",
                              "section_type" : "section type 2",
                              "section_on_site_uuid": "a4396dc1-0091-4915-baed-75b70f5dc8dc",
                              "fields": {
                                    "1": { "field_name":"demande-echafaudeur",
                                           "field_label":"Echafaudeur",
                                           "field_type":"user_from_role",
                                           "field_on_site_uuid":"8a4bb1eb-af22-4ce1-91c4-4c3d89e14709",
                                           "values": ["échafaudeur"]
                                      }
                              }
                        },
                        "4": { "section_name" : "nature des opérations",
                              "section_type" : "section type 2",
                              "section_on_site_uuid": "abc3514f-0fbf-4cd3-81a5-c35983f95f55",
                              "fields": {
                                   
                                    "1": { "field_name":"entreprise-utilisatrice-1",
                                                "field_label":"Entreprise utilisatrice 1",
                                                "field_type":"list_from_mandatory_lists",
                                                "field_on_site_uuid":"dd714f1d-0333-45d4-83ba-8955d5bf0cb5",
                                                "values":["entreprise-utilisatrice"]
                                    },
                                    "2": { "field_name":"utilisation-1",
                                                "field_label":"Utilisation 1",
                                                "field_type":"list_from_mandatory_lists",
                                                "field_on_site_uuid":"ed645d0a-ac24-4ffe-9fe1-b0591a7e1835",
                                                "values":["utilisations"]
                                    },
                                    "3": { "field_name":"entreprise-utilisatrice-2",
                                                "field_label":"Entreprise utilisatrice 2",
                                                "field_type":"list_from_mandatory_lists",
                                                "field_on_site_uuid":"3b494675-c3ba-4e60-a577-eceb1222291f",
                                                "values":["entreprise-utilisatrice"]
                                    },
                                    "4": { "field_name":"utilisation-2",
                                                "field_label":"Utilisation 2",
                                                "field_type":"list_from_mandatory_lists",
                                                "field_on_site_uuid":"34b2e441-647f-4cc2-a796-d865890c8c04",
                                                "values":["utilisations"]
                                    },
                                    "5": { "field_name":"entreprise-utilisatrice-3",
                                                "field_label":"Entreprise utilisatrice 3",
                                                "field_type":"list_from_mandatory_lists",
                                                "field_on_site_uuid":"7b6ec55c-d012-4219-bfbf-bafb7992ceec",
                                                "values":["entreprise-utilisatrice"]
                                    },
                                    "6": { "field_name":"utilisation-3",
                                                "field_label":"Utilisation 3",
                                                "field_type":"list_from_mandatory_lists",
                                                "field_on_site_uuid":"c242fe59-d17f-4796-bceb-c1c9963c8525",
                                                "values":["utilisations"]
                                    },
                                    "7": { "field_name":"entreprise-utilisatrice-4",
                                                "field_label":"Entreprise utilisatrice 4",
                                                "field_type":"list_from_mandatory_lists",
                                                "field_on_site_uuid":"b3c7b59f-0d5b-49b1-a3ad-931fb37ab536",
                                                "values":["entreprise-utilisatrice"]
                                    },
                                    "8": { "field_name":"utilisation-4",
                                                "field_label":"Utilisation 4",
                                                "field_type":"list_from_mandatory_lists",
                                                "field_on_site_uuid":"cc10c052-e0a4-4af3-bde0-2a9f9ab651c1",
                                                "values":["utilisations"]
                                    },
                                    "9": { "field_name":"entreprise-utilisatrice-5",
                                                "field_label":"Entreprise utilisatrice 5",
                                                "field_type":"list_from_mandatory_lists",
                                                "field_on_site_uuid":"a9792ace-543b-4866-92d0-2bb24fe4a72f",
                                                "values":["entreprise-utilisatrice"]
                                    },
                                    "10": { "field_name":"utilisation-5",
                                                "field_label":"Utilisation 5",
                                                "field_type":"list_from_mandatory_lists",
                                                "field_on_site_uuid":"bcccc812-a542-457d-a421-6548ef72acb7",
                                                "values":["utilisations"]
                                    },
                                   
                              }
                        },
                         "5": { "section_name" : "description du besoin",
                              "section_type" : "section type 2",
                              "section_on_site_uuid": "70bcdf77-14b7-42b2-820c-f3ec82f1d27b",
                              "fields": {
                                    "1": { "field_name": "longueur-echafaudage-souhaite",
                                           "field_label": "Longueur",
                                           "field_type": "list_from_mandatory_lists",
                                           "field_on_site_uuid": "c86dfbda-4574-4093-a7df-3986fa721304",
                                            "values":["dimensions"]
                                           },
                                    "2": { "field_name": "largeur-echafaudage-souhaite",
                                           "field_label": "Largeur",
                                           "field_type": "list_from_mandatory_lists",
                                           "field_on_site_uuid": "c86dfbda-4574-4093-a7df-3986fa721304",
                                            "values":["dimensions"]
                                           },
                                    "3": { "field_name": "hauteur-echafaudage-souhaite",
                                           "field_label": "Hauteur",
                                           "field_type": "list_from_mandatory_lists",
                                           "field_on_site_uuid": "176e5c64-a286-4fa9-a544-fbcc6f48abb5",
                                            "values":["dimensions"]
                                           },
                                    "4": { "field_name": "altitude-elevation-souhaite",
                                           "field_label": "Altitude/Elevation/Niveau",
                                           "field_type": "list_from_mandatory_lists",
                                           "field_on_site_uuid": "6887c05a-28b2-4caa-94ec-89ad455eda4d",
                                            "values":["elevation"]
                                           },
                                      "5": { "field_name":"dimension-echafaudage-ou-plancher",
                                           "field_label":"Dimensions échafaudage ou plancher ?",
                                           "field_type":"switch",
                                           "field_on_site_uuid":"95cd67d3-fb22-4a30-931d-7cd0f3bfb21f",
                                           "value_on": "échafaudage",
                                           "value_off": "plancher"
                                      },
                                    "6": { "field_name":"charges-reparties-ou-ponctuelle",
                                           "field_label":"Charges réparties ou ponctuelles",
                                           "field_type":"switch",
                                           "field_on_site_uuid":"26bd134c-a4fb-49c5-b430-71dc8c7128db",
                                           "value_on": "oui",
                                           "value_off": "non"
                                      },
                                    "7": { "field_name":"precisions-charges-reparties-ou-ponctuelle",
                                                "field_label":"Oui : préciser niveau(x) + poids",
                                                "field_type":"text",
                                                "field_on_site_uuid":"81986e84-a190-44ad-a83c-3ce416407b9f",
                                                "values":[]},
                                    "8": { "field_name":"stockage-sur-plancher-de-travail",
                                           "field_label":"Stockage sur le plancher de travail",
                                           "field_type":"switch",
                                           "field_on_site_uuid":"2169dfb2-27f8-46c2-a681-3e43940d503b",
                                           "value_on": "oui",
                                           "value_off": "non"
                                      },
                                    "9": { "field_name":"precisions-stockage-sur-plancher-de-travail",
                                                "field_label":"Oui : préciser niveau(x) + poids",
                                                "field_type":"text",
                                                "field_on_site_uuid":"20fd4811-02f4-4762-8a29-1a8754353dde",
                                                "values":[]},
                                    "10": { "field_name":"nombre-de-travailleurs",
                                           "field_label":"Nombre de travailleurs",
                                           "field_type":"integer",
                                           "field_on_site_uuid":"81380fd5-7652-4e88-9af9-f03972a772a1"
                                      },
                                      "11": { "field_name": "type-d-acces",
                                           "field_label": "Type d'accès",
                                           "field_type": "list_from_mandatory_lists",
                                           "field_on_site_uuid": "893f538a-5ff1-44a1-9ff0-5b0bd8d50ddb",
                                            "values":["type-d-acces"]
                                           },
                                      "12": { "field_name": "approvisionnement-materiaux",
                                           "field_label": "Approvisionnement materiaux",
                                           "field_type": "list_from_mandatory_lists",
                                           "field_on_site_uuid": "e24edb51-d00d-49f0-8941-5604de59c369",
                                            "values":["approvisionnement-materiaux"]
                                           },
                                      "13": { "field_name": "protection-personnes-biens-ouvrages",
                                           "field_label": "Protection des personnes/biens/ouvrages",
                                           "field_type": "list_from_mandatory_lists",
                                           "field_on_site_uuid": "206ef5af-7700-43f1-90df-3aa475e510e0",
                                            "values":["protection-personnes-biens-ouvrages"]
                                           },
                              }
                        },
                         
                        "6": { "section_name" : "description",
                              "section_type" : "section type 3",
                              "section_on_site_uuid": "219fa801-82f3-450b-97f1-9d2db8bf33af",
                              "fields": {
                                    "1": { "field_name":"description",
                                          "field_label":"description",
                                          "field_type":"paragraph",
                                          "field_on_site_uuid":"1e8d26db-3513-4a7d-afc8-9610525b6521",
                                          "values":[]
                              },
                              }
                        },
                        "7": { "section_name" : "medias",
                                "section_type" : "section type 4",
                                "section_on_site_uuid": "e6391434-1e0e-48be-8b69-aa603cb99a9e",
                                 "fields": {
                                       "1": { "field_name":"initial_request_pictures",
                                           "field_label":"pictures",
                                           "field_type":"gallery",
                                           "field_on_site_uuid":"5f927a1c-5bc9-492f-b955-decdd2823708",
                                           "values": []
                                      },
                                 }
                         },
                         "8": { "section_name" : "Schema",
                                "section_type" : "section type 5",
                                "section_on_site_uuid": "32251e12-ab48-4477-871e-5c67352effaf",
                                 "fields": {
                                       "1": { "field_name":"schema",
                                           "field_label":"schema",
                                           "field_type":"schema",
                                           "field_on_site_uuid":"84d763eb-e368-452e-8038-2ead384cb492",
                                           "values": []
                                      },
                                 }
                         }
                  }
                },
                "2" :{"form_name":"visite",
                      "form_on_site_uuid": "a81c475c-3b9d-40da-839d-56eeee06e85a",
                      "sections": {
                        "1": { "section_name" : "Caractéristiques de l'échafaudage",
                              "section_type" : "section type 1",
                              "section_on_site_uuid": "11b19f92-b590-44d5-b29c-4144b709bd9b",
                              "fields": {
                                    "1": { "field_name":"visite-date",
                                          "field_label":"Date visite",
                                          "field_type":"date",
                                          "field_on_site_uuid":"dbf12337-261a-49a2-a84e-8d7c366a9b94",
                                          "default_value":"now"
                                    },
                                    "2": { "field_name":"visite-typologie",
                                                "field_label":"Typologie",
                                                "field_type":"list_from_mandatory_lists",
                                                "field_on_site_uuid":"245096d8-0ac2-46cb-97ae-242501ac0230",
                                                "values":["echafaudage-typologie"]
                                    },
                                    "3": { "field_name":"visite-classe-service",
                                                "field_label":"Classe de service",
                                                "field_type":"list_from_mandatory_lists",
                                                "field_on_site_uuid":"3d8c35a9-02e0-49d9-b568-f4b35d85b267",
                                                "values":["echafaudage-classe-de-service"]
                                    },
                                     "4": { "field_name":"visite-nature-appuis",
                                                "field_label":"Nature des appuis",
                                                "field_type":"list_from_mandatory_lists",
                                                "field_on_site_uuid":"b803d6ce-188f-46f9-be37-d482996a3da3",
                                                "values":["echafaudage-nature-appuis"]
                                    },
                                    "5": { "field_name": "visite-longueur-echafaudage",
                                           "field_label": "Longueur",
                                           "field_type": "list_from_mandatory_lists",
                                           "field_on_site_uuid": "3cd0c728-8e18-4b07-919c-957a0ea4181d",
                                            "values":["dimensions"]
                                     },
                                    "6": { "field_name": "visite-largeur-echafaudage",
                                           "field_label": "Largeur",
                                           "field_type": "list_from_mandatory_lists",
                                           "field_on_site_uuid": "5fff33d7-0a2d-4a10-8f59-a8c511e26616",
                                            "values":["dimensions"]
                                     },
                                     "7": { "field_name": "visite-hauteur-echafaudage",
                                           "field_label": "Hauteur",
                                           "field_type": "list_from_mandatory_lists",
                                           "field_on_site_uuid": "0caa620c-6823-4c01-9774-aabb02359019",
                                            "values":["dimensions"]
                                     },
                                     "8": { "field_name": "visite-altitude-elevation",
                                           "field_label": "Altitude/Elevation/Niveau",
                                           "field_type": "list_from_mandatory_lists",
                                           "field_on_site_uuid": "66a1a9d6-9d50-42b2-bfca-68068e7b0bf3",
                                            "values":["elevation"]
                                           },
                                     "9": { "field_name":"visite-planchers-travail",
                                           "field_label":"Nombre de planchers travail",
                                           "field_type":"list",
                                           "field_on_site_uuid":"e4b3e46c-0b90-412e-b6ed-e8c0087cff4d",
                                           "values": [
                                               "1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"
                                            ] 
                                    },
                                      "10": { "field_name":"visite-planchers-acces",
                                           "field_label":"Nombre de planchers d'accès",
                                           "field_type":"list",
                                           "field_on_site_uuid":"313f56bb-ef39-4a62-ae72-cc494cb77c56",
                                           "values": [
                                               "1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"
                                            ] 
                                    }, "11": { "field_name":"visite-conforme-notice",
                                           "field_label":"Conforme notice constructeur",
                                           "field_type":"switch",
                                           "field_on_site_uuid":"2158ecbb-b3f6-445e-b865-dc9df322bc3c",
                                           "value_on": "oui",
                                           "value_off": "non"
                                      },
                                     "12": { "field_name":"visite-marque-materiel",
                                           "field_label":"Marque matériel",
                                            "field_type": "list_from_mandatory_lists",
                                           "field_on_site_uuid": "7e6434b0-9594-421c-b0ab-0fa44ca84f6d",
                                            "values":["echafaudage-marque-materiel"]
                                           },
                                      
                                     "13": { "field_name":"visite-modification-prevoir",
                                           "field_label":"Modifications à prévoir",
                                            "field_type":"switch",
                                           "field_on_site_uuid":"192aecba-ad91-4697-b65d-230338d88b2b",
                                           "value_on": "oui",
                                           "value_off": "non"
                                           
                                      },
                                      "14": { "field_name":"visite-precisions-modification-prevoir",
                                                "field_label":"Oui : lesquelles ?",
                                                "field_type":"text",
                                                "field_on_site_uuid":"fb07dd35-57b3-447d-b819-7b0e6d3d8dd1",
                                                "values":[]
                                    },
                                       "15": { "field_name":"visite-type-facturation",
                                           "field_label":"Facturation",
                                            "field_type": "list_from_mandatory_lists",
                                           "field_on_site_uuid": "b19c7eb5-7518-4e72-ae01-5fa396db6559",
                                            "values":["echafaudage-type-facturation"]
                                           }
                                      
                              }
                                   
                              
                        },
                        "2": { "section_name" : "Sécurité",
                                "section_type" : "section type 1",
                                "section_on_site_uuid": "a706e588-b8f5-4b11-a711-ee1e7612bb6a",
                                 "fields": {
                                      
                                      "1": { "field_name":"securite-obstrue-acces-dispositif-urgence",
                                           "field_label":"Obstrue un acces ou un dispositif d'urgence",
                                           "field_type":"switch",
                                           "field_on_site_uuid":"3ab35154-c63a-4bf4-b085-8d6a8aa74cbe",
                                           "value_on": "oui",
                                           "value_off": "non"
                                      },
                                      
                                      "2": { "field_name":"securite-zone-evolution-equipement-mobile",
                                           "field_label":"Dans zone d'évolution d'un equipement mobile (palan, ascenceur,…)",
                                           "field_type":"switch",
                                           "field_on_site_uuid":"a5f14187-3704-47b2-b667-5000c37de47e",
                                           "value_on": "oui",
                                           "value_off": "non"
                                      },
                                      
                                      "3": { "field_name":"securite-proximite-reseaux-haute-tension",
                                           "field_label":"proximité directe de réseaux sous très haute tension",
                                           "field_type":"switch",
                                           "field_on_site_uuid":"ac96883f-6e96-4dd9-99cc-0669022b43aa",
                                           "value_on": "oui",
                                           "value_off": "non"
                                      },
                                                                            
                                    "4": { "field_name":"securite-proximite-reseaux-chimiques",
                                           "field_label":"Proximité direct de réseaux chimiques dangereux",
                                           "field_type":"switch",
                                           "field_on_site_uuid":"7b85e8be-b410-4ae7-bb8c-d71ebcb379d3",
                                           "value_on": "oui",
                                           "value_off": "non"
                                      },
                                     "5": { "field_name":"securite-presence-equipement-important",
                                           "field_label":"Présence d'un équipement important",
                                           "field_type":"switch",
                                           "field_on_site_uuid":"640d84f5-30b9-4513-8cb9-bb0820ae0359",
                                           "value_on": "oui",
                                           "value_off": "non"
                                      },
                                       "6": { "field_name":"securite-unite-en-marque",
                                           "field_label":"Unité en marche",
                                           "field_type":"switch",
                                           "field_on_site_uuid":"8f182dd2-b61d-4c43-8fb5-a89e1301c147",
                                           "value_on": "oui",
                                           "value_off": "non"
                                      },
                                      
                                      
                                      
                                      
                                 }
                                },
                        
                        "3": { "section_name" : "Contractualisation du présent cahier des charges",
                                "section_type" : "section type 3",
                                "section_on_site_uuid": "b72ec40c-0194-47a0-9744-35137dde1e9d",
                                 "fields": {
                                       "1": { "field_name":"visite-echafaudeur",
                                           "field_label":"échafaudeur",
                                           "field_type":"user_from_role",
                                           "field_on_site_uuid":"1481ef60-16f5-4090-94a4-daf787ae5926",
                                           "values": ["échafaudeur"]
                                      },
                                       "2": { "field_name":"visite-echafaudeur-signature",
                                           "field_label":"signature",
                                           "field_type":"signature",
                                           "field_on_site_uuid":"983287bb-62c3-42cf-86f2-f15d1b9b4204",
                                      },
                                      "3": { "field_name":"visite-donneur-ordre",
                                                "field_label":"Donneur d'ordre",
                                                "field_type":"user_from_role",
                                                "field_on_site_uuid":"a1d672a5-b522-470e-a4ea-aca66c490ce4",
                                                "values":["donneur d'ordre"]
                                    },
                                       "4": { "field_name":"visite-donneur-ordre-signature",
                                           "field_label":"signature User",
                                           "field_type":"signature",
                                           "field_on_site_uuid":"47afbe06-57a3-416e-8f39-42a4916bf97e",
                                      },
                                        "5": { "field_name":"visite-responsable-unite-fabrication",
                                           "field_label":"Responsable unité fabrication",
                                           "field_type":"user_from_role",
                                           "field_on_site_uuid":"032dfe04-c8f0-4552-9cd1-248b272c7c15",
                                           "values": ["responsable unité fabrication"]
                                      },
                                       "6": { "field_name":"visite-responsable-unite-fabrication-signature",
                                           "field_label":"signature",
                                           "field_type":"signature",
                                           "field_on_site_uuid":"853a16f2-7327-4317-aed4-ea8782556eb4",
                                      },
                                       "7": { "field_name":"visite-service-securite",
                                           "field_label":"service sécurité",
                                           "field_type":"user_from_role",
                                           "field_on_site_uuid":"5a3f72df-7599-48c4-8f51-8fa6127d3a5d",
                                           "values": ["service sécurité"]
                                      },
                                       "8": { "field_name":"visite-service-securite-signature",
                                           "field_label":"signature",
                                           "field_type":"signature",
                                           "field_on_site_uuid":"a3963ed3-38a8-41da-8a23-01822ecf3311",
                                      },
                                 }
                                 
                         },
                        "5": { "section_name" : "medias",
                                "section_type" : "section type 4",
                                "section_on_site_uuid": "c4e6b4b9-4b87-4e75-b873-8376acb6fb71",
                                 "fields": {
                                       "1": { "field_name":"visite_pictures",
                                           "field_label":"pictures",
                                           "field_type":"gallery",
                                           "field_on_site_uuid":"8c5b89ff-62eb-42c7-a259-334bd4a33c79",
                                           "values": []
                                      },
                                 }
                         },
                        "6": { "section_name" : "commentaires",
                              "section_type" : "section type 5",
                              "section_on_site_uuid": "10523e6f-da11-406e-a39d-4b7e00e1e125",
                              "fields": {
                                    "1": { "field_name":"visite_comments",
                                          "field_label":"comments",
                                          "field_type":"paragraph",
                                          "field_on_site_uuid":"25cd9145-cd6f-422d-aab7-a25f7ba23fd4",
                                          "values":[]
                              },
                              }
                        },
                        }
                    },
                "3" :{"form_name":"mise en service",
                      "form_on_site_uuid": "e773e72b-e00e-4fcc-b6be-fbfb70307351",
                      "sections": {
                        "1": { "section_name" : "summary",
                              "section_type" : "section type 1",
                              "section_on_site_uuid": "8db50ed5-633b-4ede-98b6-162bc1c6e883",
                              "fields": {
                                    "1": { "field_name": "commissioning_date",
                                          "field_label": "commissioning date",
                                          "field_type": "date",
                                          "field_on_site_uuid":"2bda509d-62a1-49d2-bd24-021fdb363170"},
                                    "2": { "field_name": "commissioning_attempts",
                                          "field_label": "commissioned at",
                                          "field_type": "switch",
                                          "field_on_site_uuid":"8bb52583-ca7b-4645-8841-306e2da1760a",
                                          "value_on": "1st",
                                           "value_off": "2 or more"}
                              }
                        },
                        "2": { "section_name" : "dimensions",
                              "section_type" : "section type 1",
                              "section_on_site_uuid": "c876534a-d870-43c0-b0ab-a7d53486b9f6",
                              "fields": {
                                   "1": { "field_name": "commissioning_scaff_width",
                                            "field_label": "longueur",
                                           "field_type": "float",
                                           "field_on_site_uuid":"6c3d5abb-484c-4fa2-910e-0fbd182a8b34"
                                           },
                                     "2": { "field_name": "commissioning_scaff_depth",
                                           "field_label": "largeur",
                                           "field_type": "float",
                                           "field_on_site_uuid":"8389bdac-fcd4-4681-ba44-4a2bcbead81d"},
                                     "3": { "field_name": "commissioning_scaff_height",
                                            "field_label": "hauteur",
                                           "field_type": "float",
                                           "field_on_site_uuid":"95d01fa7-0358-4a85-9bfd-9a5951f0b966"},
                                      "4": { "field_name": "commissioning_conformite_notice",
                                            "field_label": "conforme notice",
                                           "field_type": "switch",
                                           "field_on_site_uuid":"1742f506-42bf-43ef-9df3-34a021f3b26e",
                                            "value_on": "oui",
                                           "value_off": "non"},
                              }
                        }, 
                        "3": { "section_name" : "signatures",
                                "section_type" : "section type 1",
                                "section_on_site_uuid": "a8432ea0-d164-47f9-a0a2-877f60078380",
                                 "fields": {
                                      "1": { "field_name":"commissioning_user_commissioning_engineer",
                                           "field_label":"inspecteur échafaudage",
                                           "field_type":"user_from_role",
                                           "field_on_site_uuid":"dd18e0d5-8d3a-477e-ab3d-09d5736b7ffa",
                                           "values": ["inspecteur échafaudage"]
                                      },
                                       "2": { "field_name":"commissioning_signature_commissioning_engineer",
                                           "field_label":"signature",
                                           "field_type":"signature",
                                           "field_on_site_uuid":"e319c8dc-73b6-4b42-8e2f-fec5a627e14d",
                                      },
                                        "3": { "field_name":"commissioning_user_scaffolder",
                                           "field_label":"scaffolder",
                                           "field_type":"user_from_role",
                                           "field_on_site_uuid":"6f212152-0b03-4bec-89a1-bedddb42a59b",
                                           "values": ["échafaudeur"]
                                      },
                                       "4": { "field_name":"commissioning_signature_scaffolder",
                                           "field_label":"signature",
                                           "field_type":"signature",
                                           "field_on_site_uuid":"8510e1e8-ac1a-470e-a040-7640a8d237c1",
                                      },
                                        "5": { "field_name":"commissioning_user_email",
                                           "field_label":"user e-mail",
                                           "field_type":"email",
                                           "field_on_site_uuid":"d0316f25-508b-4817-b0c6-e42771bab6d0",
                                           "values": []
                                      },
                                       "6": { "field_name":"commissioning_signature_user",
                                           "field_label":"signature User",
                                           "field_type":"signature",
                                           "field_on_site_uuid":"dd0dc969-5daf-4dd3-8877-d1406b02b5f8",
                                      },
                                 },
                        
                        },
                  
                         "4": { "section_name" : "medias",
                                "section_type" : "section type 4",
                                "section_on_site_uuid": "1ac3151a-07ef-4337-b9f8-2ae822f2328b",
                                 "fields": {
                                       "1": { "field_name":"commissioning_pictures",
                                           "field_label":"pictures",
                                           "field_type":"gallery",
                                           "field_on_site_uuid":"4ae6e76d-5cab-4b21-916f-e8d603361354",
                                           "values": []
                                      },
                                 }
                        },
                        "5": { "section_name" : "commentaires",
                                "section_type" : "section type 1",
                                "section_on_site_uuid": "aa061771-8fb6-49ce-8863-e405b2d99d7d",
                                 "fields": {
                                       "1": { "field_name":"commissioning_comments",
                                          "field_label":"comments",
                                          "field_type":"paragraph",
                                          "field_on_site_uuid":"ba366f19-e4ca-43a9-858e-2dc6e6d2d87d",
                                          "values":[]
                                 } },
                        
                        },
                        
                      }
                },
                
            }
            
        },
        "calorifuge": {  
            "type_intervention": "calorifuge",
            "intervention_on_site_uuid": "5ceba891-670a-40ea-ba7f-87bd4597dbde",
            "list_statuses" : [
                  "initiated",
                  "assigned",
                  "chrono",
                  "commissioned",
                  "cancelled"
            ],
            "forms": {
                "1" :{"form_name":"initial request 2",
                      "form_on_site_uuid": "b89cf79e-36d2-4a65-ad01-479dc2e769f8",
                       "sections": {}},
                "2" :{"form_name":"visit 2",
                      "form_on_site_uuid": "f35f3474-2d1d-407f-ac72-1b70f89ff08f",
                       "sections": {}},
                "3" :{"form_name":"commissioning 2",
                      "form_on_site_uuid": "6c4480f5-8e95-4a9b-9bcc-254e76d682c",
                       "sections": {}},
                "4" :{"form_name":"rapport de vérifications 2",
                      "form_on_site_uuid": "47d8d1e6-9273-4286-8de3-ba6d80233b4f",
                       "sections": {}}
            }
        }
    },
    "roles": [
          "admin",
          "admin site",
          "site administrator",
          "donneur d'ordre",
          "coordinateur échafaudage",
          "operator",
          "cost contrôleur",
          "échafaudeur",
          "responsable unité fabrication",
          "service sécurité",                                     #Health and Safety Project Coordinator
          "inspecteur échafaudage",
          "utilisateur"
      ]
}
