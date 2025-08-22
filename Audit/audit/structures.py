from __future__ import annotations
from dataclasses import dataclass, replace, field, is_dataclass, fields
from typing import Any
from .constants import TargetType


@dataclass(frozen=True)
class AuditMessage:
    task_id: str
    target: str
    target_type: TargetType
    status: str

    @classmethod
    def create(cls, data: dict[str, Any]) -> AuditMessage:
        return cls(
            task_id=data["task_id"],
            target=data["target"],
            target_type=TargetType(data["target_type"]),
            status=data["status"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "target": self.target,
            "target_type": self.target_type,
            "status": self.status,
        }


@dataclass(frozen=True)
class DeviceReference:
    name: str | None = None
    platform: str | None = None
    model: str | None = None
    ip: str | None = None

    @classmethod
    def create(cls, data: dict[str, Any]) -> DeviceReference:
        result = cls()
        if data.get("name") is not None:
            result = replace(result, name=data["name"])
        if data.get("platform") is not None:
            result = replace(result, platform=data["platform"])
        if data.get("model") is not None:
            result = replace(result, model=data["model"])
        if data.get("ip") is not None:
            result = replace(result, ip=data["ip"])
        return result

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "platform": self.platform,
            "model": self.model,
            "ip": self.ip,
        }


@dataclass(frozen=True)
class IPReference:
    address: str | None = None
    dns_name: str | None = None
    device_name: str | None = None
    interface_name: str | None = None

    @classmethod
    def create(cls, data: dict[str, Any]) -> IPReference:
        result = cls()
        if data.get("address"):
            result = replace(result, address=data["address"])
        if data.get("dns_name"):
            result = replace(result, dns_name=data["dns_name"])
        if data.get("device_name"):
            result = replace(result, device_name=data["device_name"])
        if data.get("interface_name"):
            result = replace(result, interface_name=data["interface_name"])
        return result

    def to_dict(self) -> dict[str, Any]:
        return {
            "address": self.address,
            "dns_name": self.dns_name,
            "device_name": self.device_name,
            "interface_name": self.interface_name,
        }


@dataclass(frozen=True)
class SubnetReference:
    prefix: str | None = None
    description: str | None = None
    vlan: str | None = None

    @classmethod
    def create(cls, data: dict[str, Any]) -> SubnetReference:
        result = cls()
        if data.get("prefix") is not None:
            result = replace(result, prefix=data["prefix"])
        if data.get("description") is not None:
            result = replace(result, description=data["description"])
        if data.get("vlan") is not None:
            result = replace(result, vlan=data["vlan"])
        return result

    def to_dict(self) -> dict[str, Any]:
        return {
            "prefix": self.prefix,
            "description": self.description,
            "vlan": self.vlan,
        }

@dataclass(frozen=True)
class AuditResult:
    task_id: str
    target: str
    target_type: str
    success: bool
    differences: dict[str, tuple[Any, Any]] = field(default_factory=dict)

    @classmethod
    def create(cls, audit: AuditMessage, ref, act) -> AuditResult:
        diffs, success = cls.diff(ref, act)
        return cls(
            task_id=audit.task_id,
            target=audit.target,
            target_type=audit.target_type.value,
            success=success,
            differences=diffs,
        )

    @classmethod
    def diff(cls, ref: Any, act: Any) -> tuple[dict[str, tuple[Any, Any]], bool]:
        """Универсальное сравнение двух датаклассов (или None)."""
        names_present = bool(cls._field_names(ref) or cls._field_names(act))
        diffs = cls._calc_diffs(ref, act)
        success = (names_present and not diffs)
        return diffs, success

    @staticmethod
    def _field_names(obj: Any) -> list[str]:
        if obj is None or not is_dataclass(obj):
            return []
        return [f.name for f in fields(obj)]

    @staticmethod
    def _safe_get(obj: Any, name: str) -> Any:
        if obj is None:
            return None
        return getattr(obj, name, None)

    @classmethod
    def _calc_diffs(cls, ref: Any, act: Any) -> dict[str, tuple[Any, Any]]:
        names = set(cls._field_names(ref)) | set(cls._field_names(act))
        return {
            name: (cls._safe_get(ref, name), cls._safe_get(act, name))
            for name in names
            if cls._safe_get(ref, name) != cls._safe_get(act, name)
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "target": self.target,
            "target_type": self.target_type,
            "success": self.success,
            "differences": self.differences,
        }


@dataclass(frozen=True)
class MockIPData:
    address: str
    dns_name: str
    device_name: str
    interface_name: str


FULL_MATCH_IP = MockIPData(
    address="10.0.0.10/24",
    dns_name="host1",
    device_name="sw-core-1",
    interface_name="eth0",
)
MISMATCH_IP = MockIPData(
    address="10.0.0.20/24",
    dns_name="bad-host",
    device_name="sw-core-1",
    interface_name="eth99",
)

MOCK_IP_MAP = {
    FULL_MATCH_IP.address: FULL_MATCH_IP,
    MISMATCH_IP.address: MISMATCH_IP,
}


@dataclass(frozen=True)
class MockDeviceData:
    name: str
    platform: str
    model: str
    ip: str


FULL_MATCH_DEVICE = MockDeviceData(
    name="sw-core-1",
    platform="Cisco IOS",
    model="C9300-24T",
    ip="10.0.0.10/24",
)
MISMATCH_DEVICE = MockDeviceData(
    name="sw-core-2",
    platform="Unknown OS",
    model="C9300-24T",
    ip="10.0.0.20/24",
)

MOCK_DEVICE_MAP = {
    FULL_MATCH_DEVICE.name: FULL_MATCH_DEVICE,
    MISMATCH_DEVICE.name: MISMATCH_DEVICE,
}


@dataclass(frozen=True)
class MockSubnetData:
    prefix: str
    description: str
    vlan: str


FULL_MATCH_SUBNET = MockSubnetData(
    prefix="10.0.0.0/24",
    description="Main subnet",
    vlan="mgmt",
)
MISMATCH_SUBNET = MockSubnetData(
    prefix="10.0.1.0/24",
    description="Wrong subnet",
    vlan="guest",
)

MOCK_SUBNET_MAP = {
    FULL_MATCH_SUBNET.prefix: FULL_MATCH_SUBNET,
    MISMATCH_SUBNET.prefix: MISMATCH_SUBNET,
}
