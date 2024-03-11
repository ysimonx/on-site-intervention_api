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
                              "commissionned",
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
                                    "Acces sécurisé",
                                    "Travaux de peinture",
                                    "Travaux de métallurgie",
                                    "Travaux de montage tuyauterie",
                                    "Travaux d'isolation",
                                    "Travaux électrique",
                                    "Travaux de génie civil",
                                    "Travaux d'inspection",
                                    "Travaux d'instrumentation"
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
                  "scaffold_type":
                        {
                        "type": "fixed",
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
                  "contractor": 
                        {
                        "type": "administrable_by_site",
                        "values":
                              [
                              
                              ]
                        },
            },
            "forms": {
                "1" :{"form_name":"initial request",
                      "form_on_site_uuid": "9f1f20e3-d3cd-4a58-97fc-2e42a4d7b736",
                      "sections": {
                        "1": { "section_name" : "user",
                              "section_type" : "section type 1",
                              "section_on_site_uuid": "ef637435-30fe-4a3f-941f-f29a8df8f865",
                              "fields": {
                              "1": { "field_name":"contractor",
                                          "field_label":"contractor",
                                          "field_type":"list_from_mandatory_lists",
                                          "field_on_site_uuid":"36448a1b-3f11-463a-bf60-7668f32da094",
                                          "values":["contractor"]
                              },
                              "2": { "field_name":"user_name",
                                          "field_label":"name",
                                          "field_type":"text",
                                          "field_on_site_uuid":"9303ae9d-ac90-4a1c-bd11-123a8e94b462",
                                          "values":[]
                              },
                              "3": { "field_name":"user_phone",
                                          "field_label":"telephone",
                                          "field_type":"text",
                                          "field_on_site_uuid":"6ab0e41c-7283-451f-a34c-a01f92ce3e61",
                                          "values":[]
                              },
                              "4": { "field_name":"user_email",
                                          "field_label":"email",
                                          "field_type":"email",
                                          "field_on_site_uuid":"fad83ca8-94e3-482f-93a6-aa28e18f0dcd",
                                          "values":[]
                              }
                              },
                        },
                        "2": { "section_name" : "specifications",
                              "section_type" : "section type 2",
                              "section_on_site_uuid": "68bb7af3-d341-4a74-baa6-2b9a699404cc",
                              "fields": {
                              "1": { "field_name":"feb",
                                          "field_label":"feb",
                                          "field_type":"text",
                                          "field_on_site_uuid":"66ddbbdf-414b-4d53-acbc-392311fcc629",
                                          "values":[]
                              },
                              "2": { "field_name":"date1stutil",
                                          "field_label":"date 1s util",
                                          "field_type":"date",
                                          "field_on_site_uuid":"10909dee-86da-459f-8094-ee3d199e1631",
                                          "values":[]
                              },
                              "3": { "field_name":"duration_in_days",
                                          "field_label":"how many days",
                                          "field_type":"integer",
                                          "field_on_site_uuid":"34ea515d-0bff-4651-91e7-a7a24b243b6b",
                                          "values":[]
                              },
                              "4": { "field_name":"action",
                                          "field_label":"action",
                                          "field_type":"list_from_mandatory_lists",
                                          "field_on_site_uuid":"8dce593a-d863-489f-8249-530a24d10512",
                                          "values":["actions"]
                              },
                              "5": { "field_name":"utilisation",
                                          "field_label":"utilisation",
                                          "field_type":"list_from_mandatory_lists",
                                          "field_on_site_uuid":"82ab9a01-4672-4b35-8016-32e58d001b11",
                                          "values":["utilisations"]
                              },
                              "6": { "field_name":"pmat",
                                          "field_label":"pmat",
                                          "field_type":"list_from_mandatory_lists",
                                          "field_on_site_uuid":"f5c85e28-57b9-438a-a48c-563e8d0a9905",
                                          "values":["pmat"]
                              },
                              "7": { "field_name":"numotp",
                                          "field_label":"numotp",
                                          "field_type":"list_from_mandatory_lists",
                                          "field_on_site_uuid":"4c4549c7-a7b7-4491-abfd-0361db531e02",
                                          "values":[]
                              },
                              }
                        },
                        "3": { "section_name" : "description",
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
                        "4": { "section_name" : "medias",
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
                         }
                  }
                },
                "2" :{"form_name":"visit",
                      "form_on_site_uuid": "a81c475c-3b9d-40da-839d-56eeee06e85a",
                      "sections": {
                        "1": { "section_name" : "techniques",
                              "section_type" : "section type 1",
                              "section_on_site_uuid": "11b19f92-b590-44d5-b29c-4144b709bd9b",
                              "fields": {
                              "1": { "field_name":"scaff_type",
                                          "field_label":"type",
                                          "field_type":"list_from_mandatory_lists",
                                          "field_on_site_uuid":"e28cbc05-2f4b-46f5-acca-c147ae8a1db8",
                                          "values":["scaffold_type"]
                              },
                                    "2": { "field_name":"visit_date",
                                          "field_label":"visit Date",
                                          "field_type":"date",
                                          "field_on_site_uuid":"a1d5131d-d8bc-4783-8c0b-fb81f5e4a459",
                                          "default_value":"now"
                                    
                              }
                              }
                              },
                        "2": { "section_name" : "security",
                                "section_type" : "section type 1",
                                "section_on_site_uuid": "a706e588-b8f5-4b11-a711-ee1e7612bb6a",
                                 "fields": {
                                      
                                      "1": { "field_name":"visit_obstruct_access",
                                           "field_label":"obstructs access or emergency device",
                                           "field_type":"switch",
                                           "field_on_site_uuid":"3ab35154-c63a-4bf4-b085-8d6a8aa74cbe",
                                           "value_on": "oui",
                                           "value_off": "non"
                                      },
                                      
                                      "2": { "field_name":"visit_in_mobile_equipements_movement_area",
                                           "field_label":"in mobile equipements movement area",
                                           "field_type":"switch",
                                           "field_on_site_uuid":"a5f14187-3704-47b2-b667-5000c37de47e",
                                           "value_on": "oui",
                                           "value_off": "non"
                                      },
                                      
                                      "3": { "field_name":"visit_nearby_live_electric_network",
                                           "field_label":"nearby live electric network",
                                           "field_type":"switch",
                                           "field_on_site_uuid":"ac96883f-6e96-4dd9-99cc-0669022b43aa",
                                           "value_on": "oui",
                                           "value_off": "non"
                                      },
                                      
                                      
                                      
                                 }
                                },
                        "3": { "section_name" : "dimensions",
                                "section_type" : "section type 1",
                                "section_on_site_uuid": "de3b8182-df35-4c6a-9aea-8d652efd8142",
                                 "fields": {
                                      "1": { "field_name":"scaff_charge_exploitation_prevue",
                                           "field_label":"charge Exploit prévue",
                                           "field_type":"list",
                                           "field_on_site_uuid":"43f30456-0f0d-4fef-842c-01f869f85cdd",
                                           "values": [
                                               "Classe 3 (répartis 250kg/m2)",
                                               "Classe 4 et 5 (300kg\/m2>répartis<450kg\/m2)",
                                               "Classe 6 (450 Kg\/m2>répartis<600kg\/m2)",
                                               "autre(à renseigner dans commentaire)", 
                                               
                                            ] 
                                        },
                                      "2": { "field_name":"visit_scaff_conforme_notice",
                                           "field_label":"conforme notice",
                                           "field_type":"switch",
                                           "field_on_site_uuid":"fb737b8d-db58-418f-a69f-b437539cdec6",
                                           "value_on": "oui",
                                           "value_off": "non"
                                      },
                                      "3": { "field_name":"visit_date_reception_prevue",
                                           "field_label":"date réception prévue",
                                           "field_type":"date",
                                           "field_on_site_uuid":"4d83d71d-adfe-45f8-968c-5d9761f4c288",
                                           "default_value":"j+15",
                                      },
                                     "4": { "field_name": "visit_scaff_width",
                                            "field_label": "longueur",
                                           "field_type": "integer",
                                           "field_on_site_uuid":"8dd3f411-6f67-43c4-9d9d-1d420cc6bc68"
                                           },
                                     "5": { "field_name": "visit_scaff_depth",
                                           "field_label": "largeur",
                                           "field_type": "integer",
                                           "field_on_site_uuid":"0b1a49af-757f-4127-a0fb-f525d2f71f70"},
                                     "6": { "field_name": "visit_scaff_height",
                                            "field_label": "Hauteur",
                                           "field_type": "integer",
                                           "field_on_site_uuid":"29c05fa8-c1d6-4026-bd4a-356a1e0eca7b"},
                                      "7": { "field_name":"visit_scaff_nb_planchers_travail",
                                           "field_label":"nombre de planchers travail",
                                           "field_type":"list",
                                           "field_on_site_uuid":"552460e5-b326-4cba-816c-e84202f1f83c",
                                           "values": [
                                               "1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"
                                            ] 
                                    },
                                 }
                                },
                        "4": { "section_name" : "intervenants",
                                "section_type" : "section type 3",
                                "section_on_site_uuid": "b72ec40c-0194-47a0-9744-35137dde1e9d",
                                 "fields": {
                                       "1": { "field_name":"visit_user_scaffolder",
                                           "field_label":"scaffolder",
                                           "field_type":"user_from_role",
                                           "field_on_site_uuid":"1481ef60-16f5-4090-94a4-daf787ae5926",
                                           "values": ["scaffold builder"]
                                      },
                                       "2": { "field_name":"visit_signature_scaffolder",
                                           "field_label":"signature",
                                           "field_type":"signature",
                                           "field_on_site_uuid":"983287bb-62c3-42cf-86f2-f15d1b9b4204",
                                      },
                                      "3": { "field_name":"visit_user_email",
                                           "field_label":"user e-mail",
                                           "field_type":"email",
                                           "field_on_site_uuid":"aa141f92-4be6-4df9-83e0-81247b6c611b",
                                           "values": []
                                      },
                                       "4": { "field_name":"visit_signature_user",
                                           "field_label":"signature User",
                                           "field_type":"signature",
                                           "field_on_site_uuid":"47afbe06-57a3-416e-8f39-42a4916bf97e",
                                      },
                                        "5": { "field_name":"visit_user_building_coordinator",
                                           "field_label":"building coordinator",
                                           "field_type":"user_from_role",
                                           "field_on_site_uuid":"032dfe04-c8f0-4552-9cd1-248b272c7c15",
                                           "values": ["building coordinator"]
                                      },
                                       "6": { "field_name":"visit_signature_building_coordinator",
                                           "field_label":"signature",
                                           "field_type":"signature",
                                           "field_on_site_uuid":"853a16f2-7327-4317-aed4-ea8782556eb4",
                                      },
                                       "7": { "field_name":"visit_user_hse_engineer",
                                           "field_label":"HSE engineer",
                                           "field_type":"user_from_role",
                                           "field_on_site_uuid":"5a3f72df-7599-48c4-8f51-8fa6127d3a5d",
                                           "values": ["hse engineer"]
                                      },
                                       "8": { "field_name":"visit_signature_hse_engineer",
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
                                       "1": { "field_name":"visit_pictures",
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
                                    "1": { "field_name":"visit_comments",
                                          "field_label":"comments",
                                          "field_type":"paragraph",
                                          "field_on_site_uuid":"25cd9145-cd6f-422d-aab7-a25f7ba23fd4",
                                          "values":[]
                              },
                              }
                        },
                        }
                    },
                "3" :{"form_name":"commissioning",
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
                                           "field_type": "integer",
                                           "field_on_site_uuid":"6c3d5abb-484c-4fa2-910e-0fbd182a8b34"
                                           },
                                     "2": { "field_name": "commissioning_scaff_depth",
                                           "field_label": "largeur",
                                           "field_type": "integer",
                                           "field_on_site_uuid":"8389bdac-fcd4-4681-ba44-4a2bcbead81d"},
                                     "3": { "field_name": "commissioning_scaff_height",
                                            "field_label": "hauteur",
                                           "field_type": "integer",
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
                                           "field_label":"commissioning engineer",
                                           "field_type":"user_from_role",
                                           "field_on_site_uuid":"dd18e0d5-8d3a-477e-ab3d-09d5736b7ffa",
                                           "values": ["commissioning engineer"]
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
                                           "values": ["scaffold builder"]
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
            "list_statuses" : [
                  "initiated",
                  "assigned",
                  "chrono",
                  "commissionned",
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
          "site administrator",
          "coordinator",
          "operator",
          "billing manager",
          "scaffold builder",
          "building coordinator",
          "hse engineer",                                     #Health and Safety Project Coordinator
          "commissioning engineer",
          "user"
      ]
}
