from pydantic import BaseModel, EmailStr, Field, field_validator

from utils.string_helpers import StringHelper


class RegisterInput(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    user_name: str

    @field_validator('user_name')
    @classmethod
    def empty_string(cls, value):
        if StringHelper.check_string_empty(value):
            raise ValueError("User name required.")
        return value
