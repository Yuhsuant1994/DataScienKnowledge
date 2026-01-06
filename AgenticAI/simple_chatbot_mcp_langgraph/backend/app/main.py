import os

from app.api.api import api_router
from app.log import default_logger as logger
from app.tools.lifetime import (
    init_llm_with_tool,
    init_mcp_client,
    init_search_graph,
    init_tools,
)
from dotenv import load_dotenv

# from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("groq_api")
os.environ["TAVILY_API_KEY"] = os.getenv("tavily_api")


def get_app() -> FastAPI:
    app = FastAPI(title="Demo search engine")
    # Add CORS middleware to allow requests from any origin
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "*",
        ],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    @app.on_event("startup")
    async def _startup():
        """
        Actions to run on application startup.

        This function uses fastAPI app to store data
        in the state, such as db_engine.
        """
        await init_tools(app)
        await init_llm_with_tool(app)
        await init_search_graph(app)
        await init_mcp_client(app)

    # Include your API router
    app.include_router(api_router, prefix="/api")
    return app


app = get_app()


if __name__ == "__main__":
    get_app()
