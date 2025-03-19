FROM python:3.9

RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --use-pep517 mysqlclient==2.2.0

RUN pip install -U poetry==1.8.4

WORKDIR /app

COPY poetry.lock pyproject.toml .
RUN poetry install --no-root --only main

COPY  . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
