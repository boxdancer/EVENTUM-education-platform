from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import UserCreate, ShowUser
from db.dals import UserDAL
from db.session import get_db

# Создание роутера APIRouter для управления маршрутами, связанными с пользователями. Это позволяет группировать
# маршруты, которые можно потом подключить к основному приложению FastAPI.
user_router = APIRouter()


# Приватная функция создаёт нового пользователя в базе данных.
async def _create_new_user(body: UserCreate, db) -> ShowUser:
    # Открывает асинхронную сессию с базой данных с использованием SQLAlchemy
    async with db as session:
        # Начинает транзакцию, чтобы изменения в базе данных были атомарными
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                name=body.name,
                surname=body.surname,
                class_number=body.class_number,
                exam_type=body.exam_type,
                email=body.email,
                telegram=body.telegram,
            )
            return ShowUser(
                user_id=user.user_id,
                name=user.name,
                surname=user.surname,
                class_number=user.class_number,
                exam_type=user.exam_type,
                email=user.email,
                telegram=user.telegram,
                is_active=user.is_active,
            )


# путь '/' для относительного роутера user_router, для основного роутера main_api_router он выглядит как '/user'
@user_router.post('/', response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    return await _create_new_user(body, db)
