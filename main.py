from fastapi import FastAPI, Query, Body, Path, Header, Cookie, File, UploadFile, Depends, BackgroundTasks
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from schemas import Tasks
from db import init_db, Base,engine
from Tasks.main_tasks import router as task_router
import uvicorn
from users.main_users import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Создаем таблицы при старте
    print("🟢 Создаем таблицы в БД...")
    Base.metadata.create_all(bind=engine)
    
    # 2. Здесь работает приложение
    yield
    
    # 3. Закрываем соединения при завершении
    print("🔴 Закрываем соединение с БД...")
    engine.dispose()

app = FastAPI(lifespan = lifespan)

origins = [
    "http://127.0.0.1:1488",  # Основной домен API
    "http://localhost:1488",   # Альтернативный адрес
    "http://localhost:3000",   # Для фронтенда (React/Vue)
    "http://127.0.0.1:3000",   # Альтернативный адрес фронтенда
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
html = 'index.html'

@app.get("/")
async def main_page():
    return FileResponse(html)


app.include_router(task_router)
app.include_router(user_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port = 1488)
