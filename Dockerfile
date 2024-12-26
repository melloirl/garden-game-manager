FROM python:3.12-slim

# Set database and logging defaults
ENV ENVIRONMENT=prod \
    MYSQL_HOST=localhost \
    MYSQL_USER=ggm \
    MYSQL_PASSWORD=ggm \
    MYSQL_DB=ggm \
    LOG_DIR=/var/log/ggm

# Required environment variables that must be set in Railway's dashboard:
# - DISCORD_TOKEN
# - DISCORD_GUILD_ID
# - BOT_PREFIX

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
