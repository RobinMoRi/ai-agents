import logging
from contextlib import asynccontextmanager

from braintrust.wrappers.agno import setup_agno
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from odevo_ai.utils import (
    setup_uvicorn_logging,
)

from deps import get_settings
from routes.agents import router as agents_router

logger = logging.getLogger(__name__)
settings = get_settings()

setup_agno(project_name="ai-agno-agent", api_key=settings.braintrust_api_key)


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Agno Agent", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = create_app()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "healthy"}


app.include_router(agents_router)


if __name__ == "__main__":
    import uvicorn

    log_config = setup_uvicorn_logging()

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_config=log_config,
    )
