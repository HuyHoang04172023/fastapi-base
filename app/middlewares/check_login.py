from datetime import datetime

from fastapi import Depends, Request
from fastapi.security import HTTPBearer
from jose import jwt

from utils.configs import project_settings
from utils.custom_exception import CustomException

for_docs_form = HTTPBearer(scheme_name='Authorization')


class CheckLogin:

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __call__(self, request: Request, token=Depends(for_docs_form)):
        if token:
            try:
                payload = jwt.decode(token.credentials, project_settings.SECRET_KEY,
                                     algorithms=[project_settings.ALGORITHM])
                if datetime.fromtimestamp(payload.get('exp')) < datetime.now():
                    raise CustomException(403, 'Token expired')
                self.__dict__.update({
                    'user_id': payload.get('id'),
                    'user_email': payload.get('email'),
                    'is_admin': payload.get('admin'),
                    'is_active': payload.get('active')
                })
            except Exception as ex:
                raise CustomException(403, str(ex))
        else:
            raise CustomException(401, 'Unauthorized! Please login.')
        return self.__dict__
