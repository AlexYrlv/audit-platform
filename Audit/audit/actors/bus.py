from config_fastapi import Config
from fpiaioact import Actor
from ..baseclasses import BasePC
from ..controls import AuditControl
from ..kafka import KafkaPC
from ..structures import AuditMessage, AuditResult


class KafkaActor(Actor, BasePC):
    config = Config(section="kafka.topics")

    def __init__(self):
        super().__init__(name="KafkaActor")
        self.kafka = KafkaPC()
        self.control = AuditControl()

    async def __call__(self, system):
        self.kafka.subscribe(self.on_message)

        try:
            await self.kafka.listen()
        finally:
            await self.kafka.close()


    async def on_message(self, msg: dict) -> None:
        self.logger.info(f" Получено сообщение audit_requests: {msg}")

        if (audit := AuditMessage.create(msg)) is None:
            self.logger.warning(" Некорректное сообщение, пропущено")
            return

        ref, act = await self.control.fetch_pair(audit)

        self.logger.info(f" Эталон {audit.target_type} → {ref}")
        self.logger.info(f" Фактическое состояние {audit.target_type} → {act}")

        result = AuditResult.create(audit, ref, act)
        self.logger.info(f" Результат: success={result.success}, differences={result.differences}")

        await self.kafka.send(self.config.audit_results, result.to_dict())
