from fastapi import FastAPI,HTTPException,Depends
from schemas import UserCreate,UserResponse,Token
# authentication
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from auth import(
    authenticate_user,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    oauth2_scheme,
    default_password
)
import bcrypt
# stripe
import os
import stripe

# FastAPI app
app = FastAPI()
# Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

test_database = {
    1: {"id":1,"email":"jonathan@email.com","logged_in":False,
        "password":bcrypt.hashpw(default_password.encode("utf-8"), bcrypt.gensalt())},
    2: {"id":2,"email":"sonam@email.com","logged_in":False,
        "password":bcrypt.hashpw(default_password.encode("utf-8"), bcrypt.gensalt())},
    3: {"id":3,"email":"kevin@email.com","logged_in":False,
        "password":bcrypt.hashpw(default_password.encode("utf-8"), bcrypt.gensalt())},
    4: {"id":4,"email":"richard@email.com","logged_in":False,
        "password":bcrypt.hashpw(default_password.encode("utf-8"), bcrypt.gensalt())},
    5: {"id":5,"email":"neo@email.com","logged_in":False,
        "password":bcrypt.hashpw(default_password.encode("utf-8"), bcrypt.gensalt())},
}

# welcome page
@app.get("/",tags=["Welcome Screen"])
async def welcome():
    return {"Hello":"World"}

# returns a list of all the users in the database
@app.get("/users",tags=["User Records"])
async def get_all_users():
    user_list = []
    for user in test_database:
        user_list.append(test_database[user])
    return user_list

# returns a single user by id
@app.get("/users/{id}",tags=["User Records"])
async def get_user_by_id(id:int):
    # error handling: if id does not exist
    if id not in test_database:
        raise HTTPException(status_code=404,detail="User not found")
    else:
        user = test_database[id]
        return user

# deletes a single user by id
@app.delete("/users/{id}",tags=["User Records"])
async def delete_user_by_id(id:int):
    # error handling: if id does not exist
    if id not in test_database:
        raise HTTPException(status_code=404,detail="User not found")
    else:
        current_user = test_database[id]
        del test_database[id]
        return current_user

# modifies a user by id
@app.put("/users/{id}",tags=["User Records"])
async def update_user_by_id(id:int,user: UserCreate):
    # error handling: if id does not exist
    if id not in test_database:
        raise HTTPException(status_code=404,detail="User not found")
    else:
        # get current user
        current_user = test_database[id]
        updated_user = {
            "id":current_user["id"],
            "email":user.email,
            "logged_in":current_user["logged_in"]
        }
    test_database[id]=updated_user
    return updated_user


# creates a user using pydantic schema, response model to hide ID in input field
@app.post("/users",tags=["User Records"],response_model=UserResponse)
async def create_user(user: UserCreate):
    # checks if email exists in database
    for entry in test_database.values():
        if entry["email"] == user.email:
            raise HTTPException(status_code=409,detail="User already exists")

    # find maximum id for new id in database
    max_id = 0
    for id in test_database:
        if id > max_id:
            max_id = id
    new_id = max_id+1

    # hash new password:
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())

    # create database object
    new_user = {
        "id": new_id,
        "email":user.email,
        "password": hashed_password,
        "logged_in": False
    }

    test_database[new_id]={
        "id": new_id,
        "email":user.email,
        "logged_in": False,
        "password": hashed_password,

    }

    return new_user

# login
@app.post("/login",response_model=Token,tags=["Authentication"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username,form_data.password,test_database)
    # if login credentials are not valid
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={}
        )
    # if credentials are valid
    else:
        user["logged_in"] = True

        # create access token
        access_token = create_access_token(
            data={"sub": user["email"]},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

# logout
@app.post("/logout",tags=["Authentication"])
async def logout(token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token,test_database)

    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    current_user["logged_in"] = False

    return {
        "message": f'{current_user["email"]} is now logged out',
        "user": current_user
    }

# stripe
@app.get("/stripe-test",tags=["Stripe"])
async def stripe_test():
    return {"loaded": stripe.api_key is not None}
