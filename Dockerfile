FROM python:3.12-slim

WORKDIR /app

RUN groupadd -r botuser && useradd -r -g botuser botuser

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p /var/log/ggm && \
    chown -R botuser:botuser /var/log/ggm /app

USER botuser

CMD ["python", "src/client.py"]
