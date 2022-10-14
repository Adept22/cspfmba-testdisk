import uvicorn
from fastapi import FastAPI, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.settings import settings
from app.db import db
from app.routers import imports_router, delete_router, nodes_router, updates_router
from app.exceptions import ValidationException


app = FastAPI(title="Test Disk API", debug=settings.debug)


@app.exception_handler(status.HTTP_404_NOT_FOUND)
async def not_found_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"code": status.HTTP_404_NOT_FOUND, "message": "Item not found"},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"code": status.HTTP_400_BAD_REQUEST, "message": "Validation Failed"},
    )


@app.exception_handler(ValidationException)
async def bad_request_exception_handler(request: Request, exc):
    return await validation_exception_handler(request, exc)


app.include_router(router=imports_router)
app.include_router(router=delete_router)
app.include_router(router=nodes_router)
app.include_router(router=updates_router)


@app.on_event("startup")
def startup():
    db.init_app(app)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        debug=settings.debug,
    )
