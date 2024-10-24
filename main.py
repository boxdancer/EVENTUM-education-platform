from fastapi import FastAPI, HTTPException
import uvicorn
from fastapi.routing import APIRouter
from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import settings
from sqlalchemy.dialects.postgresql import UUID
import uuid
import re

from pydantic import BaseModel, EmailStr, field_validator


########################################################################
# Взаимодействие с БД
########################################################################

# создаем асинхронный движок для взаимодействия с БД, echo=True - включает вывод всех SQL-запросов в лог для отладки
engine = create_async_engine(settings.REAL_DATABASE_URL, echo=True)

# создаем сессию для взаимодействия с БД
# expire_on_commit=False: объекты не истекают после коммита, предотвращая доп. запросы при повторном доступе к данным.
# AsyncSession — это специальный класс в SQLAlchemy, поддерживает асинхронные операции для взаимодействия с БД.
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

########################################################################
# Модели БД SQLalchemy
########################################################################
# Base = declarative_base() создаёт базовый класс для всех наших моделей (таблиц).
Base = declarative_base()


# Создание таблицы users, управляемой через класс User
class User(Base):
    __tablename__ = 'users'

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(150), nullable=False)  # Максимальная длина строки 150 символов
    surname = Column(String(150), nullable=False)
    class_number = Column(Integer, nullable=True)
    exam_type = Column(String(150), nullable=True)
    email = Column(String(150), nullable=False, unique=True)
    telegram = Column(String(150), nullable=True)  # nullable=True, не обязательный параметр
    is_active = Column(Boolean(), default=True)


########################################################################
# Взаимодействие БД и бизнес-логики (создание, удаление пользователя и т.д.)
########################################################################
class UserDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
            self, name: str, surname: str, class_number: int, exam_type: str, email: str, telegram: str
    ) -> User:
        # Создаётся новый объект User, используя переданные параметры.
        new_user = User(
            name=name,
            surname=surname,
            class_number=class_number,
            exam_type=exam_type,
            email=email,
            telegram=telegram,
        )
        # добавляет нового пользователя в сессию (но не сохраняет его в базе данных сразу, до выполнения flush)
        self.db_session.add(new_user)
        # синхронизирует состояние сессии с базой данных. В отличие от commit, flush сохраняет изменения,
        # но не фиксирует транзакцию. Это позволяет получить доступ к автоматически сгенерированным значениям
        # (например, id пользователя) перед фиксацией транзакции.
        await self.db_session.flush()
        return new_user


########################################################################
# Модели API (Pydantic)
########################################################################
# Регулярка проверяет, что строка состоит только из букв и тире
LETTER_MATCH_PATTERN = re.compile(r'^[а-яА-Яa-zA-Z\-]+$')


# наследование от BaseModel позволяет использовать возможности валидации и сериализации Pydantic
class TunedModel(BaseModel):
    class Config:
        """заставляет Pydantic конвертировать все объекты(не только словари) в JSON"""
        # Указывает Pydantic, что модель может быть создана из объектов SQLAlchemy
        from_attributes = True


# Модель ответа для пользователя (поэтому наследовались от TunedModel, чтобы перегонять данные в JSON)
class ShowUser(TunedModel):
    user_id: uuid.UUID
    name: str
    surname: str
    class_number: int
    exam_type: str
    email: EmailStr
    telegram: str
    is_active: bool


# Модель обработки входящего запроса
class UserCreate(BaseModel):
    name: str
    surname: str
    class_number: int
    exam_type: str
    email: str
    telegram: str

    # Валидация для имени
    @field_validator('name')
    def validate_name(cls, value: str) -> str:
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail='Имя должно содержать только буквы'
            )
        return value

    # Валидация для фамилии
    @field_validator('surname')
    def validate_surname(cls, value: str) -> str:
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail='Фамилия должна содержать только буквы'
            )
        return value


########################################################################
# API Пути (Routes)
########################################################################
# Инициализация FastAPI-приложения
app = FastAPI(title='Онлайн платформа Eventum')

# Создание роутера APIRouter для управления маршрутами, связанными с пользователями. Это позволяет группировать
# маршруты, которые можно потом подключить к основному приложению FastAPI.
user_router = APIRouter()

# Приватная функция создаёт нового пользователя в базе данных.
async def _create_new_user(body: UserCreate) -> ShowUser:
    # Открывает асинхронную сессию с базой данных с использованием SQLAlchemy
    async with async_session() as session:
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
async def create_user(body: UserCreate) -> ShowUser:
    return await _create_new_user(body)

# Основной роутер для подключения к приложению
main_api_router = APIRouter()

# Добавляем пользовательский роутер user_router в основной main_api_router
main_api_router.include_router(user_router, prefix='/user', tags=['user'])
# Добавляем основной роутер в наше приложение
app.include_router(main_api_router)

if __name__ == '__main__':
    # запуск приложения на указанном хосту и порте
    uvicorn.run(app, host='0.0.0.0', port=8000)