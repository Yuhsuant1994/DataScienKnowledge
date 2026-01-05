from app.log import default_logger as logger
from app.tools.dependency import get_llm_with_tool
from fastapi import APIRouter, Depends, Query, Request, status
from fastapi.responses import UJSONResponse

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
