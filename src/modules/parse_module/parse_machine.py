from datetime import datetime
from src.enums import SIDE

from src.modules.parse_module.parser_factory.parser_creator import PaserCreator
from src.modules.parse_module.parser_factory.parser import Parser, PairInt
from src.modules.parse_module.parse_models.parse_config import ParseConfig
from src.modules.parse_module.parse_models.parse_message import ParseMessage
from src.logger import AppLogger
from preprocessor import IS_DEV_BUILD

def run_parse_machine(raw_message: str, parse_config: ParseConfig, date_check: datetime, side: SIDE) -> tuple[bool, str, list[ParseMessage], list[PairInt]]:
	'''
		Return:
			bool: success
			list[ParseMessage]: parse results
			list[PairInt]: error indexes collection
	'''
	if len(raw_message) == 0:
		return False, []
	
	parser_creator = PaserCreator()
	parser: Parser = parser_creator.create_parser(parse_config.syntax)
	if parser == None:
		return False, []
	
	success, message_standardized, parsed_message_results, parsed_message_checkpoints, error_checkpoints = parser.run(raw_message, parse_config, date_check, side)
	if success:
		__debug_parsed_message_collection("PARSING", parsed_message_results)
		success, parsed_message_results, error_checkpoints = parser.do_processing(parsed_message_results, parsed_message_checkpoints, parse_config, date_check, side)
		if success:
			__debug_parsed_message_collection("PROCESSING", parsed_message_results)
			return True, message_standardized, parsed_message_results, error_checkpoints
		else:
			AppLogger.e(f"[PARSE MACHINE] PROCESSING Error")
	else:
		AppLogger.e(f"[PARSE MACHINE] Raw Error")
	return False, message_standardized, parsed_message_results, error_checkpoints

def  __debug_parsed_message_collection(tag: str, messages: list[ParseMessage]):
	if IS_DEV_BUILD:
		AppLogger.d(f"=====================================================================")
		for msg in messages:
			AppLogger.d(f"[{tag}] {msg.to_bet_str()}")
		AppLogger.d(f"=====================================================================")