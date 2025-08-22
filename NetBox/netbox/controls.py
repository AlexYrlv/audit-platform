from __future__ import annotations
from proto import netbox_pb2, netbox_pb2_grpc
from .rest import NetBoxRest
from .structures import Target


class NetBoxController(netbox_pb2_grpc.NetBoxServicer):
    def __init__(self) -> None:
        self.rest = NetBoxRest()

    async def GetTargets(self, request, context):
        raw = await self.rest.get_targets()
        return netbox_pb2.GetTargetsResponse(
            targets=[netbox_pb2.Target(**Target.create(item).to_dict()) for item in raw]
        )

    async def GetDevices(self, request, context):
        devices = await self.rest.get_devices()
        matched = [d.to_dict() for d in devices if d.name == request.name]
        return netbox_pb2.GetDevicesResponse(
            devices=[netbox_pb2.Device(**d) for d in matched]
        )

    async def GetSubnets(self, request, context):
        subnets = await self.rest.get_subnets()
        matched = [s.to_dict() for s in subnets if s.prefix == request.prefix]
        return netbox_pb2.GetSubnetsResponse(
            subnets=[netbox_pb2.Subnet(**s) for s in matched]
        )

    async def GetIPs(self, request, context):
        ips = await self.rest.get_ips()
        matched = [ip.to_dict() for ip in ips if ip.address == request.address]
        return netbox_pb2.GetIPsResponse(
            ips=[netbox_pb2.IPAddress(**ip) for ip in matched]
        )
