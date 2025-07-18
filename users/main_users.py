from fastapi import APIRouter, Depends, Path, Body, HTTPException,Form
from db import init_db, User, Session, Task
from bcrypt import gensalt, hashpw, checkpw
from schemas import UserCreate, UserUpdate
from typing import Annotated
from Tasks.main_tasks import client

router = APIRouter()  

def hash_password(password: str) -> bytes:
    password_bytes = password.encode('utf-8')
    salt = gensalt()
    hashed_password = hashpw(password_bytes, salt)
    return hashed_password

def verify_password(stored_password, input_password):
   if checkpw(stored_password,input_password):
       return True
   else:
       return False

@router.post("/users_create")
async def create_user(
    user_data: Annotated[UserCreate,Form()],
    db: Session = Depends(init_db)
):
    hashed = hash_password(user_data.password)

    if db.query(User).filter(User.name == user_data.name).first():
        raise HTTPException(status_code=400, detail="User already exists")
    
    user = User(
        name=user_data.name,
        grade=user_data.grade,
        password=hashed
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/users_delete")
async def delete_user(
    name: Annotated[str, Form(min_length=3, max_length=100)],
    db: Session = Depends(init_db)
):
    user = db.query(User).filter(User.name == name).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}  

@router.patch("/users_patch")
async def patch_user(
    name: Annotated[str, Form(min_length=3, max_length=100)],
    user_update: Annotated[UserUpdate, Form()],
    password: Annotated[str, Form(min_length=1, max_length=100)],
    db: Session = Depends(init_db)
):
    user = db.query(User).filter(User.name == name).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    
    if verify_password(user.password.encode(),password) == True:
    
        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field == "password":  
                value = hash_password(value)
                setattr(user, field, value)
    
                db.commit()
                db.refresh(user)
                return user
    else:
        raise HTTPException(status_code=403,detail="Invalid password")
    
    return password

@router.patch("/users_add_task/")
async def give_task(
    name_user: Annotated[str, Form(min_length=1, max_length=100)],
    name_task: Annotated[str, Form(min_length=1, max_length=100)],
    db: Session = Depends(init_db)
):
    user = db.query(User).filter(User.name == name_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        task = db.query(Task).filter(Task.name == name_task).first()
        if not task:
            task = client.get(name_task)
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
    if user.tasks is None:
        user.tasks = []
    if isinstance(user.tasks, str):
        user.tasks = [user.tasks]
    user.tasks.append(task.name if hasattr(task, 'name') else task)
    
    try:
        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    return user
