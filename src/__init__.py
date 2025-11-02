from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.auth.routes import auth_router
from src.books.routes import book_router
from src.reviews.routes import review_router
from src.db.main import init_db


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

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["reviews"])
