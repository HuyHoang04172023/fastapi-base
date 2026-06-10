from typing import Optional

from pydantic import BaseModel, model_validator

from utils.string_helpers import StringHelper


class SearchInput(BaseModel):
    page: Optional[int] = 1
    keyword: Optional[str] = None
    per_page: Optional[int] = 10
    user_id: Optional[int] = None
    offset: Optional[int] = 0

    @model_validator(mode='after')
    def hash_password(self):
        self.offset = (self.page - 1) * self.per_page
        self.keyword = StringHelper.escape_special_character_in_like_filter(self.keyword) if self.keyword else None
        return self
