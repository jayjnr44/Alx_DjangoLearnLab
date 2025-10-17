# Simple Dockerfile for Django deployment
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

# collectstatic (assumes env vars are set in container entrypoint)
RUN python manage.py collectstatic --noinput || true

CMD ["gunicorn", "social_media_api.wsgi:application", "--bind", "0.0.0.0:8000"]
