"""
MySQL Database Connection and Utilities
"""

import pymysql
import os
from dotenv import load_dotenv
from contextlib import contextmanager
from typing import Optional, Dict, Any
import json

load_dotenv()

# Database configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "assessment_orchestrator"),
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
    "autocommit": False
}

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = None
    try:
        conn = pymysql.connect(**DB_CONFIG)
        yield conn
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def get_db_cursor():
    """Get a database cursor (for use with connection context)"""
    conn = pymysql.connect(**DB_CONFIG)
    return conn, conn.cursor()

def init_db():
    """Initialize database - verify connection"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                return True
    except Exception as e:
        print(f"Database connection error: {e}")
        raise

def execute_query(query: str, params: Optional[tuple] = None) -> list:
    """Execute a SELECT query and return results"""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()

def execute_insert(query: str, params: Optional[tuple] = None) -> int:
    """Execute an INSERT query and return last insert ID"""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid

def execute_update(query: str, params: Optional[tuple] = None) -> int:
    """Execute an UPDATE query and return affected rows"""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            rows_affected = cursor.execute(query, params)
            conn.commit()
            return rows_affected

def log_api_call(
    user_id: Optional[int],
    endpoint: str,
    method: str,
    request_body: Optional[Dict] = None,
    response_status: int = 200,
    response_body: Optional[Dict] = None,
    internal_api_called: Optional[str] = None,
    llm_provider_used: Optional[str] = None,
    correlation_id: Optional[str] = None,
    execution_time_ms: Optional[int] = None,
    error_message: Optional[str] = None
):
    """Log API call to audit_logs table"""
    try:
        query = """
            INSERT INTO api_audit_logs 
            (user_id, endpoint, method, request_body, response_status, response_body,
             internal_api_called, llm_provider_used, correlation_id, execution_time_ms, error_message)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            user_id,
            endpoint,
            method,
            json.dumps(request_body) if request_body else None,
            response_status,
            json.dumps(response_body) if response_body else None,
            internal_api_called,
            llm_provider_used,
            correlation_id,
            execution_time_ms,
            error_message
        )
        execute_insert(query, params)
    except Exception as e:
        print(f"Failed to log API call: {e}")
