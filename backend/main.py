from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import redis
import os

app = FastAPI()

# РАЗРЕШАЕМ ФРОНТЕНДУ ДОСТУП
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # В реальном проекте тут будет адрес твоего сайта
    allow_methods=["*"],
    allow_headers=["*"],
)

# Было: REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
# Стало:
REDIS_URL = os.getenv("REDIS_URL", "redis://db:6379")
r = redis.from_url(REDIS_URL)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Nurgali, system is up!"}

@app.get("/api/data")
def get_data():
    # Просто отдаем список ключей из базы
    keys = r.keys("*")
    items = [k.decode() for k in keys]
    return {"items": items, "count": len(items)}

@app.post("/api/add")
def add_item(name: str):
    # Добавляем данные в базу
    r.set(name, "added_by_user")
    return {"message": f"Элемент {name} добавлен!"}
