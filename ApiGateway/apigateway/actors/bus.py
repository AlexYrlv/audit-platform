from fpiaioact import Actor
from ..baseclasses import BasePC
from ..kafka import KafkaPC


class KafkaActor(Actor, BasePC):
    """
    Актор для получения сообщений из Kafka и передачи их в bus.
    Работает только если consumer был инициализирован.
    """
    def __init__(self):
        super().__init__(name="KafkaActor")
        self.kafka = KafkaPC()

    async def __call__(self, system):
        self.kafka.subscribe(self.on_message)

        try:
            await self.kafka.listen()
        finally:
            await self.kafka.close()

    async def on_message(self, msg: dict):
        self.logger.info(f" Получено сообщение audit_results: {msg}")
