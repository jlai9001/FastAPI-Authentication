from datetime import datetime,timedelta,timezone
import bcrypt
import jwt
from fastapi.security import OAuth2PasswordBearer

# authentication credentials
SECRET_KEY = "secret_random_generated_characters"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
default_password = "password"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")



# take clear text and hash it using bcrypt
def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

# compare plain password word hashed password
def verify_password(plain_password:str,hashed_password:bytes) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password
    )

# authenticates user and returns user information in the database
def authenticate_user(email:str, password:str, test_database: dict):
    for user in test_database.values():
        # check if name matches with input
        if user["email"] == email:
            # gets password from fake_passwords dictionary
            hashed_password = user["password"]

            # compares cleartext password with hashed cleartext
            if hashed_password != None and verify_password(password,hashed_password) == True:
                return user
    # no user matches
    return None

# creates access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    # expiry logic
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# decode JWT token
def get_current_user(token: str, test_database: dict):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        # Read the username from the "sub" field
        username = payload.get("sub")
        # If token does not contain a username, fail
        if username is None:
            return None
    # If token is invalid, fail
    except jwt.InvalidTokenError:
        return None
    # Find the valid user
    for user in test_database.values():
        if user["email"] == username:
            return user

    # Valid token, but longer exists in database
    return None
