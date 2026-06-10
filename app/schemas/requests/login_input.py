from pydantic import BaseModel, EmailStr, Field, model_validator

from utils.security import hash_password


class LoginInput(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

    @model_validator(mode='after')
    def hash_input_password(self):
        self.password = hash_password(self.password)
        return self
