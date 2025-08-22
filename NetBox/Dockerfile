#FROM python:3.13-slim AS builder
#
#ARG CLOUDSMITH_USER
#ARG CLOUDSMITH_TOKEN
#
#ENV PYTHONUNBUFFERED=1 \
#    POETRY_NO_INTERACTION=1 \
#    POETRY_KEYRING_ENABLED=false
#
#WORKDIR /app
#
#RUN apt-get update && \
#    apt-get install -y --no-install-recommends \
#        curl bash build-essential protobuf-compiler ca-certificates \
#    && rm -rf /var/lib/apt/lists/*
#
#RUN pip install --no-cache-dir poetry
#
#COPY pyproject.toml poetry.lock* ./
#
## Для netbox-сервиса тебе нужен dev для grpcio-tools (если генеришь .proto в build)
#RUN poetry config virtualenvs.create false \
# && poetry config http-basic.config_fastapi "$CLOUDSMITH_USER" "$CLOUDSMITH_TOKEN" \
# && poetry config http-basic.grpclnt "$CLOUDSMITH_USER" "$CLOUDSMITH_TOKEN" \
# && poetry config http-basic.kafkabus "$CLOUDSMITH_USER" "$CLOUDSMITH_TOKEN" \
# && poetry install --no-interaction --with dev --no-root
#
#COPY . .
## Если нужно — генерация прото тут (или убери, если уже сгенерено в репо)
## RUN poetry run python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. proto/netbox.proto
#
## =========================
## Stage 2: Runtime
## =========================
#FROM python:3.13-slim AS runtime
#
#ENV PYTHONUNBUFFERED=1
#WORKDIR /app
#
#COPY --from=builder /usr/local/bin/ /usr/local/bin/
#COPY --from=builder /usr/local/lib/python3.13 /usr/local/lib/python3.13
#COPY --from=builder /app /app
#
## НИКАКИХ poetry install здесь!
#CMD ["python", "manage.py"]
FROM python:3.13-slim AS builder

ARG CLOUDSMITH_USER
ARG CLOUDSMITH_TOKEN

ENV PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_KEYRING_ENABLED=false

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
      curl bash build-essential protobuf-compiler ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.8.3
ENV PATH="/root/.local/bin:${PATH}"

# 2) Создаём целевой venv проекта вне /app, чтобы bind-mount не перекрывал
RUN python -m venv /opt/venv
# Активируем venv для всех дальнейших шагов
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:/root/.local/bin:${PATH}"

# сначала только манифесты (для кеша)
COPY pyproject.toml poetry.lock* ./

# приватный репозиторий из pyproject: config_fastapi
RUN poetry config virtualenvs.create false \
 && poetry config http-basic.config_fastapi "$CLOUDSMITH_USER" "$CLOUDSMITH_TOKEN" || true \
 && poetry config http-basic.kafkabus      "$CLOUDSMITH_USER" "$CLOUDSMITH_TOKEN" || true


# синхронизируем lock с pyproject без обновления версий
RUN poetry lock --no-update --no-interaction

# УСТАНОВКА:
# если не генерируешь .proto во время build:
RUN poetry install --no-interaction --only main --no-root --sync
# если генерируешь .proto здесь, а не в runtime — используй:
# RUN poetry install --no-interaction --with dev --no-root --sync

# теперь исходники
COPY . .

# =========================
# Runtime
# =========================
FROM python:3.13-slim AS runtime
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Берём только готовое окружение
COPY --from=builder /opt/venv /opt/venv

# Активируем venv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

# Код будет подмонтирован томом в /app из compose
CMD ["python", "manage.py"]