# tablebooking

Проект сервиса бронирования столов на FastAPI.

## Запуск

1. Создайте файл `.env.docker` с переменными окружения для базы данных:

```env
DB_HOST=db
DB_PORT=5432
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=tablebooking
```

2. Соберите и запустите проект:

```docker-compose up --build```

Приложение будет доступно на http://localhost:8000
Документация OpenAPI — http://localhost:8000/docs


## Стек

- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Docker, docker-compose
- pytest (тесты)