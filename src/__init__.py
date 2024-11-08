from fastapi import FastAPI, status

from src.books.routes import router as book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from src.tags.routes import tags_router
from contextlib import asynccontextmanager 
from src.db.main import init_db
from .exceptions.errors import (
    register_all_errors
)


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
    # lifespan=life_span
)


register_all_errors(app)



app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Authentication"])
app.include_router(book_router, prefix=f"/api/{version}/books", tags=["Books"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["Reviews"])
app.include_router(tags_router, prefix=f"/api/{version}/tags", tags=["Tags"])

