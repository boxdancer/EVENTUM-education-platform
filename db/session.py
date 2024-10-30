"""Взаимодействие с БД"""
from typing import Generator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

import settings

# Создаем асинхронный движок для взаимодействия с БД, echo=True - включает вывод всех SQL-запросов в лог для отладки
engine = create_async_engine(settings.REAL_DATABASE_URL, echo=True)

# Создаем сессию для взаимодействия с БД
# expire_on_commit=False: объекты не истекают после коммита, предотвращая доп. запросы при повторном доступе к данным.
# AsyncSession — это специальный класс в SQLAlchemy, поддерживает асинхронные операции для взаимодействия с БД.
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> Generator:
    """Dependency for getting async session"""
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
