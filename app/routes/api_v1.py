from fastapi import APIRouter

from controllers import *

api_v1 = APIRouter(prefix='/api/v1')

api_v1.include_router(public_router, prefix='', tags=['public'])
api_v1.include_router(auth_router, prefix='/auth', tags=['auth'])
api_v1.include_router(admin_router, prefix='/admin', tags=['admin'])
