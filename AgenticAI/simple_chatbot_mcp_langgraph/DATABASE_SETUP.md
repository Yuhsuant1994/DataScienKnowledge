# Database Setup Guide

## Overview

The application now includes a PostgreSQL database that automatically loads your sales data from CSV files. The LangGraph agent can query this database using natural language.

## What's Been Added

### 1. PostgreSQL Database in Docker
- **Service**: `postgres` container running PostgreSQL 15
- **Database**: `sales_db`
- **User**: `chatbot_user`
- **Port**: 5432 (exposed to host)

### 2. Automatic Table Creation
When the Postgres container starts, it automatically:
- Creates `sales_order` table from `sales_order.csv`
- Creates `order_details` table from `order_details.csv`
- Creates indexes for better query performance
- Creates a `sales_summary` view joining both tables

### 3. SQL Tools in LangGraph
Your existing `search_graph` now has 5 tools:
1. **arxiv** - Search academic papers
2. **wikipedia** - Search Wikipedia
3. **tavily** - Web search
4. **get_database_schema** - View database structure (NEW)
5. **query_sales_database** - Execute SQL queries (NEW)

The LLM will automatically choose which tool to use based on your query.

## Database Schema

### sales_order table
```sql
- order_id: VARCHAR(20) PRIMARY KEY
- order_date: DATE
- customer_name: VARCHAR(100)
- state: VARCHAR(100)
- city: VARCHAR(100)
```

### order_details table
```sql
- id: SERIAL PRIMARY KEY
- order_id: VARCHAR(20) FOREIGN KEY
- amount: DECIMAL(10, 2)
- profit: DECIMAL(10, 2)
- quantity: INTEGER
- category: VARCHAR(50)
- sub_category: VARCHAR(50)
```

### sales_summary view (convenience)
Joins both tables for easy querying.

## How to Use

### 1. Set Environment Variables

Add to your `.env` file or docker-compose environment:
```bash
POSTGRES_PASSWORD=your_secure_password
DATABASE_URL=postgresql://chatbot_user:your_secure_password@postgres:5432/sales_db
```

### 2. Start the Services

```bash
docker-compose up -d
```

This will:
1. Start PostgreSQL container
2. Wait for it to be healthy
3. Load CSV data automatically
4. Start the backend with SQL tools enabled

### 3. Query Examples

Your LangGraph agent can now handle questions like:

**Sales Data Queries:**
- "What are the top 5 customers by total sales?"
- "Show me all orders from Gujarat"
- "What's the total profit by category?"
- "Which product sub-category has the highest profit margin?"
- "List all orders with negative profit"

**Combined Queries (SQL + API):**
- "What are the top selling categories and what does Wikipedia say about them?"
- "Show me orders from Maharashtra and research the latest trends in those product categories"

**External Knowledge:**
- "What are the latest papers on machine learning?" (uses arxiv)
- "Tell me about quantum computing" (uses wikipedia)
- "What's happening in AI today?" (uses tavily)

### 4. Verify Database Setup

Check if the database is running and tables are created:

```bash
# Connect to the database
docker exec -it chatbot-postgres psql -U chatbot_user -d sales_db

# Check tables
\dt

# View some data
SELECT * FROM sales_order LIMIT 5;
SELECT * FROM order_details LIMIT 5;

# Exit
\q
```

## Architecture

```
User Query → LangGraph search_graph
    ↓
LLM decides which tool to use:
    ├─→ Sales data question? → SQL tools
    ├─→ Research question? → API tools (arxiv, wiki, tavily)
    └─→ Complex question? → Multiple tools in sequence
```

## Safety Features

1. **Read-Only Queries**: Only SELECT queries are allowed
2. **Query Validation**: Dangerous keywords (DROP, DELETE, etc.) are blocked
3. **Result Limits**: Query results limited to 100 rows
4. **Connection Pooling**: Efficient database connection management

## Troubleshooting

### Database not connecting
```bash
# Check if Postgres is healthy
docker-compose ps

# View Postgres logs
docker-compose logs postgres

# Check backend logs for database connection
docker-compose logs backend
```

### Tables not created
```bash
# Manually run init script
docker exec -i chatbot-postgres psql -U chatbot_user -d sales_db < db/init.sql
```

### CSV data not loading
Make sure:
- CSV files are in the `db/` directory
- CSV files have headers matching the table columns
- Files use comma as delimiter

## Files Created/Modified

### New Files
- `db/init.sql` - Database initialization script
- `backend/app/tools/sql_tools.py` - SQL tools implementation
- `DATABASE_SETUP.md` - This file

### Modified Files
- `docker-compose.yml` - Added Postgres service
- `backend/requirements.txt` - Added sqlalchemy, psycopg2-binary
- `backend/app/tools/lifetime.py` - Added database initialization
- `backend/app/main.py` - Added init_database to startup

## Next Steps

### Optional: Add More Advanced Features

1. **Query Caching**: Cache common queries for faster responses
2. **Query Templates**: Pre-defined queries for common questions
3. **Data Validation**: Validate user inputs before querying
4. **Query Optimization**: Add more indexes based on usage patterns
5. **Analytics Dashboard**: Add endpoints for visualization

### Optional: Router Pattern

If you want to implement the router pattern (classify queries first):
- Add a router node to classify "sql" vs "api" vs "both"
- Route to specialized nodes based on classification
- More efficient for complex queries

Let me know if you want help implementing any of these!
