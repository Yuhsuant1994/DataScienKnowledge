import os
from pathlib import Path
from typing import Annotated

from app.log import default_logger as logger
from app.tools.mcp import MCPClientPool
from app.tools.sql_tools import DatabaseManager, create_sql_tools
from app.tools.tool_factory import create_tools
from fastapi import FastAPI
from langchain_core.messages import AnyMessage, SystemMessage
from langchain_groq import ChatGroq
import json
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict
# how many records do we have in sales, who bought the most product, what is the weather now in taipei, what is the latest NLP paper

async def init_tools(app: FastAPI) -> None:
    """Initialize all tools using the shared factory."""
    arxiv, wiki, tavily = create_tools()
    app.state.arxiv = arxiv
    app.state.wiki = wiki
    app.state.tavily = tavily
    logger.info("Tools initialized using shared factory (arxiv, wikipedia, tavily)")


async def init_database(app: FastAPI) -> None:
    """Initialize database connection and SQL tools."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        logger.warning("DATABASE_URL not set, skipping database initialization")
        app.state.db_manager = None
        app.state.sql_tools = []
        return

    try:
        db_manager = DatabaseManager(database_url)
        await db_manager.initialize()
        app.state.db_manager = db_manager

        # Create SQL tools with the database manager
        sql_tools = create_sql_tools(db_manager)
        app.state.sql_tools = sql_tools
        logger.info("Database and SQL tools initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        app.state.db_manager = None
        app.state.sql_tools = []


async def init_llm_with_tool(app: FastAPI) -> None:
    # Verify dependencies are initialized
    if (
        not hasattr(app.state, "arxiv")
        or not hasattr(app.state, "wiki")
        or not hasattr(app.state, "tavily")
    ):
        raise RuntimeError("Tool wrappers must be initialized before llm_with_tool")

    # Combine API tools with SQL tools
    tools = [app.state.arxiv, app.state.wiki, app.state.tavily]

    # Add SQL tools if database is initialized
    if hasattr(app.state, "sql_tools") and app.state.sql_tools:
        tools.extend(app.state.sql_tools)
        logger.info(f"Added {len(app.state.sql_tools)} SQL tools to the tool set")

    llm = ChatGroq(model="qwen/qwen3-32b")
    llm_with_tool = llm.bind_tools(tools)
    app.state.llm_with_tool = llm_with_tool
    app.state.tools = tools
    logger.info(f"llm with tool initialized with {len(tools)} tools total")


async def init_db_schema(app: FastAPI) -> None:
    """Pre-fetch and cache database schema for use in system prompts."""
    db_schema = None
    if hasattr(app.state, "db_manager") and app.state.db_manager:
        try:
            db_schema = app.state.db_manager.get_schema_info()
            logger.info("Database schema pre-fetched and cached in app.state")
        except Exception as e:
            logger.error(f"Failed to fetch schema: {e}")

    # Store schema in app state for both endpoints to use
    app.state.db_schema = db_schema


async def init_search_graph(app: FastAPI) -> None:
    # Verify dependencies are initialized
    if not hasattr(app.state, "llm_with_tool") or not hasattr(app.state, "tools"):
        raise RuntimeError(
            "llm_with_tool and tools must be initialized before search_graph"
        )

    # Get pre-fetched schema from app state
    db_schema = getattr(app.state, "db_schema", None)

    # Define State
    class State(TypedDict):
        messages: Annotated[list[AnyMessage], add_messages]

    # Tool calling node with comprehensive prompting
    def tool_calling_llm(state: State):
        messages = state["messages"]

        # Add system message on first turn only
        if len(messages) == 1:
            system_prompt = """You are a helpful assistant with access to multiple tools.

Available tools:
1. **query_sales_database_impl**: Execute SQL queries on sales database (orders, customers, products, revenue, etc.)
2. **arxiv**: Search academic papers
3. **wikipedia**: Search Wikipedia
4. **tavily_search_results_json**: Web search for current info"""

            if db_schema:
                system_prompt += f"""

DATABASE SCHEMA (already fetched for you):
{db_schema}

Use this schema to write SQL queries directly. Common queries:
- Count records: SELECT COUNT(*) FROM table_name
- Find top customer: SELECT customer_name, SUM(quantity) FROM sales_order JOIN order_details USING(order_id) GROUP BY customer_name ORDER BY SUM(quantity) DESC LIMIT 1"""

            system_prompt += """

INSTRUCTIONS:
- If question is about sales data (customers, orders, products, revenue, purchases, etc.):
  1. Write SQL query using the provided schema
  2. Call query_sales_database_impl() with your SQL query
  3. Return actual data, NOT just SQL suggestions

- If question is about research/papers: use arxiv
- If question is about general knowledge: use wikipedia
- If question is about current events/weather: use tavily

- If MULTIPLE questions: call ALL necessary tools
- Always EXECUTE tools, don't just describe what you would do

Example: "Who bought the most?" → call query_sales_database_impl with SQL, return actual answer."""

            system_msg = SystemMessage(content=system_prompt)
            messages = [system_msg] + messages

        return {"messages": [app.state.llm_with_tool.invoke(messages)]}

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
