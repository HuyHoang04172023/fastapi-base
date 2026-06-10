class StringHelper:
    @classmethod
    def check_string_empty(cls, data: str):
        if len(data.strip()) == 0:
            return True
        return False

    @classmethod
    def escape_special_character_in_like_filter(cls, value: str):
        if value:
            value = value.replace('\\', "\\\\")
            value = value.replace('_', '\\_')
            value = value.replace('%', '\\%')
        return value
