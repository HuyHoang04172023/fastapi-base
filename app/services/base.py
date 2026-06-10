from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from constants.messages import AllMessages


class BaseService:

    @classmethod
    def custom_response(cls, data=None, status_code=200, message=None, errors=None, internal_code=None) -> JSONResponse:
        if internal_code is None:
            internal_code = status_code
        response = {
            'status': {
                'code': internal_code,
                'message': message if message is not None else AllMessages.HTTP_MESSAGES[internal_code]
            },
            'data': data
        }

        if data is not None:
            response['data'] = data
        if errors is not None:
            response['errors'] = errors

        return JSONResponse(status_code=status_code, content=jsonable_encoder(response))
