from typing import AsyncGenerator

from starlette.requests import Request


async def get_llm_with_tool(
    request: Request,
):
    return request.app.state.llm_with_tool


async def get_search_graph(
    request: Request,
):
    return request.app.state.search_graph
