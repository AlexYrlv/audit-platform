#!/usr/bin/env python
import asyncio
import logging
from commandlinestart import Cli, echo
import netbox as service

logger = logging.getLogger("manage")


def run_workers(*actor_names: str):
    echo("▶️  Start NetBox gRPC workers")
    service.application_config()
    actor_app = service.create_app()

    async def wrapper():
        await actor_app.run_actors(*actor_names)

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        asyncio.run(wrapper())
    else:
        return loop.create_task(wrapper())


def create_cli():
    cli = Cli(service=service)
    cli.add_command("workers", run_workers, nargs=-1)
    cli.add_command("worker", run_workers)
    return cli


if __name__ == "__main__":
    create_cli().start()