
dataCompany =  {
                "kysoe": {
                     "yannick.simon@gmail.com":  "12345678",
                      "toto@toto.com":            "12345678",
                      "yannick.simon@kysoe.com":  "12345678"
                }
    }
    
    

for company, itemsUser in dataCompany.items():
    for user, email in itemsUser.items():
        print(company, user, email)
    
        