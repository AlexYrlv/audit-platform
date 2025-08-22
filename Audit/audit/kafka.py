import kafkabus
from config_fastapi import Config

from .baseclasses import BasePC


class KafkaPC(BasePC):
    config = Config(section='kafka.connection')

    def __init__(self):
        self.connection = kafkabus.get(self.config.alias)

    async def send(self, topic: str, value: dict) -> None:
        if not self.connection.producer:
            raise RuntimeError("Kafka producer не инициализирован")
        await self.connection.producer.send(topic, value)

    def subscribe(self, handler) -> None:
        if not self.connection.consumer:
            raise RuntimeError("Kafka consumer не инициализирован")
        self.connection.consumer.subscribe(handler)

    async def listen(self) -> None:
        if self.connection.producer:
            await self.connection.producer.start()
        if self.connection.consumer:
            await self.connection.consumer.start()

    async def close(self) -> None:
        if self.connection.consumer:
            await self.connection.consumer.stop()
        if self.connection.producer:
            await self.connection.producer.stop()

    @property
    def bus(self):
        return self.connection.bus
