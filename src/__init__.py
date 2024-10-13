from fastapi import FastAPI

from src.books.routes import router
from src.auth.routes import auth_router
from contextlib import asynccontextmanager 
from src.db.main import init_db

#to determine which code to run at the start of our application.
@asynccontextmanager
async def life_span(app: FastAPI):
    print("Starting server...")

    await init_db()  # Initialize database connection.

    try:
        yield
    finally:
        print("Closing server...")   

version = "v1"
app = FastAPI(
    title="Book Review",
    description="A REST API for book review web service",
    version = version,
    lifespan=life_span
)

app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["authentication"])
app.include_router(router, prefix=f"/api/{version}/books", tags=["books"])