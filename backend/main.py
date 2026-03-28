from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import redis
import os
from fastapi import Request
app = FastAPI()

# РАЗРЕШАЕМ ФРОНТЕНДУ ДОСТУП
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# СОВЕТ DEVOPS: Сначала ищем переменную Railway, 
# если её нет — пробуем докер-имя 'db', если и его нет — 'localhost'
REDIS_URL = os.getenv("REDIS_URL", os.getenv("DATABASE_URL", "redis://localhost:6379"))
r = redis.from_url(REDIS_URL)

@app.get("/health")
def health_check():
    try:
        r.ping() # Проверяем реальную связь с базой
        return {"status": "ok", "database": "connected", "user": "Nurgali"}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "details": str(e)}

@app.get("/api/data")
def get_data():
    # Получаем все ключи
    keys = r.keys("*")
    # Декодируем их из байтов в обычный текст
    items = [k.decode() for k in keys]
    return {"items": items, "count": len(items)}


@app.post("/api/add")
async def add_item(name: str, request: Request):
    # Railway передает реальный IP в этом заголовке
    real_ip = request.headers.get("X-Forwarded-For")
    
    # Если заголовка нет (например, тестируешь локально), берем обычный адрес
    if not real_ip:
        real_ip = request.client.host
        
    print(f"--- НОВАЯ ЗАПИСЬ ---")
    print(f"Имя: {name}")
    print(f"Реальный IP пользователя: {real_ip}")
    
    r.set(name, f"User: {name}, IP: {real_ip}")
    return {"status": "ok", "your_ip": real_ip}

@app.post("/api/add")
def add_item(name: str):
    # Сохраняем в Redis: Ключ — имя, Значение — дата/время или просто текст
    r.set(name, "added_by_nurgali")
    return {"message": f"Элемент {name} успешно добавлен в Redis!"}
