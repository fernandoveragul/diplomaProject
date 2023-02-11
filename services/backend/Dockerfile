FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1

RUN mkdir /app && chmod -R 777 /app
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000


CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

#CMD ["alembic", "revision", "--autogenerate", "-m", "'init'"]
#CMD ["alembic", "upgrade", "head"]