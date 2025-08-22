from .grpc import NetBoxGrpc
from .structures import AuditTargetsRequest

class TargetsControl:
    def __init__(self):
        self.grpc = NetBoxGrpc()

    async def fetch_targets(self) -> AuditTargetsRequest:
        return await self.grpc.get_targets()