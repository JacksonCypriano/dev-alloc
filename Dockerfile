FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install celery redis python-dotenv

COPY . /app/

RUN mkdir -p /app/static

RUN python manage.py collectstatic --noinput

EXPOSE 8000

COPY .env /app/.env

CMD ["sh", "-c", "python wait_for_db.py && python manage.py runserver 0.0.0.0:8000"]
