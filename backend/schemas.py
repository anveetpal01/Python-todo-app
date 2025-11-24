# model validation ke liye pydantic use hota hai
'''
API, Database mein data request tabhi lejayega agar wo schema mein hai
Request Schema: when user sends the data
Response Schema: when backend sends the data to user 
'''
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

# ---- Task Schemas ----
# Base class: common things jo ki har jagah hogi
class TaskBase(BaseModel):
    title: str
    description:Optional[str] = None
    is_completed: bool = False

# create : Jab user naya task banayega
class TaskCreate(TaskBase):
    pass

# Response: Jab hum user ko task show karenge to id or owner id bhi chaiye
class Task(TaskBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)

# ---- User Schemas ----

class UserBase(BaseModel):
    email: str
# password is required while signup
class UserCreate(UserBase):
    password: str

# response: hide password while showing profile( not return password)
class User(UserBase):
    id: int
    is_active: bool = True
    tasks: List[Task] = [] # for showing users tasks

    model_config = ConfigDict(from_attributes=True)
