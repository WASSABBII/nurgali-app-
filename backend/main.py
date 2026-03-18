from fastapi import FastAPI
import redis
import os

app = FastAPI()

# Подключаемся к Redis через переменную окружения, которую даст Railway
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
r = redis.from_url(REDIS_URL)

@app.get("/")
def read_root():
    return {"status": "success", "message": "Это мой новый проект Sayat-App!"}

@app.get("/items")
def read_items():
    # Просто пример: берем данные из Redis
    try:
        keys = r.keys("*")
        return {"total_keys": len(keys), "keys": [k.decode() for k in keys]}
    except:
        return {"error": "База пока недоступна"} 
