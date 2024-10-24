# Eventum онлайн платформа

Для накатывания миграций, если файла alembic.ini еще нет, запустить в терминале:
```
alembic init migrations
```

Будет создана папка с миграциями и конфигом алембика.

- В alembic.ini задаем адрес БД, в которую накатываем миграции. (sqlalchemy.url =...)
- Переходим в папку с миграциями, открываем env.py, ищем:
```
from myapp import mymodel  
```

- Вводим: ``` alembic revision --autogenerate -m "comment text"```
- Создается миграция
- Вводим: ```alembic upgrade heads```