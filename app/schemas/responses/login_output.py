from schemas.base_schema import BaseSchema


class LoginOutput(BaseSchema):
    id: int
    email: str
    access_token: str
    refresh_token: str
