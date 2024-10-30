"""API Пути (Routes)"""
import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
from api.handlers import user_router

# Инициализация FastAPI-приложения
app = FastAPI(title='Онлайн платформа Eventum')

# Основной роутер для подключения к приложению
main_api_router = APIRouter()

# Добавляем пользовательский роутер user_router в основной main_api_router
main_api_router.include_router(user_router, prefix='/user', tags=['user'])
# Добавляем основной роутер в наше приложение
app.include_router(main_api_router)

if __name__ == '__main__':
    # запуск приложения на указанном хосту и порте
    uvicorn.run(app, host='0.0.0.0', port=8000)
