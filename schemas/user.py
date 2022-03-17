def userEntity(item) -> dict:
    return {
        'id': str(item['_id']),
        'email': item["email"],
        'password': item["password"],
    }

def usersEntity(items) -> list:
    return [userEntity(item) for item in items] 


def serializeDict(a) -> dict:
    return {**{i:str(a[i]) for i in a if i=='_id'},**{i:a[i] for i in a if i!='_id'}}

def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]