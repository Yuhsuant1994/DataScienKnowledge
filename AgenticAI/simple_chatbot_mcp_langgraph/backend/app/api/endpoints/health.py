from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/health")
async def health_check(request: Request):
    """Health check endpoint to verify all services are initialized."""
    app = request.app
    health_status = {
        "status": "healthy",
        "components": {
            "arxiv": hasattr(app.state, "arxiv") and app.state.arxiv is not None,
            "wikipedia": hasattr(app.state, "wiki") and app.state.wiki is not None,
            "tavily": hasattr(app.state, "tavily") and app.state.tavily is not None,
            "llm_with_tool": hasattr(app.state, "llm_with_tool")
            and app.state.llm_with_tool is not None,
            "search_graph": hasattr(app.state, "search_graph")
            and app.state.search_graph is not None,
            "mcp_client": hasattr(app.state, "mcp_client")
            and app.state.mcp_client is not None,
        },
    }
    all_healthy = all(health_status["components"].values())
    health_status["status"] = "healthy" if all_healthy else "unhealthy"

    return health_status
