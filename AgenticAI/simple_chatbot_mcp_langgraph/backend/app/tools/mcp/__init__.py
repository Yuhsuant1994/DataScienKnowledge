"""MCP (Model Context Protocol) integration module."""

from .client import MCPClient, MCPClientPool

# Note: server.py is NOT imported here because it runs as a separate subprocess
# and should not be loaded during the main app import

__all__ = ["MCPClient", "MCPClientPool"]
