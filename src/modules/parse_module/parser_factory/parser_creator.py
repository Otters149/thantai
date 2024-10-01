from src.modules.parse_module.parser_factory.parser import Parser
from src.modules.parse_module.parser_factory.dsk_parser import DSKParser

class PaserCreator:
	def __init__(self) -> None:
		pass

	@classmethod
	def create_parser(self, syntax: str) -> Parser:
		self.parser = None
		if syntax == "DSK":
			self.parser = DSKParser()
		return self.parser