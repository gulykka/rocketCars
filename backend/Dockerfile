FROM python:3.9-slim

WORKDIR /app

# Копируем зависимости
COPY ./backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы
COPY ./backend/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]