from mysql.connector import pooling
from mysql.connector.pooling import MySQLConnectionPool, PooledMySQLConnection

from src.database_connector.dbms.dbms import DBMS
from configure import local_mysql_config, app_name
from src.logger import AppLogger

class MySqlDBMS(DBMS):
	def __init__(self) -> None:
		super().__init__()
		self.__context: MySQLConnectionPool = pooling.MySQLConnectionPool(pool_name=f"{app_name.lower()}_pool", pool_size=1, **local_mysql_config)

	def exe_insert(self, query, params):
		try:
			AppLogger.d(str.format(query, params))
			cnx: PooledMySQLConnection = self.__context.get_connection()
			cursor = cnx.cursor()
			cursor.execute(query, params)
			cnx.commit()
			id = cursor.lastrowid
			cursor.close()
			cnx.close()
			return id
		except Exception as e:
			AppLogger.e(f"[MYSQL_DBMS][exe_insert] Fatal: {e}")
			cursor.close()
			cnx.close()
			return None
		
	def exe_update(self, query, params) -> bool:
		try:
			AppLogger.d(str.format(query, params))
			cnx: PooledMySQLConnection = self.__context.get_connection()
			cursor = cnx.cursor()
			cursor.execute(query, params)
			cnx.commit()
			cursor.close()
			cnx.close()
			return True
		except Exception as e:
			AppLogger.e(f"[MYSQL_DBMS][exe_update] Fatal: {e}")
			cursor.close()
			cnx.close()
			return False
		
	def exe_select(self, query):
		try:
			AppLogger.d(str.format(query))
			cnx: PooledMySQLConnection = self.__context.get_connection()
			cursor = cnx.cursor()
			cursor.execute(query)
			result = cursor.fetchall()
			cursor.close()
			cnx.close()
			return result
		except Exception as e:
			AppLogger.e(f"[MYSQL_DBMS][exe_select] Fatal: {e}")
			cursor.close()
			cnx.close()
			return None
		
	def exe_delete(self, query) -> bool:
		try:
			AppLogger.d(str.format(query))
			cnx: PooledMySQLConnection = self.__context.get_connection()
			cursor = cnx.cursor()
			cursor.execute(query)
			cnx.commit()
			cursor.close()
			cnx.close()
			return True
		except Exception as e:
			AppLogger.e(f"[MYSQL_DBMS][exe_delete] Fatal: {e}")
			cursor.close()
			cnx.close()
			return False
		
	def start_transaction(self):
		self.__context.auto