oxide = {"name": "not real name", "age": "school", "pfp": "cat", "speciality": ["maths", "haskell", "mod"], "id": 1}
shirious = {"name": "not real name", "age": "job", "pfp": "none", "speciality": ["ex owner", "admin"], "id": 1}
stark = {"name": "not real name", "age": "graduation", "pfp": "none", "speciality": ["panoti", "js"], "id": 1}
kueen = {"name": "not real name", "age": "graduation", "pfp": "anime", "speciality": ["owner", "admin"], "id": 1}
pixie = {"name": "not real name", "age": "job", "pfp": "none", "speciality": ["trap", "admin"], "id": 1}
hannah = {"name": "real name", "age": "graduation", "pfp": "none", "speciality": "attention", "id": 1}
yash = {"name": "real name", "age": "graduation", "pfp": "cat", "speciality": ["bot dev", "py"], "id": 1}
ekansh = {"name": "real name", "age": "school", "pfp": "none", "speciality": ["cycle gang", "bot dev", "py"], "id": 1}
uday = {"name": "real name", "age": "graduation", "pfp": "none", "speciality": ["bot dev", "engineer", "py"], "id": 1}
ketan = {"name": "real name", "age": "school", "pfp": "none", "speciality": "communism", "id": 1}
surbhi = {"name": "real name", "age": "graduation", "pfp": "anime", "speciality": ["bts", "anime", "mod", "js"], "id": 1}
juzzou = {"name": "not real name", "age": "school", "pfp": "anime", "speciality": ["haveli", "anime", "mod"], "id": 1}
frost = {"name": "not real name", "age": "graduation", "pfp": "anime", "speciality": ["lurk", "anime", "admin"], "id": 1}
nits = {"name": "not real name", "age": "graduation", "pfp": "anime", "speciality": "bjp", "id": 1}
sun = {"name": "not real name", "age": "graduation", "pfp": "anime", "speciality": ["py", "medical", "admin"], "id": 1}
sky = {"name": "not real name", "age": "graduation", "pfp": "none", "speciality": ["js"], "id": 1}

personalities = [oxide, shirious, stark, kueen, pixie, hannah, yash, ekansh, uday, ketan, surbhi, juzzou, frost, nits, sun, sky]
sort = []

#real name - 6
#anime pfp - 5
#school - 3
#not real name - 9
#cat pfp - 2
#graduation - 9

def calculate(self, array):
    return

def sortify(self, given):
    for personality in  personalities:
        for token, value in personality:
            if type(given) is not list:
                if token and value is given:
                    sort.append(personality)
            else:
                if given in token:
                    sort.append(personality)