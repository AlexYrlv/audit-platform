from __future__ import annotations

from asyncio import get_event_loop
from logging.config import dictConfig

from fpiaioact import ActorApp
from config_fastapi import Config
import kafkabus

from . import actors

__version__ = "0.1.0"


def application_config() -> Config:
    cfg = Config(file_path="config_fastapi.json")
    topics = cfg.extract("kafka").extract("topics")

    if cfg.get("logging"):
        dictConfig(cfg.extract("logging").to_dict())

    kafka_cfg = cfg.extract("kafka")
    kafkabus.connect(
        **kafka_cfg.get("connection").to_dict(),
        enable_consumer=True,
        enable_producer=True,
        consumer_topics=[topics.get("audit_requests")]
    )

    return cfg


def create_app(cfg: Config | None = None) -> ActorApp:
    cfg = cfg or application_config()
    app = ActorApp("DiscoveryAuditService", loop=get_event_loop())
    return actors.init(app)