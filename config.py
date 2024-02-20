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
            "forms": {
                "1" :{"form_name":"initial request",
                      "form_on_site_uuid": "9f1f20e3-d3cd-4a58-97fc-2e42a4d7b736",
                      "sections": {
                          "1": { "section_name" : "initial request rub a",
                                 "section_type" : "section type 1",
                                 "section_on_site_uuid": "ef637435-30fe-4a3f-941f-f29a8df8f865",
                                 "fields": {
                                     "1": { "field_name": "field aa",
                                           "field_type": "field_type 1","field_on_site_uuid":"46d8ccd9-5580-4c92-b9cc-eebb76b9c57c"},
                                     "2": { "field_name": "field ab",
                                           "field_type": "field_type 1","field_on_site_uuid":"0b3f2281-cb74-4122-bdb5-353214e7c611"},
                                     "3": { "field_name": "field ac",
                                           "field_type": "field_type 1","field_on_site_uuid":"0b3f2281-cb74-4122-bdb5-353214e7c611"},
                                 }
                                },
                                 
                          "2": { "section_name" : "initial request rub b",
                                "section_type" : "section type 2",
                                "section_on_site_uuid": "6b8b8b4c-8bca-4697-8c3c-6b70d4fd9b51",
                                 "fields": {
                                     "1": { "field_name": "field ba",
                                           "field_type": "field_type 1","field_on_site_uuid":"0b3f2281-cb74-4122-bdb5-353214e7c611"},
                                     "2": { "field_name": "field bb",
                                           "field_type": "field_type 1","field_on_site_uuid":"30a238fe-5de1-48c6-b91a-3d177124f634"},
                                     "3": { "field_name": "field bc",
                                           "field_type": "field_type 1","field_on_site_uuid":"f249bf91-9bfd-4516-96a5-94bd31e9e391"},
                                 } },
                          "3": { "section_name" : "initial request rub c",
                                "section_type" : "section type 3",
                                "section_on_site_uuid": "83ce8e7f-1c28-4270-bede-9bd5dcd6ab0e",
                                 "fields": {
                                     "1": { "field_name": "field ca",
                                           "field_type": "field_type 1","field_on_site_uuid":"9d4f8747-f238-4c41-81b7-b16adb97d9c7"},
                                     "2": { "field_name": "field cb",
                                           "field_type": "field_type 1","field_on_site_uuid":"7669d2b9-e626-4acc-842c-6922d2737a1f"},
                                     "3": { "field_name": "field cc",
                                           "field_type": "field_type 1","field_on_site_uuid":"d76e74ca-b7ce-463c-b833-4ba45585d224"},
                                 } },
                     }
                    },
                "2" :{"form_name":"visit",
                      "form_on_site_uuid": "a81c475c-3b9d-40da-839d-56eeee06e85a",
                      "sections": {
                          "1": { "section_name" : "Techniques",
                                "section_type" : "section type 1",
                                "section_on_site_uuid": "11b19f92-b590-44d5-b29c-4144b709bd9b",
                                 "fields": {
                                    "1": { "field_name":"scaff_type",
                                           "field_label":"Type",
                                           "field_type":"list",
                                           "field_on_site_uuid":"e28cbc05-2f4b-46f5-acca-c147ae8a1db8",
                                           "values": [
                                               "Fixe",
                                               "Roulant",
                                               "Balisage en dur",
                                               "Protection", 
                                               "Potence",
                                               "Escalier",
                                               "Autre"
                                            ] 
                                    },
                                     "2": { "field_name":"visit_date",
                                           "field_label":"Visit Date",
                                           "field_type":"date",
                                           "field_on_site_uuid":"a1d5131d-d8bc-4783-8c0b-fb81f5e4a459",
                                           "default_value":"now"
                                          
                                    }
                                 }
                                },
                          "2": { "section_name" : "Dimensions",
                                "section_type" : "section type 1",
                                "section_on_site_uuid": "de3b8182-df35-4c6a-9aea-8d652efd8142",
                                 "fields": {
                                      "1": { "field_name":"scaff_charge_exploitation_prevue",
                                           "field_label":"Charge Exploit prévue",
                                           "field_type":"list",
                                           "field_on_site_uuid":"43f30456-0f0d-4fef-842c-01f869f85cdd",
                                           "values": [
                                               "Classe 3 (répartis 250kg/m2)",
                                               "Classe 4 et 5 (300kg/m2>répartis<450kg/m2)",
                                               "Classe 6 (450 Kg/m2>répartis<600kg/m2)",
                                               "autre(à renseigner dans commentaire)", 
                                               
                                            ] 
                                        },
                                      "2": { "field_name":"scaff_conforme_notice",
                                           "field_label":"Conforme Notice",
                                           "field_type":"switch",
                                           "field_on_site_uuid":"fb737b8d-db58-418f-a69f-b437539cdec6",
                                           "value_on": "oui",
                                           "value_off": "non"
                                      },
                                      "3": { "field_name":"visit_date_reception_prevue",
                                           "field_label":"Date Réception prévue",
                                           "field_type":"date",
                                           "field_on_site_uuid":"4d83d71d-adfe-45f8-968c-5d9761f4c288",
                                           "default_value":"j+15",
                                      },
                                     "4": { "field_name": "scaff_width",
                                            "field_label": "Longueur",
                                           "field_type": "integer",
                                           "field_on_site_uuid":"8dd3f411-6f67-43c4-9d9d-1d420cc6bc68"
                                           },
                                     "5": { "field_name": "scaff_depth",
                                           "field_label": "Largeur",
                                           "field_type": "integer",
                                           "field_on_site_uuid":"0b1a49af-757f-4127-a0fb-f525d2f71f70"},
                                     "6": { "field_name": "scaff_height",
                                            "field_label": "Hauteur",
                                           "field_type": "integer",
                                           "field_on_site_uuid":"29c05fa8-c1d6-4026-bd4a-356a1e0eca7b"},
                                      "7": { "field_name":"scaff_nb_planchers_travail",
                                           "field_label":"Nombre de planchers travail",
                                           "field_type":"list",
                                           "field_on_site_uuid":"552460e5-b326-4cba-816c-e84202f1f83c",
                                           "values": [
                                               "1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"
                                            ] 
                                    },
                                 }
                                },
                                 
                         "3": { "section_name" : "Interventants",
                                "section_type" : "section type 3",
                                "section_on_site_uuid": "b72ec40c-0194-47a0-9744-35137dde1e9d",
                                 "fields": {
                                       "1": { "field_name":"user_scaffolder",
                                           "field_label":"Scaffolder",
                                           "field_type":"user_from_role",
                                           "field_on_site_uuid":"1481ef60-16f5-4090-94a4-daf787ae5926",
                                           "values": ["scaffolder"]
                                      },
                                       "2": { "field_name":"signature_scaffolder",
                                           "field_label":"Signature",
                                           "field_type":"signature",
                                           "field_on_site_uuid":"983287bb-62c3-42cf-86f2-f15d1b9b4204",
                                      },
                                 }
                         },
                          "4": { "section_name" : "Medias",
                                "section_type" : "section type 4",
                                "section_on_site_uuid": "c4e6b4b9-4b87-4e75-b873-8376acb6fb71",
                                 "fields": {
                                       "1": { "field_name":"visit_pictures",
                                           "field_label":"pictures",
                                           "field_type":"gallery",
                                           "field_on_site_uuid":"8c5b89ff-62eb-42c7-a259-334bd4a33c79",
                                           "values": []
                                      },
                                 }
                         }
                            
                        }
                    },
                "3" :{"form_name":"commissioning",
                      "form_on_site_uuid": "e773e72b-e00e-4fcc-b6be-fbfb70307351",
                      "sections": {
                          "1": { "section_name" : "commissioning rub a",
                                "section_type" : "section type 1",
                                "section_on_site_uuid": "7c1b3d74-b98a-43a5-9520-dee3a22f7dcb",
                                 "fields": {
                                     "1": { "field_name": "field aa",
                                           "field_type": "field_type 1","field_on_site_uuid":"27f76c97-0ea7-4274-ae09-62748bfc4a33"},
                                     "2": { "field_name": "field ab",
                                           "field_type": "field_type 1","field_on_site_uuid":"f1ee438e-580f-4760-a748-6621f3c32ecf"},
                                     "3": { "field_name": "field ac",
                                           "field_type": "field_type 1","field_on_site_uuid":"54dfe367-ba00-40e6-9eb1-cda38bc7d896"},
                                 }
                                },
                                 
                          "2": { "section_name" : "commissioning rub b",
                                "section_type" : "section type 1",
                                "section_on_site_uuid": "9d33f2b7-6543-4738-b974-1892ce675260",
                                 "fields": {
                                     "1": { "field_name": "field ba",
                                           "field_type": "field_type 1","field_on_site_uuid":"f00da6cd-aa31-49bd-a2f0-a85fe275240e"},
                                     "2": { "field_name": "field bb",
                                           "field_type": "field_type 1","field_on_site_uuid":"20a26c7c-321f-407d-ba39-2b6ca7c623dc"},
                                     "3": { "field_name": "field bc",
                                           "field_type": "field_type 1","field_on_site_uuid":"e9f823c0-956d-4cf9-b3e6-cd13e58f1551"},
                                 } },
                          "3": { "section_name" : "commissioning rub c",
                                "section_type" : "section type 1",
                                "section_on_site_uuid": "0d19ba0a-1af3-4f7d-9243-b7ae04634c39",
                                 "fields": {
                                     "1": { "field_name": "field ca",
                                           "field_type": "field_type 1","field_on_site_uuid":"5c69d56e-fdb6-4bd3-8973-620479e4045f"},
                                     "2": { "field_name": "field cb",
                                           "field_type": "field_type 1","field_on_site_uuid":"2d502bd6-7e18-4018-8821-1b7d66b7fe03"},
                                     "3": { "field_name": "field cc",
                                           "field_type": "field_type 1","field_on_site_uuid":"672e17c1-9aec-4a54-a2a0-35b5c59fdb55"},
                                 } },
                     }
                      },
                "4" :{"form_name":"rapport de vérifications",
                      "form_on_site_uuid": "3e5a68a0-ac2f-4bf0-9f96-e2cf205b658e",
                      "sections": {
                          "1": { "section_name" : "rapport de vérifications rub a",
                                 "section_type" : "section type 1",
                                 "section_on_site_uuid": "0d19ba0a-1af3-4f7d-9243-b7ae04634c39",
                                 "fields": {
                                     "1": { "field_name": "field aa",
                                           "field_type": "field_type 1","field_on_site_uuid":"11aa7a09-14ff-4766-b1ba-e541a25ed9e5"},
                                     "2": { "field_name": "field ab",
                                           "field_type": "field_type 1","field_on_site_uuid":"398e5a3c-d583-4265-ba40-e01dd2a1c28a"},
                                     "3": { "field_name": "field ac",
                                           "field_type": "field_type 1","field_on_site_uuid":"042089d1-6b32-49cf-b3a7-1e86e68e26e4"},
                                 }
                                },
                                 
                          "2": { "section_name" : "rapport de vérifications rub b",
                                 "section_type" : "section type 1",
                                 "section_on_site_uuid": "8f21a7d9-854e-4faf-8f26-180b7b5cc6c3",
                                 "fields": {
                                     "1": { "field_name": "field ba",
                                           "field_type": "field_type 1","field_on_site_uuid":"6312e0e9-2210-4487-8c7c-8e210448b6f3"},
                                     "2": { "field_name": "field bb",
                                           "field_type": "field_type 1","field_on_site_uuid":"8940a306-5532-440e-b43b-cce0538b8820"},
                                     "3": { "field_name": "field bc",
                                           "field_type": "field_type 1","field_on_site_uuid":"eafc1f34-c858-441c-b061-86d799547651"},
                                 } },
                          "3": { "section_name" : "rapport de vérifications rub c",
                                 "section_type" : "section type 1",
                                 "section_on_site_uuid": "026d86e1-7256-4fb9-a306-e413fbd925cc",
                                 "fields": {
                                     "1": { "field_name": "field ca",
                                           "field_type": "field_type 1","field_on_site_uuid":"bdc1b557-039c-42db-9f59-adcaf25435f0"},
                                     "2": { "field_name": "field cb",
                                           "field_type": "field_type 1","field_on_site_uuid":"7a24e3d4-fbf4-40a8-85ae-4dc0be6faf1d"},
                                     "3": { "field_name": "field cc",
                                           "field_type": "field_type 1","field_on_site_uuid":"7a24e3d4-fbf4-40a8-85ae-4dc0be6faf1d"},
                                 } },
                     }}
            }
        },
        "calorifuge": {  
            "type_intervention": "calorifuge",
            "intervention_on_site_uuid": "5ceba891-670a-40ea-ba7f-87bd4597dbde",
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
    "roles": ["admin", "coordinator","billing","commissioning","user","operator","scaffolder"]
}
