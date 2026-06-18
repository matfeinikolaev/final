# HR Vacancy Service

Бэкенд сервис для HR, позволяющий работать с вакансиями и кандидатами, а также предоставляющий HR-аналитику.

## Стек технологий

- **Python 3.11** + **FastAPI** - асинхронный веб-фреймворк
- **SQLAlchemy 2.0** (async) + **asyncpg** - ORM и драйвер PostgreSQL
- **Alembic** - миграции базы данных
- **Pydantic v2** - валидация данных
- **python-jose** + **bcrypt** - JWT авторизация
- **Pytest** + **httpx** + **aiosqlite** - тестирование
- **Docker** + **Docker Compose** - контейнеризация

## Структура проекта

```
app/
├── api/
│   ├── deps.py                 # Зависимости (текущий пользователь)
│   └── v1/
│       ├── api.py              # Роутер v1
│       └── endpoints/
│           ├── applications.py # Управление подачами резюме на вакансии
│           ├── auth.py         # Регистрация, логин, смена пароля, refresh
│           ├── users.py        # Управление пользователями
│           ├── categories.py   # Категории вакансий
│           ├── jobs.py         # Должности
│           ├── vacancies.py    # Вакансии + статистика
│           └── resumes.py      # Резюме соискателей
├── core/
│   ├── config.py               # Настройки приложения
│   ├── database.py             # Подключение к БД
│   └── security.py             # Хэширование паролей, JWT
├── crud/
│   └── user_crud.py            # CRUD для пользователей
├── models/                     # SQLAlchemy модели
├── schemas/                    # Pydantic схемы
└── main.py                     # Точка входа
migrations/                     # Alembic миграции
tests/                          # Pytest тесты
```

## Модели данных

| Таблица      | Поля                                                                 |
|--------------|----------------------------------------------------------------------|
| `users`      | id, email, hashed_password, first_name, last_name, is_active, is_superuser |
| `categories` | id, name                                                             |
| `jobs`       | id, title, category_id                                               |
| `vacancies`  | id, title, description, category, status (OPEN/CLOSED), job_id      |
| `resumes`    | id, applicant_name, applicant_email, description, category, status, job_id |

## API эндпоинты

### Auth `/api/v1/auth`
| Метод | Путь               | Описание                        |
|-------|--------------------|---------------------------------|
| POST  | `/register`        | Регистрация нового пользователя |
| POST  | `/login`           | Получение токенов               |
| POST  | `/refresh`         | Обновление access токена        |
| POST  | `/change-password` | Смена пароля (требует токен)    |
| GET   | `/me`              | Данные текущего пользователя    |

### Vacancies `/api/v1/vacancies`
| Метод | Путь                    | Описание                              |
|-------|-------------------------|---------------------------------------|
| GET   | `/`                     | Список вакансий (фильтры: category, status, job_id) |
| GET   | `/{id}`                 | Получить вакансию                     |
| GET   | `/{id}/stats`           | Статистика кандидатов на вакансию     |
| POST  | `/`                     | Создать вакансию (superuser)          |
| PATCH | `/{id}`                 | Обновить вакансию (superuser)         |
| POST  | `/{id}/close`           | Закрыть вакансию (superuser)          |
| DELETE| `/{id}`                 | Удалить вакансию (superuser)          |

### Resumes `/api/v1/resumes`
| Метод | Путь   | Описание                                          |
|-------|--------|---------------------------------------------------|
| GET   | `/`    | Список резюме (фильтры: category, status, job_id) |
| GET   | `/{id}`| Получить резюме                                   |
| POST  | `/`    | Создать резюме (авторизованный пользователь)      |
| PATCH | `/{id}`| Обновить резюме                                   |
| DELETE| `/{id}`| Удалить резюме                                    |

### Jobs `/api/v1/jobs` и Categories `/api/v1/categories`
CRUD операции, создание/изменение/удаление - только superuser.

## Запуск

### Локально через Docker Compose

```bash
# Скопировать и настроить переменные окружения
cp .env.example .env

# Запустить (миграции применяются автоматически)
docker compose up --build
```

Приложение будет доступно на http://localhost:8000  
Документация: http://localhost:8000/docs

### Для разработки (с hot-reload)

```bash
docker compose -f docker-compose.local.yml up --build
```

### Запуск без Docker

```bash
pip install -r requirements.txt

# Создать базу данных (если не существует)
python create_db.py

# Применить миграции
alembic upgrade head

# Запустить сервер
uvicorn app.main:app --reload
```

## Тесты

Тесты используют SQLite in-memory - PostgreSQL не нужен.

```bash
pip install -r requirements.txt
pytest
```

Для отчёта о покрытии:

```bash
pip install pytest-cov
pytest --cov=app --cov-report=term-missing
```

## Создание суперпользователя

После запуска приложения зарегистрируйтесь через `/api/v1/auth/register`, затем вручную установите `is_superuser=true` в БД:

```sql
UPDATE users SET is_superuser = true WHERE email = 'your@email.com';
```
