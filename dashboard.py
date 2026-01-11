from fastapi import FastAPI, Depends, HTTPException
from database import Base, engine, get_db
from passlib.context import CryptContext
from sqlalchemy.orm import Session, sessionmaker
from models import UserInput, Users
from schemas import UserDetails, userEdit, userInputs, UserResponse, signupDetails


pwd_hash = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

Base.metadata.create_all(engine)

@app.get("/")
def root():
    return {"message": "Welcome to Dashboard"}

@app.post ("/signup", response_model=UserResponse)
def signUp(user: signupDetails, db: Session = Depends(get_db)):
    db_user = db.query(Users).filter(Users.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    hash_pasword = pwd_hash.hash(user.password)
    new_user = Users(username = user.username, password = hash_pasword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post ("/signin")
async def signIn(user: signupDetails, db: Session = Depends(get_db)):
    existing = db.query(Users).filter(Users.username == user.username).first()
    if not existing or not pwd_hash.verify(user.password, existing.password):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User sucessfully logged in"}



@app.post("/details/{user_name}")
def user_detail_completion(user_name, user: userInputs, db: Session = Depends(get_db)):    
    db_user = db.query(Users).filter(Users.username == user_name).first() 
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")   
    for field, values in user.model_dump(exclude_unset=True, exclude={"username"}).items():
        if field == "password":
            values = pwd_hash.hash(user.password)
        print(setattr(db_user, field, values))
        db.commit()
        db.refresh(db_user)
    return {"message" : "User details updated"}

@app.get("/getDetails/{user_id}")
def getDetails(user_id, db: Session = Depends(get_db)):
    query = db.query(Users).filter(Users.id == user_id).first()
    if not query:
        raise HTTPException(status_code=404, detail="User not found")
    return query

@app.post("/myBio/{user_name}")
def myBio(user_name, user_bio: userInputs, db: Session = Depends(get_db)):
    db_bio = db.query(Users).filter(Users.username == user_name).first()
    if not db_bio:
        raise HTTPException(status_code=400, detail="user does not exist")
    db_bio.bio = user_bio.bio
    db.commit()
    db.refresh(db_bio)
    return {"message" : "Bio updated sucessfully"}