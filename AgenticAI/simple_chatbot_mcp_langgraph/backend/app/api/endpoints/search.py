from app.log import default_logger as logger
from app.tools.dependency import get_llm_with_tool, get_search_graph
from fastapi import APIRouter, Depends, Query, Request, status
from fastapi.responses import UJSONResponse
from langchain_core.messages import HumanMessage

router = APIRouter()


@router.post(
    "/search",
    responses={status.HTTP_204_NO_CONTENT: {"description": "No item found."}},
    response_class=UJSONResponse,
)
async def get_response(
    request: Request,
    query: str = Query(
        default="type your question here",
        title="Search Query",
        description="Question to ask",
    ),
    llm_with_tool=Depends(get_llm_with_tool),
):
    try:
        response = llm_with_tool.invoke(query)
        return {"response": response}
    except Exception as e:
        logger.error(f"Error processing search query: {e}")
        return {"error": str(e)}


@router.post(
    "/search_graph",
    responses={status.HTTP_204_NO_CONTENT: {"description": "No item found."}},
    response_class=UJSONResponse,
)
async def get_graph_response(
    request: Request,
    query: str = Query(
        default="type your question here",
        title="Search Query",
        description="Question to ask",
    ),
    search_graph=Depends(get_search_graph),
):
    try:
        # Invoke the graph with the user query
        messages = search_graph.invoke({"messages": HumanMessage(content=query)})

        # Extract the final response and tool calls
        final_response = ""
        tools_used = []

        for message in messages["messages"]:
            # Check if it's an AI message with tool calls
            if hasattr(message, "tool_calls") and message.tool_calls:
                for tool_call in message.tool_calls:
                    tools_used.append(
                        {
                            "tool": tool_call["name"],
                            "ai_gen_query": tool_call["args"].get("query", ""),
                        }
                    )

            # Get the final AI response (last AI message without tool calls)
            if (
                hasattr(message, "content")
                and message.content
                and not (hasattr(message, "tool_calls") and message.tool_calls)
            ):
                final_response = message.content

        return {"response": final_response, "tools": tools_used}
    except Exception as e:
        logger.error(f"Error processing search query: {e}")
        return {"error": str(e)}
