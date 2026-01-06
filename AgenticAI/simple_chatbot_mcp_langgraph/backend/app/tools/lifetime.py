from pathlib import Path
from typing import Annotated

from app.log import default_logger as logger
from app.tools.mcp import MCPClientPool
from app.tools.tool_factory import create_tools
from fastapi import FastAPI
from langchain_core.messages import AnyMessage
from langchain_groq import ChatGroq
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict


async def init_tools(app: FastAPI) -> None:
    """Initialize all tools using the shared factory."""
    arxiv, wiki, tavily = create_tools()
    app.state.arxiv = arxiv
    app.state.wiki = wiki
    app.state.tavily = tavily
    logger.info("Tools initialized using shared factory (arxiv, wikipedia, tavily)")


async def init_llm_with_tool(app: FastAPI) -> None:
    # Verify dependencies are initialized
    if (
        not hasattr(app.state, "arxiv")
        or not hasattr(app.state, "wiki")
        or not hasattr(app.state, "tavily")
    ):
        raise RuntimeError("Tool wrappers must be initialized before llm_with_tool")

    tools = [app.state.arxiv, app.state.wiki, app.state.tavily]
    llm = ChatGroq(model="qwen/qwen3-32b")
    llm_with_tool = llm.bind_tools(tools)
    app.state.llm_with_tool = llm_with_tool
    app.state.tools = tools
    logger.info("llm with tool initialized")


async def init_search_graph(app: FastAPI) -> None:
    # Verify dependencies are initialized
    if not hasattr(app.state, "llm_with_tool") or not hasattr(app.state, "tools"):
        raise RuntimeError(
            "llm_with_tool and tools must be initialized before search_graph"
        )

    # Define State
    class State(TypedDict):
        messages: Annotated[list[AnyMessage], add_messages]

    # Define tool calling node
    def tool_calling_llm(state: State):
        return {"messages": [app.state.llm_with_tool.invoke(state["messages"])]}

    # Build the graph
    builder = StateGraph(State)
    builder.add_node("tool_calling_llm", tool_calling_llm)
    builder.add_node("tools", ToolNode(app.state.tools))

    # Add edges
    builder.add_edge(START, "tool_calling_llm")
    builder.add_conditional_edges(
        "tool_calling_llm",
        tools_condition,
    )
    builder.add_edge("tools", "tool_calling_llm")

    graph = builder.compile()
    app.state.search_graph = graph

    # Display graph structure as Mermaid code
    try:
        mermaid_code = graph.get_graph().draw_mermaid()
        logger.info(f"search graph initialized. Graph structure:\n{mermaid_code}")
    except Exception as e:
        logger.warning(f"Could not generate mermaid diagram: {e}")
        logger.info("search graph initialized")


async def init_mcp_client(app: FastAPI) -> None:
    """Initialize the MCP client pool for communicating with MCP server."""
    # Get the path to the MCP server script (now inside app/tools/mcp/)

    # Get current file location
    current_file = Path(__file__)
    logger.info(f"Current file location: {current_file}")

    # Try different path strategies
    possible_paths = [
        # New location: backend/app/tools/lifetime.py -> mcp/server.py
        current_file.parent / "mcp" / "server.py",
        # Docker: /app/app/tools/mcp/server.py
        Path("/app/app/tools/mcp/server.py"),
        # Relative to working directory
        Path.cwd() / "app" / "tools" / "mcp" / "server.py",
    ]

    mcp_server_script = None
    for path in possible_paths:
        logger.info(f"Checking MCP server path: {path}")
        if path.exists():
            mcp_server_script = path
            logger.info(f"Found MCP server at: {mcp_server_script}")
            break

    if not mcp_server_script:
        error_msg = f"MCP server script not found. Tried paths:\n"
        error_msg += "\n".join(f"  - {p}" for p in possible_paths)
        raise RuntimeError(error_msg)

    # Create and initialize MCP client pool
    mcp_pool = MCPClientPool(str(mcp_server_script), pool_size=1)
    await mcp_pool.initialize()

    app.state.mcp_client = mcp_pool
    logger.info(f"MCP client initialized with server: {mcp_server_script}")
