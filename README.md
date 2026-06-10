## FastAPI Base API
- using Python 3.13 and FastAPI 0.115.13
- all lib use in file requirement.txt
- Using alembic to manager version migrate


- Setup:
- run `docker compose up -d`
- run `docker exec fastapi-app alembic upgrade head` to migrate first table
- open `localhost:8001/docs` for Swagger
- Project build follow MVC with some custom
- Use `sqlalchemy` 2 for ORM and query builder
- Use `pydantic` for form validate request and mapping response (see `schemas` folder)
- Can run with docker or virtual-env to debug 
- Log request will appear in `zlogs` folder