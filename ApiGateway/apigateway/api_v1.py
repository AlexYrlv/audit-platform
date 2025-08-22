from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_200_OK
from config_fastapi import Config

from .controls import TargetsControl
from .baseclasses import BaseAPI, BaseResource
from .constants import API_PREFIX, API_NAME
from .exceptions import BadRequestHTTPError
from .structures import AuditRunRequest
from .kafka import KafkaPC


def init_api():
    api = BaseAPI(name=API_NAME, url_prefix=API_PREFIX)
    api.new_routes({
        "/audit/run": AuditRunResource,
        "/audit/targets": AuditTargetsResource,
    })
    return api.router


class AuditRunResource(BaseResource):
    config = Config(section="kafka.topics")

    def __init__(self):
        self.kafka = KafkaPC()

    async def post(self, request: Request) -> JSONResponse:
        if not (data := await request.json()):
            raise BadRequestHTTPError("Пустой JSON")

        if (audit := AuditRunRequest.create(data)) is None:
            raise BadRequestHTTPError("некорректны обязательные поля")

        await self.kafka.send(topic=self.config.audit_requests, value=audit.to_dict())

        return JSONResponse(audit.to_dict(), status_code=HTTP_200_OK)


class AuditTargetsResource(BaseResource):
    def __init__(self):
        self.control = TargetsControl()

    async def get(self) -> JSONResponse:
        if (targets := await self.control.fetch_targets()) is None:
            raise BadRequestHTTPError("не удалось получить список целей")

        return JSONResponse(targets.to_dict(), status_code=HTTP_200_OK)
