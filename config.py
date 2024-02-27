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
                              "canceled"
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
                        "1": { "section_name" : "User",
                              "section_type" : "section type 1",
                              "section_on_site_uuid": "ef637435-30fe-4a3f-941f-f29a8df8f865",
                              "fields": {
                              "1": { "field_name":"contractor",
                                          "field_label":"Contractor",
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
                        "2": { "section_name" : "Specifications",
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
                        "3": { "section_name" : "Description",
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
                        "4": { "section_name" : "Medias",
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
                        "1": { "section_name" : "Techniques",
                              "section_type" : "section type 1",
                              "section_on_site_uuid": "11b19f92-b590-44d5-b29c-4144b709bd9b",
                              "fields": {
                              "1": { "field_name":"scaff_type",
                                          "field_label":"Type",
                                          "field_type":"list_from_mandatory_lists",
                                          "field_on_site_uuid":"e28cbc05-2f4b-46f5-acca-c147ae8a1db8",
                                          "values":["scaffold_type"]
                              },
                                    "2": { "field_name":"visit_date",
                                          "field_label":"Visit Date",
                                          "field_type":"date",
                                          "field_on_site_uuid":"a1d5131d-d8bc-4783-8c0b-fb81f5e4a459",
                                          "default_value":"now"
                                    
                              }
                              }
                              },
                        "2": { "section_name" : "Security",
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
                        "3": { "section_name" : "Dimensions",
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
                        "4": { "section_name" : "Intervenants",
                                "section_type" : "section type 3",
                                "section_on_site_uuid": "b72ec40c-0194-47a0-9744-35137dde1e9d",
                                 "fields": {
                                       "1": { "field_name":"visit_user_scaffolder",
                                           "field_label":"Scaffolder",
                                           "field_type":"user_from_role",
                                           "field_on_site_uuid":"1481ef60-16f5-4090-94a4-daf787ae5926",
                                           "values": ["scaffolder"]
                                      },
                                       "2": { "field_name":"visit_signature_scaffolder",
                                           "field_label":"Signature",
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
                                           "field_label":"Signature User",
                                           "field_type":"signature",
                                           "field_on_site_uuid":"47afbe06-57a3-416e-8f39-42a4916bf97e",
                                      },
                                        "5": { "field_name":"visit_user_building_coordinator",
                                           "field_label":"Building coordinator",
                                           "field_type":"user_from_role",
                                           "field_on_site_uuid":"032dfe04-c8f0-4552-9cd1-248b272c7c15",
                                           "values": ["building_coordinator"]
                                      },
                                       "6": { "field_name":"visit_signature_building_coordinator",
                                           "field_label":"Signature",
                                           "field_type":"signature",
                                           "field_on_site_uuid":"47afbe06-57a3-416e-8f39-42a4916bf97e",
                                      },
                                 }
                                 
                         },
                        "5": { "section_name" : "Medias",
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
                        "6": { "section_name" : "Commentaires",
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
                  "canceled"
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
        
    },
    "roles": [
          "admin",
          "site administrator",
          "coordinator",
          "operator",
          "billing manager",
          "scaffolder builder",
          "building_coordinator",
          "hse engineer",                                     #Health and Safety Project Coordinator
          "commissioning engineer"
      ]
}
