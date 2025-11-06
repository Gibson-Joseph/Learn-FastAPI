from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import Response


import time
import logging

logger = logging.getLogger("uvicorn.access")
logger.disabled = True

# So normally, for every incoming request, you’ll see lines like this in the console:
# INFO:     127.0.0.1:49218 - "GET /users HTTP/1.1" 200 OK

# That’s the access log — it’s managed by the "uvicorn.access" logger.


def register_middleware(app: FastAPI):
    @app.middleware("http")
    async def custom_loggin(request: Request, call_next):
        start_time = time.time()

        response: Response = await call_next(request)

        processing_time = time.time() - start_time

        message = f"{request.client.host}:{request.client.port} - {request.method} - {request.url.path} - {response.status_code} completed after {processing_time}s"

        print(message)
        return response
