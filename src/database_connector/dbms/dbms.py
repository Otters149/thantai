from abc import ABC, abstractmethod

class DBMS(ABC):
	@abstractmethod
	def exe_insert(self, query, params):
		pass

	@abstractmethod
	def exe_update(self, query, params):
		pass

	@abstractmethod
	def exe_select(self, query):
		pass

	@abstractmethod
	def exe_delete(self, query):
		pass
	