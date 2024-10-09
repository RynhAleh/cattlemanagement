from fastapi import FastAPI
from routes import router
from database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Замените на адрес фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создание таблиц
Base.metadata.create_all(bind=engine)

app.include_router(router)
