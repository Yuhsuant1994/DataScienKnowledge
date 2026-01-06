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
    TRUE MCP endpoint: Uses MCP protocol to communicate with MCP server.

    This endpoint demonstrates:
    - FastAPI spawns MCP server as subprocess
    - Communicates via MCP protocol (stdio)
    - Tools are executed via MCP server
    - Single-pass execution (no iterative loops)
    """
    try:
        # Get the LLM and MCP client
        llm_with_tool = request.app.state.llm_with_tool
        mcp_client = request.app.state.mcp_client

        # Get available tools from MCP server
        mcp_tools = await mcp_client.list_tools()
        logger.info(f"MCP server has {len(mcp_tools)} tools available")

        # First LLM call to determine which tools to use
        ai_message = llm_with_tool.invoke(query)

        # Track tools used
        tools_used = []
        tool_results = []

        # Execute tool calls via MCP if any
        if hasattr(ai_message, "tool_calls") and ai_message.tool_calls:
            for tool_call in ai_message.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
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

                # Execute the tool via MCP server
                try:
                    logger.info(f"Calling MCP tool: {mcp_tool_name}")
                    result = await mcp_client.call_tool(
                        mcp_tool_name, {"query": query_arg}
                    )
                    tool_results.append(f"**{tool_name}** (via MCP): {result}")
                except Exception as e:
                    logger.error(f"Error executing MCP tool {mcp_tool_name}: {e}")
                    tool_results.append(f"**{tool_name}** (via MCP): Error - {str(e)}")

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
