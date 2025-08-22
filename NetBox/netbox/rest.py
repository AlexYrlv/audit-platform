# netbox/rest.py
from typing import Any

from config_fastapi import Config
from frpclnt import AsyncRestClient
from .structures import Device, Subnet, IPAddress
from .constants import API_ENDPOINT


class NetBoxRest:
    config = Config(section="netbox")

    @property
    def rest(self) -> AsyncRestClient:
        return AsyncRestClient(
            address=self.config.url,
            headers=self.config.headers.to_dict(),
            timeout=self.config.timeout,
        )

    async def get_devices(self) -> list[Device]:
        resp = await self.rest("get", API_ENDPOINT.netbox_devices.value)
        return [Device.create(item) for item in resp.get("results", [])]

    async def get_subnets(self) -> list[Subnet]:
        resp = await self.rest("get", API_ENDPOINT.netbox_prefixes.value)
        return [Subnet.create(item) for item in resp.get("results", [])]

    async def get_ips(self) -> list[IPAddress]:
        resp = await self.rest("get", API_ENDPOINT.netbox_ip_addresses.value)
        return [IPAddress.create(item) for item in resp.get("results", [])]


    async def get_targets(self) -> list[dict[str, Any]]:
        devices = await self.get_devices()
        subnets = await self.get_subnets()
        ips = await self.get_ips()
        return [d.to_dict() for d in devices + subnets + ips]