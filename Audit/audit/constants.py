from __future__ import annotations
from enum import StrEnum


class TargetType(StrEnum):
    DEVICE = "device"
    SUBNET = "subnet"
    IP = "ip"
