FROM python:3.12-slim-bookworm

RUN adduser --disabled-password --gecos "" appuser

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R appuser:appuser /app

USER appuser

CMD ["python", "-m", "main"]