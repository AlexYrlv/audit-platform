from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from .constants import TYPES


@dataclass(frozen=True)
class AuditRunRequest:
    task_id: str = field(default_factory=lambda: f"audit-{uuid4()}")
    target: str = ""
    target_type: str = ""
    status: str = "scheduled"

    @classmethod
    def create(cls, data: dict) -> AuditRunRequest | None:
        if (target := data.get("target")) is None:
            return None
        if (target_type := data.get("target_type")) is None:
            return None
        if target_type not in TYPES:
            return None

        return cls(
            target=target,
            target_type=target_type,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "target": self.target,
            "target_type": self.target_type,
            "status": self.status,
        }


@dataclass(frozen=True)
class AuditTargetsRequest:
    target_ids: list[str] = field(default_factory=list)

    @classmethod
    def create(cls, data: dict) -> AuditTargetsRequest | None:
        if (target_ids := data.get("target_ids")) is None:
            return None
        if not isinstance(target_ids, list):
            return None

        return cls(target_ids=target_ids)

    def to_dict(self) -> dict[str, Any]:
        return {"target_ids": self.target_ids}
