from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


class BadRequestHTTPError(HTTPException):
    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=HTTP_400_BAD_REQUEST, detail=detail)