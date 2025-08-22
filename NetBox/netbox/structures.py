from __future__ import annotations
from dataclasses import dataclass, replace
from typing import Any


@dataclass(frozen=True)
class Device:
    name: str | None = None
    platform: str | None = None
    model: str | None = None
    ip: str | None = None

    @classmethod
    def create(cls, data: dict[str, Any]) -> Device:
        result = cls()
        if data.get("name") is not None:
            result = replace(result, name=data["name"])
        if data.get("platform") and data["platform"].get("name") is not None:
            result = replace(result, platform=data["platform"]["name"])
        if data.get("device_type") and data["device_type"].get("model") is not None:
            result = replace(result, model=data["device_type"]["model"])
        if data.get("primary_ip4") and data["primary_ip4"].get("address") is not None:
            result = replace(result, ip=data["primary_ip4"]["address"])
        return result

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "platform": self.platform,
            "model": self.model,
            "ip": self.ip,
        }


@dataclass(frozen=True)
class Subnet:
    prefix: str | None = None
    description: str | None = None
    vlan: str | None = None

    @classmethod
    def create(cls, data: dict[str, Any]) -> Subnet:
        result = cls()
        if data.get("prefix") is not None:
            result = replace(result, prefix=data["prefix"])
        if data.get("description") is not None:
            result = replace(result, description=data["description"])
        if isinstance(data.get("vlan"), dict) and data["vlan"].get("name"):
            result = replace(result, vlan=data["vlan"]["name"])
        return result

    def to_dict(self) -> dict[str, Any]:
        return {
            "prefix": self.prefix,
            "description": self.description,
            "vlan": self.vlan,
        }

@dataclass(frozen=True)
class IPAddress:
    address: str | None = None
    dns_name: str | None = None
    device_name: str | None = None
    interface_name: str | None = None

    @classmethod
    def create(cls, data: dict[str, Any]) -> IPAddress:
        result = cls()
        if data.get("address"):
            result = replace(result, address=data["address"])
        if data.get("dns_name"):
            result = replace(result, dns_name=data["dns_name"])
        if assigned := data.get("assigned_object"):
            if device := assigned.get("device"):
                result = replace(result, device_name=device.get("name"))
            if assigned.get("name"):
                result = replace(result, interface_name=assigned["name"])
        return result

    def to_dict(self) -> dict[str, Any]:
        return {
            "address": self.address,
            "dns_name": self.dns_name,
            "device_name": self.device_name,
            "interface_name": self.interface_name,
        }

@dataclass(frozen=True)
class Target:
    target: str | None = None
    target_type: str | None = None

    @classmethod
    def create(cls, data: dict[str, Any]) -> Target:
        result = cls()
        if data.get("name") is not None:
            result = replace(result, target=data["name"], target_type="device")
        if data.get("prefix") is not None:
            result = replace(result, target=data["prefix"], target_type="subnet")
        if data.get("address") is not None:
            result = replace(result, target=data["address"], target_type="ip")
        return result

    def to_dict(self) -> dict[str, Any]:
        return {"target": self.target, "target_type": self.target_type}
