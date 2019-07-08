oxide =    {"name": "not real name", "age": "school",     "pfp": "cat",     "position": "mod",        "speciality": ["maths", "haskell"],         "id": 341171182227161088}
shirious = {"name": "not real name", "age": "job",        "pfp": "",        "position": "admin",      "speciality": ["ex owner"],                 "id": 270898185961078785}
stark =    {"name": "not real name", "age": "graduation", "pfp": "avenger", "position": "",           "speciality": ["panoti"],                   "id": 456331309304905730}
kueen =    {"name": "not real name", "age": "graduation", "pfp": "anime",   "position": "admin",      "speciality": ["owner"],                    "id": 247386559450578954}
pixie =    {"name": "not real name", "age": "job",        "pfp": "",        "position": "admin",      "speciality": ["trap", "admin"],            "id": 249395897497157632}
hannah =   {"name": "real name",     "age": "graduation", "pfp": "",        "position": "",           "speciality": ["attention"],                "id": 390072368120332289}
yash =     {"name": "real name",     "age": "graduation", "pfp": "cat",     "position": "IU Bot dev", "speciality": [],                           "id": 388984732156690433}
ekansh =   {"name": "real name",     "age": "school",     "pfp": "",        "position": "IU Bot dev", "speciality": ["cycle gang"],               "id": 315728369369088003}
uday =     {"name": "real name",     "age": "graduation", "pfp": "",        "position": "IU Bot dev", "speciality": [],                           "id": 443961507051601931}
ketan =    {"name": "real name",     "age": "school",     "pfp": "",        "position": "",           "speciality": ["communism"],                "id": 279318185524723712}
surbhi =   {"name": "real name",     "age": "graduation", "pfp": "anime",   "position": "mod",        "speciality": ["bts", "anime"],             "id": 361521098111844352}
juzzou =   {"name": "not real name", "age": "school",     "pfp": "anime",   "position": "mod",        "speciality": ["haveli", "anime"],          "id": 444896160105103361}
frost =    {"name": "not real name", "age": "graduation", "pfp": "anime",   "position": "admin",      "speciality": ["lurk", "anime"],            "id": 269678631050018826}
nits =     {"name": "not real name", "age": "graduation", "pfp": "anime",   "position": "",           "speciality": ["meme"],                     "id": 422137814671425556}
sun =      {"name": "not real name", "age": "graduation", "pfp": "anime",   "position": "admin",      "speciality": ["medical"],                  "id": 270125856679002113}
sky =      {"name": "not real name", "age": "graduation", "pfp": "avenger", "position": "",           "speciality": ["torrent"],                  "id": 398419629606830082}



personalities = [oxide, shirious, stark, kueen, pixie, hannah, yash, ekansh, uday, ketan, surbhi, juzzou, frost, nits, sun, sky]

given = {"name": {"real name": False, "not real name": True}, "age": {"school": False, "graduation": True, "job": False}, "pfp": {"anime": False, "cat": False, "avenger": True}, "speciality": ["torrent"], "id": 398419629606830082}



def response_logic(resp: dict, given: dict):

    if resp["name"]["real name"] == False and resp["name"]["not real name"] == True:
        given["name"] = "not real name"
    elif resp["name"]["not real name"] == False and resp["name"]["real name"] == True:
        given["name"] = "real name"
    else:
        return "Invaild Response!"

    if resp["age"]["school"] == True and resp["age"]["graduation"] == False and resp["age"]["job"] == False:
        given["age"] = "school"
    elif resp["age"]["cat"] == False and resp["pfp"]["graduation"] == True and resp["age"]["job"] == False:
        given["age"] = "graduation"
    elif resp["age"]["cat"] == False and resp["pfp"]["graduation"] == False and resp["age"]["job"] == True:
        given["name"] = "job"
    else:
        return "Invaild Response!"

    if resp["pfp"]["cat"] == False and resp["pfp"]["anime"] == False and resp["pfp"]["avenger"] == False:
        given["pfp"] = ""
    elif resp["pfp"]["cat"] == True and resp["pfp"]["anime"] == False and resp["pfp"]["avenger"] == False:
        given["pfp"] = "cat"
    elif resp["pfp"]["cat"] == False and resp["pfp"]["anime"] == True and resp["pfp"]["avenger"] == False:
        given["pfp"] = "anime"
    elif resp["pfp"]["cat"] == False and resp["pfp"]["anime"] == False and resp["pfp"]["avenger"] == True:
        given["pfp"] = "avenger"
    else:
        return "Invaild Response!"

    if resp["position"]["admin"] == False and resp["pfp"]["mod"] == False and resp["pfp"]["IU Bot dev"] == False:
        given["postion"] = ""
    elif resp["posiion"]["admin"] == True and resp["pfp"]["mod"] == False and resp["pfp"]["IU Bot dev"] == False:
        given["position"] = "admin"
    elif resp["position"]["admin"] == False and resp["pfp"]["mod"] == True and resp["pfp"]["IU Bot dev"] == False:
        given["position"] = "mod"
    elif resp["position"]["admin"] == False and resp["pfp"]["mod"] == False and resp["pfp"]["IU Bot dev"] == True:
        given["position"] = "IU Bot dev"
    else:
        return "Invaild Response!"



def sortify(given: dict):
    return list(filter(createFilter(given), personalities))[0]["id"]


def createFilter(inputs: dict):
    response_logic(inputs, inputs)
    def newFilter(personality):
        for token, value in personality.items():
            if type(inputs[token]) is not list:
                if value != inputs[token]:
                    return False
            else:
                for inputVal in inputs[token]:
                    if inputVal not in value or len(inputs[token]) != len(value):
                        return False
        return True
    return newFilter
