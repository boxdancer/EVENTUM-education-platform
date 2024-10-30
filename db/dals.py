"""Взаимодействие БД и бизнес-логики (создание, удаление пользователя и т.д.)"""
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User


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
        # Синхронизирует состояние сессии с базой данных. В отличие от commit, flush сохраняет изменения,
        # но не фиксирует транзакцию. Это позволяет получить доступ к автоматически сгенерированным значениям
        # (например, id пользователя) перед фиксацией транзакции.
        await self.db_session.flush()
        return new_user
