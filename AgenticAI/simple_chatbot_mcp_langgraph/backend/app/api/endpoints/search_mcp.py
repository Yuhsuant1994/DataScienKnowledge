from app.log import default_logger as logger
from app.tools.dependency import get_llm_with_tool
from fastapi import APIRouter, Depends, Query, Request, status
from fastapi.responses import UJSONResponse
from starlette.requests import Request as StarletteRequest

router = APIRouter()


@router.post(
    "/search_mcp",
    responses={status.HTTP_204_NO_CONTENT: {"description": "No item found."}},
    response_class=UJSONResponse,
)
async def get_mcp_response(
    request: StarletteRequest,
    query: str = Query(
        default="type your question here",
        title="Search Query",
        description="Question to ask",
    ),
):
    """
    MCP endpoint with SQL tools: Single-pass execution with MCP + SQL database tools.

    This endpoint demonstrates:
    - MCP tools (arxiv, wikipedia, tavily) executed via MCP protocol subprocess
    - SQL tools executed directly against the database
    - LLM decides which tools to use in a single pass
    - Combines results from both MCP and SQL tools
    """
    try:
        # Get dependencies from app state
        llm_with_tool = request.app.state.llm_with_tool
        mcp_client = request.app.state.mcp_client
        db_manager = request.app.state.db_manager

        # Get available tools from MCP server
        mcp_tools = await mcp_client.list_tools()
        logger.info(f"MCP server has {len(mcp_tools)} tools available")

        # Check if database is available
        has_database = db_manager is not None
        # Get pre-fetched schema from app state (cached at startup)
        db_schema = getattr(request.app.state, "db_schema", None)

        if has_database:
            logger.info("SQL database tools available")
            if db_schema:
                logger.info("Using cached database schema from app.state")
            else:
                logger.warning("Database available but schema not cached")

        # Create comprehensive system prompt
        system_prompt = """You are a helpful assistant with access to multiple tools.

Available tools via MCP protocol:
1. **arxiv**: Search ArXiv for academic papers and research
2. **wikipedia**: Search Wikipedia for general knowledge and encyclopedia content
3. **tavily_search**: Search the web for current information, news, weather, and real-time data"""

        if has_database and db_schema:
            system_prompt += f"""

Available SQL database tools:
4. **query_sales_database_impl**: Execute SQL queries on sales database

DATABASE SCHEMA (already fetched for you):
{db_schema}

Use this schema to write SQL queries directly. Common queries:
- Count records: SELECT COUNT(*) FROM table_name
- Join tables: SELECT * FROM sales_order so JOIN order_details od ON so.order_id = od.order_id"""

        system_prompt += """

INSTRUCTIONS:
- If question is about research/papers: use arxiv
- If question is about general knowledge: use wikipedia
- If question is about current events/weather/news: use tavily_search"""

        if has_database:
            system_prompt += """
- If question is about sales data (customers, orders, products, revenue, purchases, etc.):
  1. Write SQL query using the provided schema
  2. Call query_sales_database_impl() with your SQL query
  3. Return actual data, NOT just SQL suggestions"""

        system_prompt += """

- If MULTIPLE questions: call ALL necessary tools
- Always EXECUTE tools, don't just describe what you would do

Example: "How many sales records and what is the weather in Taipei?" → call query_sales_database_impl AND tavily_search."""

        # First LLM call with system prompt to determine which tools to use
        full_query = f"{system_prompt}\n\nUser question: {query}"
        ai_message = llm_with_tool.invoke(full_query)

        # Track tools used
        tools_used = []
        tool_results = []

        # Execute tool calls if any
        if hasattr(ai_message, "tool_calls") and ai_message.tool_calls:
            import asyncio

            # Helper functions for parallel execution
            async def execute_sql_task(query):
                try:
                    return db_manager.execute_query(query)
                except Exception as e:
                    logger.error(f"Error executing SQL: {e}")
                    return f"Error - {str(e)}"

            async def execute_mcp_task(mcp_name, args):
                try:
                    logger.info(f"Calling MCP tool: {mcp_name}")
                    return await mcp_client.call_tool(mcp_name, args)
                except Exception as e:
                    logger.error(f"Error executing MCP tool {mcp_name}: {e}")
                    return f"Error - {str(e)}"

            # Separate SQL and MCP tool calls for parallel execution
            sql_tasks = []
            mcp_tasks = []
            task_metadata = []  # Track which task corresponds to which tool

            for tool_call in ai_message.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]

                logger.info(f"Tool called: {tool_name} with args: {tool_args}")

                # Handle SQL tools (executed directly)
                if tool_name == "get_database_schema_impl":
                    if has_database:
                        try:
                            result = db_manager.get_schema_info()
                            tool_results.append(f"**Database Schema**:\n{result}")
                            # Don't show schema tool in UI
                        except Exception as e:
                            logger.error(f"Error getting schema: {e}")
                            tool_results.append(f"**Database Schema**: Error - {str(e)}")
                    continue  # Skip adding to tools_used (internal tool)

                elif tool_name == "query_sales_database_impl":
                    if has_database:
                        sql_query = tool_args.get("sql_query", "")
                        tools_used.append({"tool": tool_name, "ai_gen_query": sql_query})

                        # Add SQL task for parallel execution
                        sql_tasks.append(execute_sql_task(sql_query))
                        task_metadata.append(("sql", tool_name, sql_query))
                    else:
                        tool_results.append("**SQL Query**: Database not available")

                # Handle MCP tools (executed via MCP protocol)
                else:
                    query_arg = tool_args.get("query", "")

                    # Map LangChain tool names to MCP tool names
                    mcp_tool_name_map = {
                        "arxiv": "arxiv",
                        "wikipedia": "wikipedia",
                        "tavily_search_results_json": "tavily_search",
                    }

                    mcp_tool_name = mcp_tool_name_map.get(tool_name, tool_name)

                    # Track the tool usage
                    tools_used.append({"tool": tool_name, "ai_gen_query": query_arg})

                    # Add MCP task for parallel execution
                    mcp_tasks.append(execute_mcp_task(mcp_tool_name, {"query": query_arg}))
                    task_metadata.append(("mcp", tool_name, query_arg))

            # Execute all tasks in parallel
            all_tasks = sql_tasks + mcp_tasks
            if all_tasks:
                logger.info(f"Executing {len(all_tasks)} tools in parallel ({len(sql_tasks)} SQL, {len(mcp_tasks)} MCP)")
                results = await asyncio.gather(*all_tasks)

                # Format results with proper labels
                for i, result in enumerate(results):
                    task_type, tool_name, query = task_metadata[i]
                    if task_type == "sql":
                        tool_results.append(f"**SQL Query Results**:\n{result}")
                    else:  # mcp
                        tool_results.append(f"**{tool_name}** (via MCP):\n{result}")

            # Second LLM call with tool results to generate final response
            if tool_results:
                context = "\n\n".join(tool_results)
                final_prompt = f"""Based on the following information from tools, please answer the user's question: "{query}"

Tool Results:
{context}

Provide a clear and concise answer:"""
                final_response = llm_with_tool.invoke(final_prompt)

                # Extract content from the response
                if hasattr(final_response, "content"):
                    final_answer = final_response.content
                else:
                    final_answer = str(final_response)
            else:
                final_answer = (
                    ai_message.content
                    if hasattr(ai_message, "content")
                    else "I couldn't generate a response."
                )
        else:
            # No tools needed, return the AI's direct response
            final_answer = (
                ai_message.content
                if hasattr(ai_message, "content")
                else "I couldn't generate a response."
            )

        return {"response": final_answer, "tools": tools_used}

    except Exception as e:
        logger.error(f"Error processing MCP search query: {e}")
        return {"error": str(e)}
