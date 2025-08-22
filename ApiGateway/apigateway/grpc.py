from __future__ import annotations
from config_fastapi import Config
from grpclnt import AsyncGrpcClient

from proto import netbox_pb2, netbox_pb2_grpc
from .structures import AuditTargetsRequest


class NetBoxGrpc:
    config = Config(section="netbox")

    @property
    def grpc(self) -> AsyncGrpcClient:
        return AsyncGrpcClient(
            address=f"{self.config.host}:{self.config.port}",
            stub_cls=netbox_pb2_grpc.NetBoxStub,
            timeout=self.config.timeout
        )

    async def get_targets(self) -> AuditTargetsRequest:
        response = await self.grpc.stub.GetTargets(netbox_pb2.GetTargetsRequest(), timeout=self.config.timeout)

        return AuditTargetsRequest(target_ids=[t.target for t in response.targets])
