from configure import use_database
from src.database_connector.dbms.dbms import DBMS
from src.database_connector.dbms.mysql_dbms import MySqlDBMS
class DBConnector(object):
	_dbms: DBMS = None
	_instance = None

	@classmethod
	def instance(cls):
		if cls._instance is None:
			cls._instance = cls.__new__(cls)
			if use_database == "MYSQL":
				cls._instance._dbms = MySqlDBMS()
			else:
				raise Exception("Not Implementation")
		return cls._instance
	def exe_insert(self, query, params):
		return self._dbms.exe_insert(query, params)

	def exe_update(self, query, params):
		return self._dbms.exe_update(query, params)

	def exe_select(self, query):
		return self._dbms.exe_select(query)

	def exe_delete(self, query):
		return self._dbms.exe_delete(query)