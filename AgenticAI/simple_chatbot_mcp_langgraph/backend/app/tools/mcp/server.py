#!/usr/bin/env python3
"""
MCP Server that exposes ArXiv, Wikipedia, and Tavily search tools.

This server runs as a separate process and communicates via the MCP protocol.
"""

import asyncio
import os

# Import from app's tool factory (sibling directory)
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

# Add app directory to path: mcp/server.py -> ../../ (app directory)
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.tools.tool_factory import create_tools

# Load environment variables
load_dotenv()

# Initialize the MCP server
app = Server("search-tools-server")

# Initialize tools using shared factory
arxiv_tool, wiki_tool, tavily_tool = create_tools()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="arxiv",
            description="Search ArXiv for academic papers and research. Use this for scientific papers, research articles, and academic content.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query for ArXiv papers",
                    }
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="wikipedia",
            description="Search Wikipedia for general knowledge and encyclopedia content. Use this for factual information, definitions, and general topics.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query for Wikipedia",
                    }
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="tavily_search",
            description="Search the web for current information, news, and real-time data. Use this for recent events, current weather, news, and up-to-date information.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query for web search",
                    }
                },
                "required": ["query"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Execute a tool with the given arguments."""
    query = arguments.get("query", "")

    if not query:
        return [TextContent(type="text", text="Error: No query provided")]

    try:
        if name == "arxiv":
            result = arxiv_tool.invoke(query)
            return [TextContent(type="text", text=str(result))]

        elif name == "wikipedia":
            result = wiki_tool.invoke(query)
            return [TextContent(type="text", text=str(result))]

        elif name == "tavily_search":
            result = tavily_tool.invoke(query)
            # Format the results nicely
            if isinstance(result, list):
                formatted_result = "\n\n".join(
                    [
                        f"**{item.get('title', 'Unknown')}**\n{item.get('content', '')}\nURL: {item.get('url', '')}"
                        for item in result
                    ]
                )
                return [TextContent(type="text", text=formatted_result)]
            return [TextContent(type="text", text=str(result))]

        else:
            return [TextContent(type="text", text=f"Error: Unknown tool '{name}'")]

    except Exception as e:
        return [TextContent(type="text", text=f"Error executing {name}: {str(e)}")]


async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
