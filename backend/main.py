from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from jose import JWTError, jwt
import models, schemas, auth, database

# 1. Database Tables Create Karna
# Ye line check karegi ki tables hain ya nahi. Agar nahi hain, to bana degi.
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Sirf in links ko allow karo
    allow_credentials=True,
    allow_methods=["*"],     # Saare methods (GET, POST, DELETE) allow karo
    allow_headers=["*"],
)
# 2. Database Session Manager (Dependency)
# Ye har request ke liye DB kholta hai aur request khatam hone par band karta hai.
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 3. Authentication Dependency (The Gatekeeper)
# Ye check karta hai ki User ke paas valid Token hai ya nahi.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Token decode karna
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # DB mein check karna ki user exist karta hai ya nahi
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# 1. Signup Route
@app.post("/signup", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Pehle check karo email already hai kya?
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Password hash karke save karo
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 2. Login Route
@app.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # User dhundo
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    # Password match karo
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Token banao
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# 3. Create Task (Secure)
@app.post("/tasks", response_model=schemas.Task)
def create_task(
    task: schemas.TaskCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user) # Ye line user verify karegi
):
    # Magic: Hum task ke 'owner_id' mein current user ki ID daal rahe hain
    new_task = models.Task(**task.model_dump(), owner_id=current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# 4. Get My Tasks (Secure)
@app.get("/tasks", response_model=List[schemas.Task])
def read_tasks(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Sirf WAHI tasks lao jiska owner current user hai
    tasks = db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()
    return tasks

# backend/main.py mein niche add karein

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_update: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    
    # 1. Database mein task dhundo (User ID filter ke saath)
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    
    # 2. Agar task nahi mila (ya kisi aur ka hai)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # 3. Status update karo
    task.is_completed = task_update.is_completed
    db.commit()
    db.refresh(task)
    
    return task