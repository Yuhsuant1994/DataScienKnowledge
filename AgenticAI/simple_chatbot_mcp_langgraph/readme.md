# Chatbot with MCP and LangGraph

Three approaches to building an AI chatbot with tool calling: simple LLM, LangGraph iterative, and MCP subprocess execution.

---

## most simple workflow
```mermaid
graph TD
    START([User Query]) --> LLM[LLM]
    LLM --> END([Response])
    style LLM fill:#FFD700
```


## 1. `/search` - Simple LLM Query

LLM has tools bound but doesn't execute them - returns raw response.

```mermaid
graph TD
    START([User Query]) --> LLM[LLM with Tools Bound<br/>llm_with_tool.invoke]
    LLM -->|May generate tool calls| RESP[Raw Response Returned<br/>Tool calls NOT executed]
    RESP --> END([Response may contain<br/>unexecuted tool call requests])

    style LLM fill:#FFD700
    style RESP fill:#FFA07A
    style END fill:#FFA07A
```

**Features:**
- ❌ Tools bound but never executed
- ❌ No tool result synthesis
- ⚠️ Response may contain tool call requests as text

**Use case:** Demo of non-functional tool binding

---

## 2. `/search_graph` - LangGraph Iterative

Automatic tool execution with looping via LangGraph's ToolNode.

```mermaid
graph TD
    START([User Query]) --> LLM[LLM Node<br/>Rewrite queries]
    LLM -->|Has tool calls?| CONDITION{Condition}
    CONDITION -->|Yes| TOOLS[ToolNode<br/>AUTO: extract, find, execute, format]
    CONDITION -->|No| END([Final Answer])

    TOOLS --> SQL[SQL Direct<br/>auto-triggered by ToolNode]
    TOOLS --> API[APIs Direct<br/>auto-triggered by ToolNode]

    SQL --> TOOLS
    API --> TOOLS
    TOOLS --> LLM

    style LLM fill:#FFD700
    style TOOLS fill:#DDA0DD
    style SQL fill:#90EE90
    style API fill:#FFB6C1
```

**Features:**
- ✅ Automatic tool execution & looping via ToolNode
- ✅ All tools direct execution (SQL, ArXiv, Wikipedia, Tavily)
- ✅ LangGraph handles iteration logic automatically

**Use case:** Complex multi-step queries with full automation

---

## 3. `/search_mcp` - Single-Pass with MCP

Manual execution loop, MCP subprocess for some tools.

```mermaid
graph TD
    START([User Query]) --> LLM1[LLM Call 1<br/>Decide tools]
    LLM1 --> MANUAL[MANUAL for loop<br/>extract, check, map, execute, collect]

    MANUAL -->|Collect SQL tasks| SQL[SQL Direct<br/>YOU call db_manager.execute_query]
    MANUAL -->|Collect MCP tasks| MCP[MCP Subprocess<br/>YOU call mcp_client.call_tool]

    SQL --> PARALLEL[asyncio.gather<br/>Execute all in parallel]
    MCP --> PARALLEL

    PARALLEL --> MERGE[Merge Results]

    MERGE --> LLM2[LLM Call 2<br/>Synthesize answer]
    LLM2 --> END([Final Answer])

    style LLM1 fill:#FFD700
    style LLM2 fill:#FFD700
    style MANUAL fill:#FFA07A
    style PARALLEL fill:#87CEEB
    style SQL fill:#90EE90
    style MCP fill:#FFB6C1
```

**Features:**
- ⚠️ Manual tool orchestration - custom loop code
- ✅ MCP subprocess (arxiv, wikipedia, tavily) - isolated execution
- ✅ SQL direct execution - fast local execution
- ✅ **Parallel tool execution** - all tools run simultaneously via asyncio.gather()
- ❌ No automatic looping (single-pass only)
- ⚠️ Requires manual tool name mapping
- ⚠️ Requires manual result collection

**Use case:** Demonstrating MCP protocol with fine-grained control and parallel execution

---

## 4. Hybrid: LangGraph + MCP *(concept, not implemented)*

Combines automatic iteration with MCP isolation.

```mermaid
graph TD
    START([User Query]) --> LLM[LLM<br/>Rewrite queries]
    LLM --> TOOLS[Tool Node<br/>Execute all tools]

    TOOLS --> SQL[SQL Direct]
    TOOLS --> MCP[MCP Subprocess<br/>ArXiv, Wikipedia, Tavily]

    SQL --> RESULTS[Results]
    MCP --> RESULTS

    RESULTS --> LLM
    LLM --> END([Final Answer])

    style LLM fill:#FFD700
    style TOOLS fill:#DDA0DD
    style SQL fill:#90EE90
    style MCP fill:#FFB6C1
```

**Why this is ideal:**
- ✅ LangGraph automatic iteration
- ✅ SQL direct (fast)
- ✅ MCP subprocess (isolated)

---

## Comparison

| Feature | `/search` | `/search_graph` | `/search_mcp` | Hybrid *(concept)* |
|---------|-----------|----------------|---------------|-------------------|
| Tool orchestration | ❌ None | ✅ **Automatic** (ToolNode) | ⚠️ **Manual** (custom loop) | ✅ Automatic (ToolNode) |
| Looping | ❌ No | ✅ Yes (automatic) | ❌ No (single-pass) | ✅ Yes (automatic) |
| Tool execution triggering (API / SQL) | ❌ No | ✅ **Auto-triggered** by ToolNode | ⚠️ **Manual-triggered** (YOU call) | ✅ Auto-triggered |
| MCP subprocess | ❌ No | ❌ No | ✅ Yes (YOU call it) | ✅ Yes (ToolNode calls it) |
| API tools (arxiv, wiki, tavily) | ❌ No | ✅ Direct (ToolNode calls) | ✅ MCP subprocess (YOU call) | ✅ MCP subprocess |
| Best for | Demo | Complex workflows | **MCP demo & custom logic** | Production |

---

## Key Concepts

**Query Rewriting:** Done by LLM, not MCP
- User: "How many sales and weather in Taipei?"
- LLM rewrites: `{"sql": "SELECT COUNT(*)", "query": "weather Taipei"}`

**MCP Role:** Execute tools in subprocess, not rewrite queries

**Schema Pre-fetching:** Database schema cached at startup, injected in prompts

---

## Hybrid Approach: LangGraph + MCP *(concept)*

This combines the strengths of both architectures:

**From LangGraph:**
- Automatic iteration and looping
- Unified tool interface via `ToolNode`
- Parallel tool execution
- Error recovery and retry capability

**From MCP:**
- Process isolation (tools can crash safely)
- ersion delegation to protocol providers

**Combined Benefits:**
- ✅ Best of both: iteration + isolation
- ✅ Direct SQL (fast) + MCP subprocess (safe)

**Example:** Complex query requiring multiple tools with automatic retry/refinement.

```mermaid
graph TD
    START([User Query:<br/>How many sales and<br/>what's the weather in Taipei<br/>and latest NLP paper?]) --> SYSTEM[System Prompt<br/>includes pre-fetched DB schema]

    SYSTEM --> LLM1[LLM analyzes query<br/>rewrites to specific queries<br/>decides to call 3 tools]

    LLM1 -->|Generated queries:<br/>SQL: SELECT COUNT&#40;*&#41; FROM sales_order<br/>Tavily: weather Taipei<br/>ArXiv: NLP papers| TOOLS[Tool Node<br/>executes tools in parallel]

    subgraph "Tool Executions"
        TOOLS --> SQL_EXEC[SQL Tool:<br/>query_sales_database_impl]
        TOOLS --> MCP_CLIENT[MCP Client Pool]

        subgraph "SQL: Direct DB Access"
            SQL_EXEC --> SQL_VALIDATE[Validate query<br/>SELECT only]
            SQL_VALIDATE --> SQL_DB[(PostgreSQL<br/>Execute:<br/>SELECT COUNT&#40;*&#41; FROM sales_order)]
            SQL_DB --> SQL_RESULT[Result: 500 records]
        end

        subgraph "MCP Subprocess - handles multiple tools"
            MCP_CLIENT --> MCP_SERVER[MCP Server subprocess<br/>provides 3 tools:<br/>arxiv, wikipedia, tavily]

            MCP_SERVER -->|tavily_search<br/>query: weather Taipei| TAVILY_API[Tavily API]
            MCP_SERVER -->|arxiv<br/>query: NLP papers| ARXIV_API[ArXiv API]

            TAVILY_API --> WEB_RESULT[Result: 25°C sunny]
            ARXIV_API --> PAPER_RESULT[Result: Latest paper info]
        end
    end

    SQL_RESULT --> MERGE[Merge all results]
    WEB_RESULT --> MERGE
    PAPER_RESULT --> MERGE

    MERGE --> LLM2[LLM synthesizes<br/>final answer]

    LLM2 --> END([Response:<br/>500 sales records,<br/>Taipei is 25°C sunny,<br/>latest NLP paper is...])

    style LLM1 fill:#FFD700
    style LLM2 fill:#FFD700
    style SQL_EXEC fill:#90EE90
    style SQL_DB fill:#4682B4
```

**Key difference from current implementations:**
- Loop back to LLM is automatic (not shown in single-pass `/search_mcp`)
- All tools accessible through one unified `ToolNode`
- MCP tools wrapped as LangChain tools for seamless integration