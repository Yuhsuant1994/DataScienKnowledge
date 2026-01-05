from app.log import default_logger as logger
from fastapi import FastAPI
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_groq import ChatGroq


async def init_arxiv_wrapper(app: FastAPI) -> None:
    api_wrapper_arxiv = ArxivAPIWrapper(top_k_results=2, doc_content_chars_max=500)
    arxiv = ArxivQueryRun(
        api_wrapper=api_wrapper_arxiv, description="Query arxiv papers"
    )
    app.state.arxiv = arxiv
    logger.info("arxiv api wrapper initialized")


async def init_wikipedia_wrapper(app: FastAPI) -> None:
    api_wrapper_wiki = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=500)
    wiki = WikipediaQueryRun(
        api_wrapper=api_wrapper_wiki, description="Query wikipedia articles"
    )
    app.state.wiki = wiki
    logger.info("wikipedia api wrapper initialized")


async def init_tavily_wrapper(app: FastAPI) -> None:
    tavily = TavilySearchResults()
    app.state.tavily = tavily
    logger.info("tavily api wrapper initialized")


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
    logger.info("llm with tool initialized")
