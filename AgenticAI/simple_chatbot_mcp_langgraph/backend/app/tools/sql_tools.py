"""SQL tools for querying the sales database."""

from typing import Optional

import sqlalchemy
from app.log import default_logger as logger
from langchain_community.utilities import SQLDatabase
from langchain_core.tools import tool
from sqlalchemy import create_engine, text


class DatabaseManager:
    """Manages database connection and provides querying capabilities."""

    def __init__(self, database_url: str):
        """Initialize database manager with connection URL."""
        self.database_url = database_url
        self.engine = None
        self.db = None

    async def initialize(self):
        """Initialize database connection."""
        try:
            self.engine = create_engine(self.database_url)
            # read schema
            self.db = SQLDatabase(self.engine)
            logger.info(f"Database connected successfully to: {self.database_url}")

            # Test connection
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT 1"))
                result.fetchone()
                logger.info("Database connection test successful")

        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise

    async def close(self):
        """Close database connection."""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connection closed")

    def get_schema_info(self) -> str:
        """Get database schema information."""
        if not self.db:
            return "Database not initialized"

        return self.db.get_table_info()

    def execute_query(self, query: str) -> str:
        """Execute a SQL query and return results."""
        if not self.engine:
            return "Database not initialized"

        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                # Fetch results
                rows = result.fetchall()

                if not rows:
                    return "Query executed successfully but returned no results."

                # Format results as a table
                columns = result.keys()
                output = " | ".join(columns) + "\n"
                output += "-" * len(output) + "\n"

                for row in rows[:100]:  # Limit to 100 rows for safety
                    output += " | ".join(str(val) for val in row) + "\n"

                if len(rows) > 100:
                    output += f"\n... ({len(rows) - 100} more rows)"

                return output

        except Exception as e:
            logger.error(f"Error executing query: {e}")
            return f"Error executing query: {str(e)}"


@tool
def get_database_schema() -> str:
    """Get the database schema information including table names and columns.

    Use this tool to understand what tables and columns are available in the database
    before writing SQL queries. This is helpful for:
    - Understanding what data is available
    - Finding the correct table and column names
    - Seeing the structure of the database

    Returns:
        str: Database schema information with table and column details
    """
    # This will be injected at runtime
    return "Schema information"


@tool
def query_sales_database(sql_query: str) -> str:
    """Execute a SQL query against the sales database.

    Use this tool to query sales data including orders, customers, and product information.

    The database has the following main tables:
    - sales_order: Contains order_id, order_date, customer_name, state, city
    - order_details: Contains order_id, amount, profit, quantity, category, sub_category
    - sales_summary: A view joining both tables for convenience

    Args:
        sql_query: A valid SQL SELECT query to execute. Only SELECT queries are allowed.
                  Example: "SELECT * FROM sales_order LIMIT 10"
                          "SELECT category, SUM(profit) FROM order_details GROUP BY category"

    Returns:
        str: Query results formatted as a table, or an error message if the query fails

    Important:
    - Only SELECT queries are allowed for safety
    - Results are limited to 100 rows
    - Use proper SQL syntax (PostgreSQL)
    - Always use WHERE clauses to limit results when possible
    """
    # Validate that it's a SELECT query
    query_upper = sql_query.strip().upper()
    if not query_upper.startswith("SELECT"):
        return "Error: Only SELECT queries are allowed for safety reasons."

    # Check for dangerous keywords
    dangerous_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE"]
    if any(keyword in query_upper for keyword in dangerous_keywords):
        return f"Error: Query contains dangerous keywords. Only SELECT queries are allowed."

    # This will be injected at runtime
    return "Query results"


def create_sql_tools(db_manager: DatabaseManager):
    """Create SQL tools with database manager injected."""

    @tool
    def get_database_schema_impl() -> str:
        """Get the database schema information including table names and columns.

        IMPORTANT: You should ALWAYS call this tool FIRST before writing any SQL queries
        to ensure you use the correct table and column names. This prevents errors from
        using non-existent tables or columns.

        Returns the complete database schema with all tables, columns, and data types.
        """
        return db_manager.get_schema_info()

    @tool
    def query_sales_database_impl(sql_query: str) -> str:
        """Execute a SQL query against the sales database.

        IMPORTANT: Call get_database_schema_impl() FIRST if you don't know the exact
        table and column names. Do not guess table names."""
        # Validate query
        query_upper = sql_query.strip().upper()
        if not query_upper.startswith("SELECT"):
            return "Error: Only SELECT queries are allowed for safety reasons."

        dangerous_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE"]
        if any(keyword in query_upper for keyword in dangerous_keywords):
            return "Error: Query contains dangerous keywords. Only SELECT queries are allowed."

        return db_manager.execute_query(sql_query)

    return [get_database_schema_impl, query_sales_database_impl]
