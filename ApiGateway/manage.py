#!/usr/bin/env python
import logging
import asyncio
import uvicorn

from commandlinestart import Cli, echo
import apigateway as service

logger = logging.getLogger("manage")


def run_server():
    """
    Запуск FastAPI сервера.
    """
    echo("Запуск FastAPI сервера...")
    uvicorn.run(service.start_app(), host="0.0.0.0", port=8000)


def run_workers(*names: str):
    """
    Запуск нескольких акторов по именам.
    """
    echo("✅ Вызов application_config()")
    echo(f"Запуск акторов: {', '.join(names)}")

    service.application_config()
    actor_app = service.create_actors()

    async def wrapped() -> None:
        loop = asyncio.get_running_loop()
        loop.set_exception_handler(global_asyncio_handler)

        await actor_app.run_actors(*names)

    try:
        asyncio.run(wrapped())
    except KeyboardInterrupt:
        echo("Остановка по Ctrl+C")
    except asyncio.CancelledError:
        echo("❌ Получен asyncio.CancelledError — возможно shutdown")
        raise
    except Exception as e:
        echo(f"❌ Неожиданная ошибка: {e}")
        raise
    except BaseException as be:
        echo(f"‼️ Системное исключение (BaseException): {be}")
        raise
    finally:
        logger.critical("‼️ Все акторы завершили работу — это НЕ штатная ситуация")

def global_asyncio_handler(loop: asyncio.AbstractEventLoop, context: dict) -> None:
    """
    Глобальный обработчик ошибок asyncio.
    """
    msg = context.get("exception", context.get("message"))
    logger.critical(f"‼️ Глобальное исключение asyncio: {msg}")



def create_cli():
    cli = Cli(service=service)
    cli.add_command("server", run_server)
    cli.add_command("workers", run_workers, nargs=-1)
    cli.add_command("worker", run_workers)
    return cli



if __name__ == "__main__":
    create_cli().start()
