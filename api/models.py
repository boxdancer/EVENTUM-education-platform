"""Модели API (Pydantic)"""
import re
import uuid

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator

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
