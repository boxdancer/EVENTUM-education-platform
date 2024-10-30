""" Настройки и конфигурации для проекта """
from envparse import Env

env = Env()


# Коннект к БД (postgresql+asyncpg для асинхронных подключений)(postgres:postgres - логин и пароль)
#  0.0.0.0:5432 - хост и порт, postgres - имя БД
REAL_DATABASE_URL = env.str(
    'REAL_DATABASE_URL',
    default='postgresql+asyncpg://postgres:postgres@localhost:5431/postgres'
)


# Коннект к тестовой БД, для интеграционного тестирования
TEST_DATABASE_URL = env.str(
    'TEST_DATABASE_URL',
    default='postgresql+asyncpg://postgres_test:postgres_test@localhost:5430/postgres_test'
)