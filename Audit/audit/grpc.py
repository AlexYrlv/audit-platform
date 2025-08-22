from __future__ import annotations
from config_fastapi import Config
from google.protobuf.json_format import MessageToDict
from grpclnt import AsyncGrpcClient

from .structures import DeviceReference, SubnetReference, IPReference
from proto import netbox_pb2, netbox_pb2_grpc


class NetBoxGrpc:
    config = Config(section="netbox")

    @property
    def grpc(self) -> AsyncGrpcClient:
        return AsyncGrpcClient(
            address=f"{self.config.host}:{self.config.port}",
            stub_cls=netbox_pb2_grpc.NetBoxStub,
            timeout=self.config.timeout
        )

    async def get_device(self, name: str) -> DeviceReference | None:
        response = await self.grpc.stub.GetDevices(
            netbox_pb2.GetDevicesRequest(name=name),
            timeout=self.config.timeout,
        )

        if not response.devices:
            return None
        return DeviceReference.create(MessageToDict(response.devices[0]))

    async def get_subnet(self, prefix: str) -> SubnetReference | None:
        response = await self.grpc.stub.GetSubnets(
            netbox_pb2.GetSubnetsRequest(prefix=prefix),
            timeout=self.config.timeout,
        )
        if not response.subnets:
            return None
        return SubnetReference.create(MessageToDict(response.subnets[0]))

    async def get_ip(self, address: str) -> IPReference | None:
        response = await self.grpc.stub.GetIPs(
            netbox_pb2.GetIPsRequest(address=address),
            timeout=self.config.timeout,
        )
        if not response.ips:
            return None
        return IPReference.create(MessageToDict(
            response.ips[0],
            preserving_proto_field_name=True,
            always_print_fields_with_no_presence=True
        ))