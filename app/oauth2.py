from jose import JWTError, jwt 
from datetime import datetime, timedelta
from . import schemas

SECRET_KEY = "08d25e094faa6ca2516c818166b7a9563b98f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
  to_encode = data.copy()
  expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def verify_access_token(token: str, credentials_exception):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    id: str = payload.get("users_id")

    if id is None:
      raise credentials_exception
    token_data = schemas.Token(id=id)
  except JWTError:
    raise credentials_exception
 