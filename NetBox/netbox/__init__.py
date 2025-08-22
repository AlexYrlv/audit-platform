from __future__ import annotations
from asyncio import get_event_loop
from logging.config import dictConfig

from fpiaioact import ActorApp
from config_fastapi import Config

from . import actors

__version__ = "0.1.0"


def application_config() -> Config:
    cfg = Config(file_path="config_fastapi.json")
    if cfg.get("logging"):
        dictConfig(cfg.extract("logging").to_dict())
    return cfg


def create_app(cfg: Config | None = None) -> ActorApp:
    cfg = cfg or application_config()
    app = ActorApp("NetBoxService", loop=get_event_loop())
    return actors.init(app)
