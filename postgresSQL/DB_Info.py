from main import logger
from connection_pool import *


def fetch_database_info():
    """
    查询数据库的相关信息
    :return: 包含数据库信息的字典，如果失败则返回包含错误信息的字典
    """
    try:
        conn = get_connection()
        if conn:
            cursor = conn.cursor()

            # 获取数据库版本
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()[0]
            logger.info(f"Database version: {db_version}")

            # 获取当前用户
            cursor.execute("SELECT current_user;")
            current_user = cursor.fetchone()[0]
            logger.info(f"Current user: {current_user}")

            # 获取已连接的数据库名称
            cursor.execute("SELECT current_database();")
            current_database = cursor.fetchone()[0]
            logger.info(f"Current database: {current_database}")

            # 获取数据库中的表
            cursor.execute("""
                SELECT tablename 
                FROM pg_catalog.pg_tables 
                WHERE schemaname = 'public';
            """)
            tables = cursor.fetchall()
            logger.info(f"Tables: {tables}")

            cursor.close()
            release_connection(conn)

            return {
                "db_version": db_version,
                "current_user": current_user,
                "current_database": current_database,
                "tables": tables
            }
        else:
            error_message = "无法连接数据库"
            logger.error("Failed to connect to database")
            return {"error": error_message}
    except Exception as error:
        logger.error(f"Error happened: {str(error)}")
        return {"error": str(error)}