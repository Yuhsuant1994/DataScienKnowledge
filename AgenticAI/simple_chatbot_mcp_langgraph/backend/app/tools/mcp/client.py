"""
MCP Client wrapper for communicating with MCP servers via subprocess.
"""

import asyncio
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.log import default_logger as logger
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:
    """Client for communicating with MCP servers."""

    def __init__(self, server_script_path: str):
        """
        Initialize the MCP client.

        Args:
            server_script_path: Path to the MCP server Python script
        """
        self.server_script_path = server_script_path
        self.session: Optional[ClientSession] = None
        self.read_stream = None
        self.write_stream = None
        self._stdio_context = None
        self._session_context = None
        self._initialized = False

    async def connect(self):
        """Connect to the MCP server via stdio."""
        if self._initialized:
            logger.info("MCP client already connected")
            return

        try:
            import os

            # Server parameters for stdio communication
            # Pass environment variables including API keys and PYTHONPATH
            env_vars = {
                "GROQ_API_KEY": os.getenv("GROQ_API_KEY", ""),
                "TAVILY_API_KEY": os.getenv("TAVILY_API_KEY", ""),
                "groq_api": os.getenv("groq_api", ""),
                "tavily_api": os.getenv("tavily_api", ""),
                # Set PYTHONPATH so subprocess can find 'app' module
                "PYTHONPATH": "/app",
            }

            server_params = StdioServerParameters(
                command="python",
                args=[self.server_script_path],
                env=env_vars,
            )

            # Create stdio client connection and keep context manager
            logger.info(f"Connecting to MCP server: {self.server_script_path}")
            self._stdio_context = stdio_client(server_params)
            self.read_stream, self.write_stream = await self._stdio_context.__aenter__()

            # Initialize session and keep context manager
            self._session_context = ClientSession(self.read_stream, self.write_stream)
            self.session = await self._session_context.__aenter__()

            # Initialize the connection
            await self.session.initialize()

            self._initialized = True
            logger.info("MCP client connected successfully")

        except Exception as e:
            logger.error(f"Failed to connect to MCP server: {e}")
            # Clean up on error
            if self._session_context:
                try:
                    await self._session_context.__aexit__(None, None, None)
                except:
                    pass
            if self._stdio_context:
                try:
                    await self._stdio_context.__aexit__(None, None, None)
                except:
                    pass
            raise

    async def list_tools(self) -> List[Dict[str, Any]]:
        """
        List all available tools from the MCP server.

        Returns:
            List of tool definitions
        """
        if not self._initialized or not self.session:
            await self.connect()

        try:
            result = await self.session.list_tools()
            tools = [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.inputSchema,
                }
                for tool in result.tools
            ]
            logger.info(f"Listed {len(tools)} tools from MCP server")
            return tools

        except Exception as e:
            logger.error(f"Failed to list tools: {e}")
            raise

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """
        Call a tool on the MCP server.

        Args:
            tool_name: Name of the tool to call
            arguments: Arguments to pass to the tool

        Returns:
            The tool's response as a string
        """
        if not self._initialized or not self.session:
            await self.connect()

        try:
            logger.info(f"Calling MCP tool: {tool_name} with args: {arguments}")
            result = await self.session.call_tool(tool_name, arguments)

            # Extract text content from the result
            if result.content:
                text_content = []
                for content in result.content:
                    if hasattr(content, "text"):
                        text_content.append(content.text)

                response = "\n".join(text_content)
                logger.info(f"MCP tool {tool_name} returned {len(response)} chars")
                return response
            else:
                logger.warning(f"MCP tool {tool_name} returned no content")
                return ""

        except Exception as e:
            logger.error(f"Failed to call tool {tool_name}: {e}")
            raise

    async def disconnect(self):
        """Disconnect from the MCP server."""
        try:
            # Exit session context first
            if self._session_context:
                await self._session_context.__aexit__(None, None, None)

            # Then exit stdio context
            if self._stdio_context:
                await self._stdio_context.__aexit__(None, None, None)

            logger.info("MCP client disconnected")
        except Exception as e:
            logger.error(f"Error disconnecting MCP client: {e}")

        self._initialized = False
        self.session = None
        self._session_context = None
        self._stdio_context = None


class MCPClientPool:
    """Pool manager for MCP clients to handle multiple requests."""

    def __init__(self, server_script_path: str, pool_size: int = 1):
        """
        Initialize the MCP client pool.

        Args:
            server_script_path: Path to the MCP server script
            pool_size: Number of clients to maintain in the pool
        """
        self.server_script_path = server_script_path
        self.pool_size = pool_size
        self.clients: List[MCPClient] = []
        self._lock = asyncio.Lock()

    async def initialize(self):
        """Initialize the client pool."""
        logger.info(f"Initializing MCP client pool with {self.pool_size} clients")
        for i in range(self.pool_size):
            client = MCPClient(self.server_script_path)
            await client.connect()
            self.clients.append(client)
        logger.info("MCP client pool initialized")

    async def get_client(self) -> MCPClient:
        """Get an available client from the pool."""
        async with self._lock:
            if not self.clients:
                # Create a new client if pool is empty
                client = MCPClient(self.server_script_path)
                await client.connect()
                return client
            return self.clients[0]  # Simple strategy: return first client

    async def list_tools(self) -> List[Dict[str, Any]]:
        """List tools using a client from the pool."""
        client = await self.get_client()
        return await client.list_tools()

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Call a tool using a client from the pool."""
        client = await self.get_client()
        return await client.call_tool(tool_name, arguments)

    async def shutdown(self):
        """Shutdown all clients in the pool."""
        logger.info("Shutting down MCP client pool")
        for client in self.clients:
            await client.disconnect()
        self.clients.clear()
        logger.info("MCP client pool shut down")
