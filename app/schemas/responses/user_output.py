from schemas.base_schema import BaseSchema


class UserOutput(BaseSchema):
    id: int
    email: str
    user_name: str
    is_active: bool


class ListUserOutput(BaseSchema):
    list: list[UserOutput]
    total: int = 0
