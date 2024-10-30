"""Модели БД SQLalchemy"""
import uuid

from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

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
