from fastapi import FastAPI, status
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse

from src.auth.routes import auth_router
from src.tags.routes import tags_router
from src.books.routes import book_router
from src.reviews.routes import review_router

from .errors import register_error_handlers
from .middleware import register_middleware

# from src.db.main import init_db


@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"🔌 server is starting ...")  # Runs on app startup
    # await init_db()
    yield  # <-- This is where FastAPI runs your app (FastAPI app is live (serving requests))
    print(f"🧹 server has been stopped ...")  # Runs on app shutdown


version = "v1"

app = FastAPI(
    title="Learn Fastapi(Book library)",
    version=version,
    description="A REST API for a book library web service",
    lifespan=life_span,
)

# In FastAPI, app.add_exception_handler() lets you register a custom handler for specific exceptions.

# That means:

# Whenever that specific exception is raised anywhere in your app, FastAPI will catch it and use your custom handler function to generate the HTTP response instead of crashing or returning the default error.
register_error_handlers(app)
register_middleware(app)

app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["reviews"])
app.include_router(tags_router, prefix=f"/api/{version}/tags", tags=["tags"])
