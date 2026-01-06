"""
Shared tool factory for creating tool instances.
This ensures consistent tool configuration across LangGraph and MCP server.
"""

from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper


def create_tools():
    """
    Create and return all tools with consistent configuration.

    This function is used by both:
    - FastAPI app (for LangGraph endpoint)
    - MCP server subprocess (for MCP endpoint)

    Returns:
        tuple: (arxiv_tool, wiki_tool, tavily_tool)
    """
    # ArXiv tool
    arxiv_wrapper = ArxivAPIWrapper(top_k_results=2, doc_content_chars_max=500)
    arxiv_tool = ArxivQueryRun(
        api_wrapper=arxiv_wrapper, description="Query arxiv papers"
    )

    # Wikipedia tool
    wiki_wrapper = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=500)
    wiki_tool = WikipediaQueryRun(
        api_wrapper=wiki_wrapper, description="Query wikipedia articles"
    )

    # Tavily search tool
    tavily_tool = TavilySearchResults()

    return arxiv_tool, wiki_tool, tavily_tool
