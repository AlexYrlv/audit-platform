from logging import Logger, getLogger
from fastabc import Api


class LoggerMixin:
    logger: Logger = getLogger()

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        obj.logger = cls.logger.getChild(cls.__name__)
        return obj

class BaseResource(LoggerMixin):
    pass


class BaseControl(LoggerMixin):
    pass


class BaseAPI(Api, LoggerMixin):
    pass

class BasePC(LoggerMixin):
    pass

