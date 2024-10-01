import os, sys
sys.path.insert(1, "/".join(os.path.realpath(__file__).split("/")[0:-2]))

from datetime import datetime

from src.modules.parse_module.parse_models.parse_config import ParseConfig
from src.modules.parse_module.parse_models.parse_message import ParseMessage
from src.modules.parse_module.parse_machine import run_parse_machine
from src.modules.calculate_module.calculator_models.calculate_config import CalculateConfig
from src.modules.calculate_module.calculator_models.calculate_result import CalculateResult
from src.modules.calculate_module.calculator_machine import run_calculator_machine
from src.enums import SIDE

def main():
	parse_config: ParseConfig = ParseConfig("DSK")
	calc_config: CalculateConfig = CalculateConfig(
		[75.5, 75.3, 75.3, 75.3, 66, 66, 66, 66, 66, 66, 75.5, 75.3], 
		[75, 75.3, 75.3, 75.3, 650, 650, 650, 650, 6000, 6000, 750, 570],
		False)
	side = SIDE.NORTH
	date_check = datetime(year=2024, month=9, day=29)
	msg_input = '''2đ 15,22,86 dau 10n'''
	success, message_standardized, results, errors_index = run_parse_machine(msg_input, parse_config, date_check, side)
	if not success:
		for e_index in errors_index:
			print(message_standardized[e_index.first: e_index.second])
		for msg in results:
			print(f"[TESTING] {msg.to_bet_str()}")
	else:
		success, calc_results = run_calculator_machine(results, calc_config, date_check, side, False, False)
		if success:
			for rs in calc_results:
				print(f"[TESTING] {rs.to_readable_str()}")
if __name__ == '__main__':
	main()