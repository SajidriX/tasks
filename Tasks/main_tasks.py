from fastapi import APIRouter, Depends, HTTPException, Body, Path
from db import init_db, Task
from schemas import TaskCreate, Tasks, TaskUpdate
from typing import List, Dict, Annotated
from sqlalchemy.orm import Session
import redis

r = redis.Redis()

router = APIRouter()

@router.post("/task_create", response_model=Tasks)  # Добавил / в начале пути
async def create_task(task_data: TaskCreate, db: Session = Depends(init_db)):
    task = Task(
        name=task_data.name,
        description=task_data.description,
        priority=task_data.priority
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task  # Автоматическая конвертация благодаря from_attributes

@router.get("/tasks", response_model=List[Tasks])
async def get_tasks(db: Session = Depends(init_db)):
    tasks = db.query(Task).all()
    return tasks

@router.delete("/tasks/{id}")
async def delete_task(id: Annotated[int, Path(ge=1,le=10000)], db: Session = Depends(init_db)) -> Dict:
    task = db.query(Task).filter(Task.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"status": "Task deleted"}

@router.patch("/tasks_change/{id}", response_model=Tasks)
async def change_task(
    id: Annotated[int, Path(ge=1, le=10000)],
    task_update: TaskUpdate,  # Используем схему валидации
    db: Session = Depends(init_db)
):
    db_task = db.query(Task).filter(Task.id == id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task