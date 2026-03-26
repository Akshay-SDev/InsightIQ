from sqlalchemy import create_engine, text
from agents import function_tool # type: ignore

from config import pg_db, pg_user, pg_password, pg_host, pg_port
from schema import DATABASE_SCHEMA, SCHEMA_DICT

DATABASE_URL = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"

engine = create_engine(DATABASE_URL)

@function_tool
def execute_query(query: str) -> list[tuple]:
    """Execute SQL query and return results
    Args:
        query (str): SQL query to execute
    Returns:
        list: Query results as list of tuples
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        return result.fetchall()
    
@function_tool
def get_db_schema() -> str:
    """Get database schema description for SQL agent"""
    return DATABASE_SCHEMA

@function_tool
def get_schema_dict() -> dict:
    """Get database schema dictionary for SQL agent"""
    return SCHEMA_DICT
