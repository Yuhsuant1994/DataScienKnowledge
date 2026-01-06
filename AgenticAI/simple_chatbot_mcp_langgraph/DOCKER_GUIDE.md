# Docker Guide - Running Everything

This guide shows you how to run the complete system with Docker Compose.

## What Gets Started

When you run `docker-compose up`, you get **3 containers**:

1. **Backend** (FastAPI + MCP Server) - Port 8001
2. **Streamlit LangGraph UI** - Port 8501
3. **Streamlit MCP UI** - Port 8502

## Quick Start

```bash
# From simple_chatbot/ directory
docker-compose up --build -d
```

That's it! Everything starts automatically.

## Access the Apps

- **Backend API**: http://localhost:8001
  - Swagger docs: http://localhost:8001/docs
  - `/api/search` - Simple endpoint
  - `/api/search_graph` - LangGraph endpoint (iterative)
  - `/api/search_mcp` - MCP endpoint (subprocess communication)

- **LangGraph UI**: http://localhost:8501
  - Uses `/api/search_graph` endpoint
  - Shows iterative tool calling with loops

- **MCP UI**: http://localhost:8502
  - Uses `/api/search_mcp` endpoint
  - Shows MCP protocol with subprocess communication

## What Happens Behind the Scenes

### Backend Container:
```
1. FastAPI starts
2. init_mcp_client() is called
3. MCP server subprocess is spawned automatically
4. MCP client connects via stdio
5. Ready to serve requests!
```

### Streamlit Containers:
```
1. Streamlit starts
2. Connects to backend via API_URL env variable
3. Makes HTTP requests to FastAPI
4. Displays results in UI
```

## Environment Variables

Make sure `backend/.env` has:
```
groq_api=your_groq_api_key
tavily_api=your_tavily_api_key
```

Docker Compose will load these automatically.

## Stopping Everything

```bash
# Stop all containers
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Stop and remove images
docker-compose down --rmi all
```

## Rebuilding

```bash
# Rebuild everything
docker-compose up --build

# Rebuild specific service
docker-compose build backend
docker-compose build streamlit-langgraph
docker-compose build streamlit-mcp
```

## Logs

```bash
# View all logs
docker-compose logs

# Follow logs
docker-compose logs -f

# Logs for specific service
docker-compose logs backend
docker-compose logs streamlit-langgraph
docker-compose logs streamlit-mcp
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Network                        │
│                                                          │
│  ┌────────────────────┐                                 │
│  │  streamlit-langgraph│  Port 8501                     │
│  │  (LangGraph UI)    │─────────────┐                   │
│  └────────────────────┘              │                   │
│                                      │                   │
│  ┌────────────────────┐              ▼                   │
│  │  streamlit-mcp     │  Port 8502  ┌─────────────────┐ │
│  │  (MCP UI)          │─────────────▶│   backend       │ │
│  └────────────────────┘              │   (FastAPI)     │ │
│                                      │   Port 8001     │ │
│                                      │                 │ │
│                                      │  ┌──────────┐   │ │
│                                      │  │MCP Server│   │ │
│                                      │  │(subprocess)  │ │
│                                      │  └──────────┘   │ │
│                                      └─────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Troubleshooting

### Issue: Port already in use
```bash
# Check what's using the port
lsof -i :8001
lsof -i :8501
lsof -i :8502

# Kill the process or change ports in docker-compose.yml
```

### Issue: MCP server not found
- Check that `Dockerfile` (at root) includes COPY for mcp_server
- Check logs: `docker-compose logs backend`
- Should see: "Found MCP server at: /app/mcp_server/server.py"

### Issue: API connection refused
- Make sure backend is healthy: `docker-compose ps`
- Check backend logs: `docker-compose logs backend`
- Streamlit uses `http://backend:80` (Docker network name)

## Comparison: Run All vs. Individual

### Run All (Recommended):
```bash
docker-compose up --build
```
✅ Everything starts together
✅ Proper networking
✅ Easy to manage

### Run Individual (Advanced):
```bash
# Backend only
docker-compose up backend

# LangGraph UI only (backend must be running)
docker-compose up streamlit-langgraph

# MCP UI only (backend must be running)
docker-compose up streamlit-mcp
```

## Next Steps

1. Open http://localhost:8501 (LangGraph UI)
2. Open http://localhost:8502 (MCP UI) in another tab
3. Try the same query in both UIs
4. Compare response times and tool execution!

**Example queries:**
- "What is the weather in Taipei?"
- "Latest research on transformers from ArXiv"
- "Explain Python programming language"
