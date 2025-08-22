from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from logging.config import dictConfig

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastabc import App
from config_fastapi import Config
from prometheus_fastapi_instrumentator import Instrumentator

from .actors import init_actor_app
from .api_v1 import init_api
import kafkabus


def application_config() -> Config:
    config = Config(file_path="config_fastapi.json")
    topics = config.extract("kafka").extract("topics")

    if config.get("logging") is not None:
        dictConfig(config.extract("logging").to_dict())

    kafka_cfg = config.extract("kafka")
    kafkabus.connect(
        **kafka_cfg.get("connection").to_dict(),
        enable_consumer=True,
        enable_producer=True,
        consumer_topics=[topics.get("audit_results")],
    )

    return config


def start_app() -> FastAPI:
    config = application_config()
    app = App(title=config.extract("app").get("name")).app
    app.logger = logging.getLogger("test_project")

    app.include_router(init_api())
    app.add_exception_handler(Exception, error_response)
    Instrumentator().instrument(app).expose(app)
    return app


def create_actors():
    return init_actor_app()


async def error_response(request: Request, exception: Exception):
    try:
        request.app.logger.error(f"Ошибка: {str(exception)}")
    except AttributeError:
        logging.getLogger("test_project").error(f"Ошибка: {str(exception)}")

    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exception),
            "type": type(exception).__name__,
            "path": request.url.path,
        },
    )
