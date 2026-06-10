from typing import Generic, TypeVar

from pydantic import BaseModel

from constants.messages import AllMessages

M = TypeVar("M", bound=BaseModel)


class ResponseStatus(BaseModel):
    code: int = 200
    message: str = AllMessages.HTTP_MESSAGES[200]


class BaseGenericResponse(BaseModel):
    status: ResponseStatus


class GenericResponse(BaseGenericResponse, Generic[M]):
    data: M
