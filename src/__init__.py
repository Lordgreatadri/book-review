from fastapi import FastAPI, status

from src.books.routes import router as book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from src.tags.routes import tags_router
from contextlib import asynccontextmanager 
from src.db.main import init_db
from src.middleware import register_middleware
from .exceptions.errors import (
    register_all_errors
)
from src.config import Config

from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

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
api_prefix =f"/api/{version}"
description = """
A REST API for book review web service.

This REST API enable you to:
- Create a user account, Receive account verification email, Resend verification email, Request reset password link via email, Reset password.
- Create, Read, Update, And Delete Books
- Add Reviews To Books
- Add Tags To Books e.t.c.
    """

app = FastAPI(
    title="Book Review",
    description=description,
    version = version,
    license_info={"name": "MIT License", "url": "https://opensource.org/license/mit"},
    contact={
        "name": "Emmanuel Lordgreat-Adri",
        "url": "https://github.com/Lordgreatadri",
        "email":"lodgreatadri@gmail.com",
    },
    openapi_url=f"{api_prefix}/openapi.json",
    docs_url=f"{api_prefix}/docs",
    redoc_url=f"{api_prefix}/redoc",
    # terms_of_service="overhere",
    # lifespan=life_span,
)


# Initialize Limiter with a global rate limit
limiter = Limiter(key_func=get_remote_address, default_limits=[Config.rate_limts])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, lambda request, exc: JSONResponse(
    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
    content={
        "status_code": status.HTTP_429_TOO_MANY_REQUESTS,
        "message": "Too many requests",
        "detail": "Rate limit exceeded. Please try again later."
        }
))

# Add SlowAPI Middleware to apply the limiter
app.add_middleware(SlowAPIMiddleware)


register_all_errors(app)

register_middleware(app)

app.include_router(auth_router, prefix=f"{api_prefix}/auth", tags=["Authentication"])
app.include_router(book_router, prefix=f"{api_prefix}/books", tags=["Books"])
app.include_router(review_router, prefix=f"{api_prefix}/reviews", tags=["Reviews"])
app.include_router(tags_router, prefix=f"{api_prefix}/tags", tags=["Tags"])

