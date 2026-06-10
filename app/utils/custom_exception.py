import inspect

from utils.custom_log import clog


class CustomException(Exception):
    status_code: int
    message: str = ""
    payload: dict | str | None = None

    def __init__(self, status_code=500, message='Unknown error', payload=None):
        Exception.__init__(self)
        caller_frame_record = inspect.stack()[1]  # 0 represents this line
        frame = caller_frame_record[0]
        info = inspect.getframeinfo(frame)
        if status_code == 500:
            clog.opt(colors=True).critical(f'<r>Errors:</r> {info.filename} >> {info.function} >> {info.lineno}:'
                                           f' {message} - {payload}')
        else:
            clog.opt(colors=True).error(f'<r>Errors:</r> {info.filename} >> {info.function} >> {info.lineno}:'
                                        f' {message} - {payload}')
        clog.info('======================= END   REQUEST =======================')
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def __str__(self):
        return self.message
