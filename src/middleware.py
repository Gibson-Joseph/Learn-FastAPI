from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from typing import Callable, Awaitable

import time
import logging

logger = logging.getLogger("uvicorn.access")
logger.disabled = True

# So normally, for every incoming request, you’ll see lines like this in the console:
# INFO:     127.0.0.1:49218 - "GET /users HTTP/1.1" 200 OK

# That’s the access log — it’s managed by the "uvicorn.access" logger.


def register_middleware(app: FastAPI):
    @app.middleware("http")
    async def custom_loggin(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ):
        start_time = time.time()

        response: Response = await call_next(request)

        processing_time = time.time() - start_time

        message = f"{request.client.host}:{request.client.port} - {request.method} - {request.url.path} - {response.status_code} completed after {processing_time}s"

        print(message)
        return response

    # @app.middleware("http")
    # async def authorization(
    #     request: Request, call_next: Callable[[Request], Awaitable[Response]]
    # ):
    #     if not "Authorization" in request.headers:
    #         # When we use middleware we can't raise HttpException inside the middleware.
    #         return JSONResponse(
    #             content={
    #                 "message": "Not Authenticated",
    #                 "resolution": "Please provide the right credentials to proceed",
    #             },
    #             status_code=status.HTTP_401_UNAUTHORIZED,
    #         )
    #     response = await call_next(request)

    #     return response

    # CORS stands for Cross-Origin Resource Sharing.
    # This middleware controls which frontend websites (origins) are allowed to make API requests to your backend.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
    # allow_origins=["*"] → allows any domain (like http://localhost:3000 or https://example.com) to call your API.
    # allow_methods=["*"] → allows all HTTP methods (GET, POST, PUT, DELETE, etc.).
    # allow_credentials=True → allows cookies or Authorization headers to be included in requests.

    # This will guard against HTTP Host Header attack
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1"])
