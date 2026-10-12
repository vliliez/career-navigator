# Требования и зависимости

## Окружение

- Python 3.10+ (если выбран Python-стек)
- Node.js 18+ (если выбран Node.js-стек)
- Docker и docker-compose
- Git

## Зависимости (пример для Python-бэкенда)

В папке `src/api` будет файл `requirements.txt` со списком библиотек.

Пример:
- fastapi
- uvicorn
- scikit-learn
- transformers
- psycopg2-binary
- python-dotenv

## Переменные окружения

Создайте файл `.env` в корне проекта и укажите:

```env
TELEGRAM_BOT_TOKEN=ваш_токен
DATABASE_URL=postgresql://user:password@host:port/dbname
API_HOST=0.0.0.0
API_PORT=8000
