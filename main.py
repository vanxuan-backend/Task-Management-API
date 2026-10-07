from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import test_connection
from app.middlewares.error_handler import global_exception_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    test_connection()
    yield
    
app = FastAPI(
    title="Task Management API",
    version="1.0.0",
    lifespan=lifespan
    )

app.add_exception_handler(Exception, global_exception_handler)

@app.get("/health", tags=["Health Check"])
def health_check():
    return {"status": "OK",
            "message": "The API is running."
            }