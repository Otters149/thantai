from abc import ABC, abstractmethod
from datetime import datetime

###
from src.utils import str_remove_accents
from src.modules.parse_module.parser_factory.processors.basic_processor import basic_processing
from src.modules.parse_module.parser_factory.processors.advance_processor import advance_processing
from src.modules.parse_module.parse_models.parse_config import ParseConfig
from src.modules.parse_module.parse_models.parse_message import ParseMessage
from src.enums import SIDE, MONEY_UNIT
from src.modules.parse_module.parse_helper import PairInt, ParseMessagePartIndexes, CHILD_ORDER, CHANNELS, IMPLICIT_NUMBERS, TYPES_BET, MONEY_UNITS, NUMBER_LINK_UNIT, NUMBER_LINK_CONTINUOUS, NUMBER_IGNORE, LINK_NUMBERS

class Parser(ABC):
#region Abstract methods
	@abstractmethod
	def run(self, input: str, parse_config: ParseConfig, date_check: datetime, side: SIDE) -> tuple[bool, str, list[ParseMessage], list[ParseMessagePartIndexes], list[PairInt]]:
		'''
			Return:
				bool: success
				str: message after standardized
				list[ParseMessage]: list of message model has been parsed from raw input
				list[ParseMessagePartIndexes]: index of message in raw input string
				list[Parser.PairInt]: indexes of error part
		'''
#endregion

#rerion Public methods
	def do_processing(self, parsed_messages: list[ParseMessage], parsed_checkpoint: list[ParseMessagePartIndexes], parse_config: ParseConfig, date_check: datetime, side: SIDE)\
							-> tuple[bool, list[ParseMessage], list[PairInt]]:
		basic_success, parsed_message_results, basic_error_checkpoints = basic_processing(parsed_messages, parsed_checkpoint, parse_config, date_check, side)
		advance_success, parsed_message_results, advance_error_checkpoints = advance_processing(parsed_messages, parsed_checkpoint, parse_config, side)
		final_error_checkpoint = []
		final_error_checkpoint.extend(basic_error_checkpoints)
		final_error_checkpoint.extend(advance_error_checkpoints)
		return basic_success and advance_success, parsed_message_results, final_error_checkpoint

#endregion

#region Standardization
	def __standardization_ignore_diffusion_dot_and_comma(self, input: str) -> str:
		output = ""
		for index in range(len(input)):
			if input[index] == '.' or input[index] == ',':
				if index == 0 or index == len(input) - 1 or input[index + 1] == ' ':
					continue
				elif not (input[index - 1].isdigit() and input[index + 1].isdigit()):
					output += ' '
					continue
			output += input[index]
		return output

	def __standardization_remove_special_char(self, input: str) -> str:
		remove_template = [ "mien trung", "m trung", "mientrung", "mtrung", "mtr", "mt",
							"mien nam", "m nam", "miennam", "mnam", "mn",
					 		"\xa0", "'", '"', "vs", "@", "!", "~", "\\", "$", "^", "%", "#", "&", "*", "|", ";", ":", "    ", "   ", "  "]
		output = input
		for template in remove_template:
			output = output.replace(template, " ")
		return output

	def __standardization_strip_newline(self, input: str) -> str:
		output = input.strip('\n')
		return output.replace('\n\n', '\n')
	
	def _standardization(self, input: str) -> str:
		output = str_remove_accents(input)
		output = output.lower()
		output = self.__standardization_strip_newline(output)
		output = self.__standardization_ignore_diffusion_dot_and_comma(output)
		output = self.__standardization_remove_special_char(output)
		return output
#endregion

#region Parse logic
	def _skip_whitespace_dot_and_comma(self, msg: str) -> str:
		while len(msg) > 0:
			if not ('a' <= msg[0] <= 'z' or 'A' <= msg[0] <= 'Z' or '0' <= msg[0] <= '9'):
				msg = msg[1:]
			else:
				return msg
		return msg

	def _skip_north_side_channel(self, msg: str, channels_code: list[str]) -> str:
		found = True
		while len(msg) > 0 and found:
			found = False
			for key in channels_code:
				for ar in CHANNELS[SIDE.NORTH][key]:
					if msg.find(ar, 0, len(ar)) >= 0:
						found = True
						msg =  msg.replace(ar, "", 1).strip()
						msg = self._skip_whitespace_dot_and_comma(msg)
						break
		return msg


	def _parse_order(self, msg: str, ceiling: int = 100) -> tuple[bool, str, int, str]:
		'''
			Return:
				bool: success
				str: msg after cut off
				int: order of child msg
				str: raw order string
		'''
		if msg.find('t', 0, 1) >= 0 or msg.find('tin', 0, 3) >= 0:
			for current in range(ceiling, 0, -1):
				for t in CHILD_ORDER:
					temp = t.replace('@', str(current))
					if msg.find(temp, 0, len(temp)) >= 0:
						return True,  msg.replace(temp, "", 1).strip(), current, temp
			return False, msg.strip(), 1, ""
		else:
			return False, msg.strip(), 1, ""


	def _parse_channel(self, msg: str, channels_code: list[str], side: SIDE) -> tuple[bool, str, list[str], str]:
		'''
			Return:
				bool: success
				str: msg after cut off
				list[str]: channels code matched
				str: raw channels
		'''
		result: list[str] = []
		success = True
		raw_channels = ""

		while len(msg) > 0:
			found = False
			for key in channels_code:
				channels_config = CHANNELS[side][key]
				for config in channels_config:
					if msg.find(config, 0, len(config)) >= 0:
						# TODO: Recheck 
						# This condition check for channel da lat [dl] overlap with type dao lo [dl] (also for binh duong[db] vs bao dao [bd]) 
						if len(config) < len(msg) and msg[len(config)].isalpha(): # if next char is digit that mean => channel dl or bd is incorrect
							continue
						found = True
						result.append(key)
						if raw_channels == "":
							raw_channels += config
						else:
							raw_channels += ", " + config
						msg =  msg.replace(config, "", 1).strip()
						msg = self._skip_whitespace_dot_and_comma(msg)
						break
			if not found:
				break
		if len(result) == 0:
			success = False
		return success, msg, result, raw_channels


	def _parse_type_bet(self, msg: str) -> tuple[bool, str, str, str]:
		'''
			Return:
				bool: success
				str: message after cut off
				str: type-bet key code
				str: type-bet raw string
		'''
		for key in TYPES_BET:
			for config in TYPES_BET[key]:
				if msg.find(config, 0 , len(config)) >= 0:
					return True, msg.replace(config, "", 1), key, config
		return False, msg, "", ""


	def __check_currency_overlap_channel(self, msg: str, unit: MONEY_UNIT, compare_set: dict[str, str]) -> tuple[str, MONEY_UNIT]:
		'''
			Return: 
				str: msg after cut off
				MONEY_UNIT: money unit
		'''
		for currency in MONEY_UNITS[unit]:
			if msg.find(currency, 0, len(currency)) >= 0:
				compare_flag = False
				if len(msg) > len(currency):
					for pair in compare_set:
						if currency == pair[0] and msg[len(currency)] in pair[1]:
							compare_flag = True
							break

				if len(currency) != len(msg) and compare_flag:
					continue

				msg = msg.replace(currency, "", 1)
				return msg, unit
		return msg, MONEY_UNIT.NONE

	def _parse_point_bet(self, msg: str, syntax: str) -> tuple[bool, str, str, MONEY_UNIT]:
		'''
			Return:
				bool: success
				str: msg after cut off
				str: money
				MONEY_UNIT: money unit
		'''
		money = ""
		currency_unit = MONEY_UNIT.NONE
		while len(msg) > 0:
			added = False
			if '0' <= msg[0] <= '9':
				added = True
				money += msg[0]
				msg = msg[1:]
			elif msg[0] == ',' or msg[0] == '.':
				if len(msg) == 2:
					added = True
					money += msg[0]
				elif len(msg) == 3:
					if (msg[1] == "2" or msg[1] == "3" or msg[1] == "4"):   # KSD: Case channel in the end
						if msg[2] == "d" and syntax[-1] == "D":	
							pass
						else:
							added = True
							money += msg[0]   
					else:
						added = True
						money += msg[0]   
				elif len(msg) > 3 and msg[1].isdigit() and not msg[2].isdigit():
					if (msg[1] == "2" or msg[1] == "3" or msg[1] == "4"):   # money.2dai/3dai/4dai -> throw error
						if msg.find("dai", 2, 5) >= 0:
							pass
						elif msg[2] == "d":
							if msg[3].isalpha():
								added = True
								money += msg[0]
							else:
								return False, msg, "" , currency_unit
						else:
							added = True
							money += msg[0]
					else:
						added = True
						money += msg[0]
				msg = msg[1:]

			if not added:
				msg = self._skip_whitespace_dot_and_comma(msg)

				#[Special] Avoid case currency "m" vs channel "mb" and case current "ng" vs number "nguoc giap" and case "n" vs channel "nt"
				compare_set = [
					["m", "bt"],
					["ng", "u"],
					["n", "ti"],
				]
				msg, currency_unit = self.__check_currency_overlap_channel(msg, MONEY_UNIT.NGHIN, compare_set)

				if currency_unit == MONEY_UNIT.NONE:
					#[Special] Avoid case currency "tr" vs channel "travinh | trvinh"
					compare_set = [
						["tr", "av"]
					]
					msg, currency_unit = self.__check_currency_overlap_channel(msg, MONEY_UNIT.TRIEU, compare_set)

					if currency_unit == MONEY_UNIT.NONE:
						currency_unit = MONEY_UNIT.NGHIN
				break

		if money != "":
			if currency_unit == MONEY_UNIT.NONE and len(msg) == 0:
				currency_unit = MONEY_UNIT.NGHIN
			return True, msg, money, currency_unit
		return False, msg, "", currency_unit


	def __check_number_match_special_config(self, msg: str, configs: list[str]) -> tuple[bool, str, str]:
		'''
			Return:
				bool: success
				str: message after cut off
				str: config matched
		'''
		for config in configs:
			if msg.find(config, 0, len(config)) >= 0:
				msg = msg.replace(config, "", 1).strip()
				return True, msg, config
		return False, msg, ""
	
	def __append_number_to_list_parsed_numbers(self, number_to_add: str, origin_numbers_list: list[str]) -> tuple[str, list[str]]:
		'''
			Return:
				str: reset number_to_add if addable
				list[str]: list numbers after added
		'''
		if number_to_add != "":
			origin_numbers_list.append(number_to_add)
			number_to_add = ""
		return number_to_add, origin_numbers_list

	def _parse_number(self, msg: str) -> tuple[bool, str, list[str], str]:
		'''
			Return:
				bool: success
				str: message after cut off
				list[str]: list of numbers
				str: raw number string
		'''
		numbers = []
		num = ""
		raw_numbers = ""
		while len(msg) > 0:
			raw_numbers += msg[0]
			if '0' <= msg[0] <= '9':
				num += msg[0]
				msg = msg[1:]
			elif 'a' <= msg[0] <= 'z':
				flag_check_link_number, msg, link_unit_config = self.__check_number_match_special_config(msg, NUMBER_LINK_UNIT)
				if flag_check_link_number:
					num, numbers = self.__append_number_to_list_parsed_numbers(num, numbers)
					numbers.append(link_unit_config)
				else:
					flag_check_link_number, msg, link_continuous_config = self.__check_number_match_special_config(msg, NUMBER_LINK_CONTINUOUS)
					if flag_check_link_number:
						num, numbers = self.__append_number_to_list_parsed_numbers(num, numbers)
						numbers.append(link_continuous_config)
					else:
						flag_check_link_number, msg, ignore_config = self.__check_number_match_special_config(msg, NUMBER_IGNORE)
						if flag_check_link_number:
							num, numbers = self.__append_number_to_list_parsed_numbers(num, numbers)
							numbers.append(ignore_config)
						else:
							for implicit_number_key in IMPLICIT_NUMBERS:
								temp_flag_check_link_number, msg, link_continuous_config = self.__check_number_match_special_config(msg, IMPLICIT_NUMBERS[implicit_number_key])
								if temp_flag_check_link_number:
									num, numbers = self.__append_number_to_list_parsed_numbers(num, numbers)
									numbers.append(implicit_number_key.name)
									flag_check_link_number = True

							if not flag_check_link_number:
								# Check link number
								template_matched = False
								for link_number_key in LINK_NUMBERS:
									for link_number_config in LINK_NUMBERS[link_number_key]:
										for index in range(10):
											temp = link_number_config.replace("@", str(index))
											if msg.find(temp, 0, len(temp)) >= 0:
												msg = msg.replace(temp, "", 1)
												num, numbers = self.__append_number_to_list_parsed_numbers(num, numbers)
												numbers.append(link_number_key.name + str(index))
												flag_check_link_number = True
												template_matched = True
												break
										if flag_check_link_number:
											break
									if flag_check_link_number:
										break

								if template_matched:
									multi_link_check_found = False
									# Check: hang1234..., donvi1234...
									while len(msg) > 0 and msg[0].isdigit():
										multi_link_check_found = True
										numbers.append(link_number_key + str(index))
										msg = msg[1:]
									# Check: hang1,2,3,4,..., donvi1,2,3,4,...
									if not multi_link_check_found:
										while len(msg) > 0:
											msg = self._skip_whitespace_dot_and_comma(msg)
											num = ""
											while len(msg) > 0 and msg[0].isdigit():
												num += msg[0]
												msg = msg[1:]
											if len(num) == 1:
												numbers.append(link_number_key + num)
											else:
												num, numbers = self.__append_number_to_list_parsed_numbers(num, numbers)
												break
											
							if not flag_check_link_number:
								num, numbers = self.__append_number_to_list_parsed_numbers(num, numbers)
								break
			else:
				if num != "":
					numbers.append(num)
					# This is floating point of money
					if (msg[0] == '.' or  msg[0] ==',') and (len(msg) == len(num) + 2 or not msg[1].isdigit()):	# len(num) + 2 mean: len of "{num}.x"
						return len(numbers) > 0 , msg, numbers, raw_numbers
					num = ""
				msg = msg[1:]
		return len(numbers) > 0, msg, numbers, raw_numbers
#endregion