from logging import Logger, getLogger


class LoggerMixin:
    logger: Logger = getLogger()

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        obj.logger = cls.logger.getChild(cls.__name__)
        return obj


class BaseControl(LoggerMixin):
    pass

class BasePC(LoggerMixin):
    pass
