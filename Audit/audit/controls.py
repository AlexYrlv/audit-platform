from __future__ import annotations
from .structures import AuditMessage, DeviceReference, SubnetReference, IPReference, MOCK_DEVICE_MAP, MOCK_SUBNET_MAP, MOCK_IP_MAP
from .constants import TargetType
from .grpc import NetBoxGrpc


class AuditControl:
    def __init__(self) -> None:
        self.grpc = NetBoxGrpc()

    async def fetch_pair(self, msg: AuditMessage) -> tuple[
        DeviceReference | SubnetReference | IPReference | None, DeviceReference | SubnetReference | IPReference | None]:

        match msg.target_type:
            case TargetType.DEVICE if (ref := await self.grpc.get_device(msg.target)):
                act = await self.get_actual_device(msg.target)
            case TargetType.SUBNET if (ref := await self.grpc.get_subnet(msg.target)):
                act = await self.get_actual_subnet(msg.target)
            case TargetType.IP if (ref := await self.grpc.get_ip(msg.target)):
                act = await self.get_actual_ip(msg.target)
            case _:
                return (None, None)

        return ref, act

    async def get_actual_device(self, name: str) -> DeviceReference | None:
        # TODO: Реализация через SSH/SNMP/gNMI
        if (data := MOCK_DEVICE_MAP.get(name)) is None:
            return None
        return DeviceReference.create(data.__dict__)

    async def get_actual_subnet(self, prefix: str) -> SubnetReference | None:
        # TODO: Реализация через gNMI или другие IP-сканеры
        if (data := MOCK_SUBNET_MAP.get(prefix)) is None:
            return None
        return SubnetReference.create(data.__dict__)

    async def get_actual_ip(self, address: str) -> IPReference | None:
        # TODO: Реализация ping/resolve или ARP-таблица
        if (data := MOCK_IP_MAP.get(address)) is None:
            return None
        return IPReference.create(data.__dict__)
