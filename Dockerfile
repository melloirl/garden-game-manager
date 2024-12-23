FROM python:3.12-slim

WORKDIR /app

# Create non-root user
RUN groupadd -r botuser && useradd -r -g botuser botuser

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Create log directory and set permissions
RUN mkdir -p /var/log/ggm && \
    chown -R botuser:botuser /var/log/ggm /app

# Switch to non-root user
USER botuser

CMD ["python", "src/client.py"]
