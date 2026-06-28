import os
import pymysql
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection():
    """
    Establishes and returns a connection to the RDS MySQL database using environment variables.
    """
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=5
        )
        return connection
    except Exception as e:
        logger.error(f"Failed to connect to RDS MySQL database: {e}")
        raise e

def init_db():
    """
    Initializes the database schema if tables do not exist.
    """
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Create urls table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS urls (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    original_url TEXT NOT NULL,
                    short_code VARCHAR(10) UNIQUE NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    total_clicks INT DEFAULT 0
                );
            """)
            # Create clicks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clicks (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    short_code VARCHAR(10) NOT NULL,
                    clicked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    ip_address VARCHAR(45),
                    user_agent VARCHAR(500)
                );
            """)
        connection.commit()
        logger.info("Database tables initialized successfully.")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
    finally:
        if connection:
            connection.close()

def save_url_rds(original_url: str, short_code: str) -> bool:
    """
    Saves a URL mapping to RDS.
    """
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "INSERT INTO urls (original_url, short_code) VALUES (%s, %s)"
            cursor.execute(sql, (original_url, short_code))
        connection.commit()
        return True
    except Exception as e:
        logger.error(f"Failed to save URL mapping to RDS for {short_code}: {e}")
        return False
    finally:
        if connection:
            connection.close()

def get_url_rds(short_code: str):
    """
    Retrieves a URL mapping from RDS.
    """
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "SELECT original_url, short_code, created_at, total_clicks FROM urls WHERE short_code = %s"
            cursor.execute(sql, (short_code,))
            return cursor.fetchone()
    except Exception as e:
        logger.error(f"Failed to retrieve URL mapping from RDS for {short_code}: {e}")
        return None
    finally:
        if connection:
            connection.close()

def increment_clicks_rds(short_code: str) -> bool:
    """
    Increments the click count in the RDS urls table.
    """
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "UPDATE urls SET total_clicks = total_clicks + 1 WHERE short_code = %s"
            cursor.execute(sql, (short_code,))
        connection.commit()
        return True
    except Exception as e:
        logger.error(f"Failed to increment click count in RDS for {short_code}: {e}")
        return False
    finally:
        if connection:
            connection.close()

def record_click_rds(short_code: str, ip_address: str, user_agent: str) -> bool:
    """
    Records a visit/click in the RDS clicks table.
    """
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "INSERT INTO clicks (short_code, ip_address, user_agent) VALUES (%s, %s, %s)"
            cursor.execute(sql, (short_code, ip_address, user_agent))
        connection.commit()
        return True
    except Exception as e:
        logger.error(f"Failed to record click in RDS clicks table for {short_code}: {e}")
        return False
    finally:
        if connection:
            connection.close()

def get_recent_urls_rds(limit: int = 5):
    """
    Retrieves the most recent N urls.
    """
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "SELECT original_url, short_code, created_at, total_clicks FROM urls ORDER BY created_at DESC LIMIT %s"
            cursor.execute(sql, (limit,))
            return cursor.fetchall()
    except Exception as e:
        logger.error(f"Failed to retrieve recent URLs from RDS: {e}")
        return []
    finally:
        if connection:
            connection.close()

def get_all_urls_rds():
    """
    Retrieves all URLs for the dashboard.
    """
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "SELECT original_url, short_code, created_at, total_clicks FROM urls ORDER BY created_at DESC"
            cursor.execute(sql)
            return cursor.fetchall()
    except Exception as e:
        logger.error(f"Failed to retrieve all URLs from RDS: {e}")
        return []
    finally:
        if connection:
            connection.close()
