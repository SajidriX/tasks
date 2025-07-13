from fastapi import APIRouter,Depends,Path,Body,HTTPException
from db import init_db,User,Session,Task
from bcrypt import gensalt,hashpw
from schemas import UserCreate,UserUpdate
from typing import Annotated
from Tasks.main_tasks import client

router = APIRouter

def hash_password(password):
    password.encode('utf-8')
    salt = gensalt()
    hashed_password = hashpw(password,salt)
    return hashed_password



@router.post("/users/create")
async def create_user(
    user_data:UserCreate,
    db:Session = Depends(init_db)
    ):
    hashed = hash_password(user_data.password)

    user = User(
        name = user_data.name,
        grade = user_data.grade,
        password = hashed
    )

    db.add(user)
    db.refresh(user)
    db.commit()

@router.delete("/users/delete/{name}")
async def delete_user(
    name: Annotated[str, Path(min_length=3,max_length=100)],
    db:Session = Depends(init_db)
):
    user = db.query(User).filter(User.name == name).first()
    db.delete(user)
    db.commit()

@router.patch("users/patch/{name}")
async def patch_user(
    name: Annotated[str, Path(min_length=3,max_length=100)],
    user_update: UserUpdate,
    password:Annotated[str, Body(min_length=1,max_length=100)],
    db:Session = Depends(init_db)
):
    hashed = hash_password(password)
    
    user = db.query(User).filter(User.name == name).first()
    
    if user.password == hashed:
        update_data = user_update.model_dump(exclude_unset=True)
        for field,value in update_data.items():
            setattr(user,field,value)
    if user.password != hashed:
        raise HTTPException(status_code=401,detail="Invalid password")
    
    db.refresh(user)
    db.commit()
    return user

@router.patch("/users/add_task/{name_user}/{name_task}")
async def give_task(
    name_user: Annotated[str, Path(min_length=1,max_length=100)],
    name_task:Annotated[str, Path(min_length=1,max_length=100)],
    db:Session = Depends(init_db)
):
    user = db.query(User).filter(User.name == name_user).first()
    try:
        task = db.query(Task).filter(Task.name == name_task).first()
    except:
        task = client.get(name_task)
    user.tasks = task
    db.refresh(user)
    db.commit()
    return user