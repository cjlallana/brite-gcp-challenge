import os

from fastapi import FastAPI

from api.v1.internal import movies as movies_internal
from api.v1.public import movies as movies_public

app = FastAPI(
    title="Public API",
    version="1.0.1",
    debug=(os.getenv("LOGGING_LEVEL", "INFO") == "DEBUG"),
)

app.include_router(router=movies_public.router)
app.include_router(router=movies_internal.router)


@app.get("/v1/healthy", include_in_schema=False)
@app.get("/v1/status", include_in_schema=False)
@app.get("/healthy", include_in_schema=False)
@app.get("/status", include_in_schema=False)
async def read_status():
    body = {
        "status": "UP",
    }
    return body
