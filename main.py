from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import test_connection
from app.middlewares.error_handler import global_exception_handler

from app.core.config import settings
from app.core.database import engine, Base
from app.api.task import router as task_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    test_connection()
    Base.metadata.create_all(bind=engine)
    yield
    
app = FastAPI(
    title="Task Management API",
    version="1.0.0",
    lifespan=lifespan
    )

app.add_exception_handler(Exception, global_exception_handler)
app.include_router(task_router)

@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "OK",
            "message": "The API is running."
            }
    
@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}!"}