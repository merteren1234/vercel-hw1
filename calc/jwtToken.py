from jose import JWTError, jwt

SECRET_KEY="deadbeef"
ALGORITHM="HS256"

def create_access_token(username):
    return jwt.encode({'username':username},SECRET_KEY,algorithm=ALGORITHM)

def verification(token):
    try:
        x=jwt.decode(token,SECRET_KEY)
        return {"stat":1,"token":x}
    except:
        return {"stat":0} 
