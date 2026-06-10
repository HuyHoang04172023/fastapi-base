import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from middlewares import add_base_middlewares
from routes.api_v1 import api_v1
from utils.configs import project_settings
from utils.handler_exceptions import exception_handlers

app = FastAPI(
    title="FastAPI Base API",
    version="1.0",
    docs_url="/docs" if project_settings.ALLOW_DOC else None,
    redoc_url="/redoc" if project_settings.ALLOW_DOC else None,
    swagger_ui_parameters={
        "displayRequestDuration": True,
        "displayOperationId": True,
        "operationsSorter": "alpha",
        "tagsSorter": "alpha",
        "filter": True,
    }
)


def remove_422_validation_errors():
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            terms_of_service=app.terms_of_service,
            contact=app.contact,
            license_info=app.license_info,
            routes=app.routes,
            tags=app.openapi_tags,
            servers=app.servers,
        )
        for _, method_item in app.openapi_schema.get('paths').items():
            for _, param in method_item.items():
                responses = param.get('responses')
                # remove 422 response, also can remove other status code
                if '422' in responses:
                    del responses['422']
    return app.openapi_schema


app.openapi = remove_422_validation_errors

app.include_router(api_v1)

add_base_middlewares(app)
exception_handlers(app)

# Use for debugging setting in pycharm, reload = True for auto build when file change
if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
