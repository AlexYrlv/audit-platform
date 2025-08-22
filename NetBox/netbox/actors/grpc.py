from __future__ import annotations
import asyncio, traceback, grpc
from fpiaioact import Actor
from config_fastapi import Config

from netbox.controls import NetBoxController
from proto import netbox_pb2_grpc


class NetBoxActor(Actor):
    cfg = Config(section="grpc")

    async def __call__(self, *__) -> None:
        server = grpc.aio.server()
        server.add_insecure_port(f"{self.cfg.host}:{self.cfg.port}")
        netbox_pb2_grpc.add_NetBoxServicer_to_server(NetBoxController(), server)

        await server.start()

        try:
            await server.wait_for_termination()
        except asyncio.CancelledError:
            pass
        except Exception as exc:
            self.logger.error("gRPC runtime error: %s\n%s", exc, traceback.format_exc())
        finally:
            await server.stop(grace=None)
            self.logger.info("⏹️ gRPC stopped")