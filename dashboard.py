from fastapi import FastAPI, Depends, HTTPException
from database import Base, engine, get_db
from passlib.context import CryptContext
from sqlalchemy.orm import Session, sessionmaker
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from models import UserInput, Users, memoTable
from schemas import UserDetails, userInfo, userInputs, UserResponse, signupDetails
from auth_utils import hash_password, verify_password, decode_access_token, create_access_token, refresh_token
from datetime import datetime


pwd_hash = CryptContext(schemes=["bcrypt"], deprecated="auto")


app = FastAPI()

security = HTTPBearer()

Base.metadata.create_all(engine)

@app.get("/")
def root():
    return {"message": "Welcome to Dashboard"}

@app.post ("/signup", response_model=UserResponse)
def sign_Up(user: signupDetails, db: Session = Depends(get_db)):
    db_user = db.query(Users).filter(Users.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    hash_pasword = hash_password(user.password)
    new_user = Users(username = user.username, password = hash_pasword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/login")
def sign_In(user: signupDetails, db: Session = Depends(get_db)):
    db_user = db.query(Users).filter(Users.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Credentials not accurate")
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Credentials not accurate")
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_bearer": "bearer", "user": db_user}

@app.post("/refresh")
def access_token_refresh(user: signupDetails, db: Session = Depends(get_db)):
    db_user = db.query(Users).filter(Users.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Credentials not accurate")
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Credentials not accurate")
    refresh_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": refresh_token, "token_bearer": "bearer", "user": db_user}


@app.patch("/details")
def user_detail_completion(user: UserDetails, db: Session = Depends(get_db), decodeAccess: dict = Depends(decode_access_token)):
    userName = decodeAccess.get("sub")    
    db_user = db.query(Users).filter(Users.username == userName).first() 
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")   
    for field, values in user.model_dump(exclude_unset=True, exclude={"username"}).items():
        if field == "password":
            values = hash_password(user.password)
        print(setattr(db_user, field, values))
        db.commit()
        db.refresh(db_user)
    return {"message" : "User details updated"}

@app.get("/getDetails/{user_name}", response_model=UserDetails)
def get_Details(db: Session = Depends(get_db), 
                decodeAccess: dict = Depends(decode_access_token)):
    userName = decodeAccess.get("sub")

    query = db.query(Users).filter(Users.username == userName).first()
    if not query:
        raise HTTPException(status_code=404, detail="User not found")
    return query

@app.get("/get_Memo/{memoTitle}")
def get_Memo(memoTitle: str, 
             db: Session = Depends(get_db), 
             decodeAccess: dict = Depends(decode_access_token)):
    userName = decodeAccess.get("sub")

    query = db.query(Users).filter(Users.username == userName).first()
    if not query:
        raise HTTPException(status_code=404, detail="User not found")

    memoInfo = db.query(memoTable).filter(memoTable.title == memoTitle).first()
    if not memoInfo:
        return {"message": "memo not found"}

    return { memoInfo.title : memoInfo.memo }


@app.post("/inputMemo")
def input_Memo(
    user_input: userInputs,
    decode_access: dict = Depends(decode_access_token),
    db: Session = Depends(get_db)
):
    # 1️⃣ Get the username from the access token
    username = decode_access.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")

    # 2️⃣ Fetch the logged-in user from the database
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        raise HTTPException(status_code=403, detail="User not found")

    # 3️⃣ Update memo fields
    new_memo = memoTable(title = user_input.memoTitle,
                        memo = user_input.memo,
                        memoTime = datetime.now()
    )
    # 4️⃣ Save changes
    db.add(new_memo)
    db.commit()
    db.refresh(new_memo)

    return {"message": "Memo updated successfully"}

@app.get ("/getAllMemo")
def get_all_memo(db: Session = Depends(get_db), decodeAccess: dict = Depends(decode_access_token)):
    userName = decodeAccess.get("sub")

    memoList = []

    db_all = db.query(Users).filter(Users.username == userName).all()
    db_memo = db.query(memoTable).all()
    for memo in db_memo:
        memoList.append({
            "memo": memo.memo,
            "title": memo.title,
            "time": memo.memoTime 
            })
    return {"user memos" : memoList }

@app.delete ("/deleteMemo")
def delete_Memo(memoDel: str, db: Session = Depends(get_db), decodeAccess: dict = Depends(decode_access_token)):
    single_memo = db.query(memoTable).filter(memoTable.title == memoDel).first()
    if not single_memo:
        return {"message": "memo not found"}
    db.delete(single_memo)
    db.commit()
    return {"message": "memo deleted"}
    

@app.get("/decode")
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if not credentials:
        raise HTTPException(status_code=status.HTTP_403_UNAUTHORIZED, detail="credentials missing")  
    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid or expired token")

    return {"message": "protected route accessed", "user":["sub"]}