from datetime import datetime

from src.enums import SIDE, MONEY_UNIT
from src.logger import AppLogger
from src.modules.module_hepler import get_day_of_week, get_channel_code_by_date
from src.modules.parse_module.parse_helper import get_implicit_numbers_by_config, get_link_numbers_by_config, PairInt, ParseMessagePartIndexes, NUMBER_IGNORE, NUMBER_LINK_UNIT, NUMBER_LINK_CONTINUOUS, LINK_NUMBERS, IMPLICIT_NUMBER
from src.modules.parse_module.parse_models.parse_message import ParseMessage
from src.modules.parse_module.parse_models.parse_config import ParseConfig

#region Handle type bet
def __is_should_convert_channel_to_2d_for_daxien(side: SIDE, channels_code: list[str]) -> bool:
	return (side == SIDE.MID or side == SIDE.SOUTH) \
			and len(channels_code) == 1 \
			and ("2D" not in channels_code) \
			and ('3D' not in channels_code) \
			and ("4D" not in channels_code)

def __handle_type_bet(pre_parsed_message: ParseMessage, parsed_message: ParseMessage, next_parsed_message: ParseMessage, parse_config: ParseConfig, side: SIDE)\
	 					 -> tuple[bool, ParseMessage, ParseMessage]:
	'''
		Return:
			bool: success
			ParseMessage: parsed message after handle
			ParseMessage: next parsed message after handle
	'''
	if parsed_message.type_bet != "UNDETERMINED":
		if (parsed_message.type_bet == "DAXIEN" or parsed_message.type_bet == "DAXIENVONG") and __is_should_convert_channel_to_2d_for_daxien(side, parsed_message.channels_code):
			parsed_message.channels_code = ['2D']
		if  parsed_message.type_bet != "BAOLO7":
			parsed_message.type_bet = ''.join(c for c in parsed_message.type_bet if c.isalpha())	# DAOXIU2 -> DAOXIU,...
	else:
		if parsed_message.raw_typebet.lower() == "d":
			if next_parsed_message != None and (next_parsed_message.raw_typebet.lower() == "d" and next_parsed_message.raw_numbers == "") \
					and next_parsed_message.numbers == parsed_message.numbers and next_parsed_message.channels_code == parsed_message.channels_code:
				parsed_message.type_bet = "DAU"
				next_parsed_message.type_bet = "DUOI"
			else:
				parsed_message.type_bet = "DA"
		elif parsed_message.raw_typebet == "b":
			if parse_config.enable_b_equal_duoi or (pre_parsed_message != None and pre_parsed_message.raw_typebet == 'a'):
				parsed_message.type_bet = "DUOI"
			else:
				parsed_message.type_bet = "BAOLO"
		elif parsed_message.raw_typebet == "dx":
			has_two_digit = False
			has_more_than_two_digit = False
			for num in parsed_message.numbers:
				if len(num) == 2:
					has_two_digit = True
				else:
					has_more_than_two_digit = True
			
				if has_two_digit and has_more_than_two_digit:
					parsed_message.type_bet = "Kiểu đánh dx, số gồm 2 loại (loại có 2 chữ số và loại có 3 chữ số) => Không thể phân biệt là 'đá xiên' hay 'đảo xiu'. Vui lòng xem lại!"
					return False, parsed_message, next_parsed_message
				
			if has_two_digit:
				parsed_message.type_bet = "DAXIEN"
				if __is_should_convert_channel_to_2d_for_daxien(side, parsed_message.channels_code):
					parsed_message.channels_code = ['2D']
			else:
				parsed_message.type_bet = "DAOXIU"
	return True, parsed_message, next_parsed_message
#endregion Handle type bet

#region Handle money
def __handle_money(parsed_message: ParseMessage) -> tuple[bool, ParseMessage]:
	'''
		Return:
			bool: success
			ParseMessage: parsed message after handle
	'''
	parsed_message.point_bet = parsed_message.point_bet.replace(",", ".")
	if len(parsed_message.point_bet) >= 0 and parsed_message.point_bet[0] == '0' and '.' not in parsed_message.point_bet:
		parsed_message.point_bet = parsed_message.point_bet[:1] + "." + parsed_message.point_bet[1:]
	if parsed_message.point_bet_unit == MONEY_UNIT.TRIEU:
		parsed_message.point_bet_unit = MONEY_UNIT.NGHIN
		parsed_message.point_bet = str(int(float(parsed_message.point_bet) * 1000))
	if parsed_message.point_bet == "" or float(parsed_message.point_bet) == 0.0:
		parsed_message.point_bet = "Tin không có điểm cược"
		return False, parsed_message
	return True, parsed_message
#endregion Handle money

#region Handle channel
def __get_channel_code_by_index(channels_code_for_check: list[str], channels_order: int, index: int) -> str:
	if index == -1:
		order_at_index = int(str(channels_order)[index:])
	else:
		order_at_index = int(str(channels_order)[index: index+1])
	return channels_code_for_check[order_at_index - 1]

def __check_general_valid_and_append_channel_code(has_multi_channel_code: bool, in_channels_handled_collection: list[str], channels_code_for_append: list[str]) -> tuple[bool, list[str], bool]:
	'''
		Return:
			bool: success
			list[str]: list of channels has been handled
			bool: has_multi_channel_code
	'''
	channels_handled_collection = in_channels_handled_collection
	if has_multi_channel_code:
		return False, channels_handled_collection, has_multi_channel_code
	channels_handled_collection.extend(channels_code_for_append)
	return True, channels_handled_collection, len(channels_code_for_append) >= 2

def __handle_channel(in_parsed_messages: ParseMessage, parse_config: ParseConfig, date_check: datetime, side: SIDE) -> tuple[bool, ParseMessage]:
	'''
		Return:
			bool: success
			ParseMessage: parsed message after process
	'''
	parsed_messages = in_parsed_messages
	channels_order = 1
	if side == SIDE.SOUTH:
		channels_order = parse_config.south_channels_order[get_day_of_week(date_check)]
	elif side == SIDE.MID:
		channels_order = parse_config.mid_channels_order[get_day_of_week(date_check)]
	
	channels_code_for_check = get_channel_code_by_date(side, date_check)
	AppLogger.d(f"[__handle_channel] channels_code_for_check {channels_code_for_check} - channels_order {channels_order}")

	handled_channels = []
	explicit_channels_code = []
	is_mixed = 0
	has_multi_channel_code = False
	for channel in parsed_messages.channels_code:
		if channel == "3D" or channel == "4D":
			if len(str(channels_order)) == 2:
				channel = "2D"
			if len(str(channels_order)) == 3:
				channel = "3D"

		# Dev Note: 2 dai phu -> 2 dai + dai phu: That reason check has_multi_channel_code at DC & DP (No not allow syntax: 2dai dc dp...)
		success = True
		if channel == "DC":
			is_mixed |= 1
			success, handled_channels, has_multi_channel_code = __check_general_valid_and_append_channel_code(has_multi_channel_code, handled_channels, 
																			[__get_channel_code_by_index(channels_code_for_check, channels_order, 0)])
		elif channel == "DP":
			is_mixed |= 1
			success, handled_channels, has_multi_channel_code = __check_general_valid_and_append_channel_code(has_multi_channel_code, handled_channels, 
																			[__get_channel_code_by_index(channels_code_for_check, channels_order, 1)])
		elif channel == "DAI3":
			is_mixed |= 1
			success, handled_channels, has_multi_channel_code = __check_general_valid_and_append_channel_code(has_multi_channel_code, handled_channels, 
																			[__get_channel_code_by_index(channels_code_for_check, channels_order, 2)])
		elif channel == "DAI4":
			is_mixed |= 1
			success, handled_channels, has_multi_channel_code = __check_general_valid_and_append_channel_code(has_multi_channel_code, handled_channels, 
																			[__get_channel_code_by_index(channels_code_for_check, channels_order, 3)])
		elif channel == "2D":
			is_mixed |= 1
			success, handled_channels, has_multi_channel_code = __check_general_valid_and_append_channel_code(has_multi_channel_code, handled_channels, 
																			[__get_channel_code_by_index(channels_code_for_check, channels_order, 0),
																			 __get_channel_code_by_index(channels_code_for_check, channels_order, 1)])
		elif channel == "3D":
			is_mixed |= 1
			success, handled_channels, has_multi_channel_code = __check_general_valid_and_append_channel_code(has_multi_channel_code, handled_channels, 
																			[__get_channel_code_by_index(channels_code_for_check, channels_order, 0),
																			 __get_channel_code_by_index(channels_code_for_check, channels_order, 1),
																			 __get_channel_code_by_index(channels_code_for_check, channels_order, 2)])
		elif channel == "4D":
			is_mixed |= 1
			success, handled_channels, has_multi_channel_code = __check_general_valid_and_append_channel_code(has_multi_channel_code, handled_channels, 
																			[__get_channel_code_by_index(channels_code_for_check, channels_order, 0),
																			 __get_channel_code_by_index(channels_code_for_check, channels_order, 1),
																			 __get_channel_code_by_index(channels_code_for_check, channels_order, 2),
																			 __get_channel_code_by_index(channels_code_for_check, channels_order, 3)])
		elif channel == "2DP":
			is_mixed |= 1
			success, handled_channels, has_multi_channel_code = __check_general_valid_and_append_channel_code(has_multi_channel_code, handled_channels, 
																			[__get_channel_code_by_index(channels_code_for_check, channels_order, -2),
																			 __get_channel_code_by_index(channels_code_for_check, channels_order, -1)])
		else:
			is_mixed |= (1 << 1)
			handled_channels.append(channel)
			explicit_channels_code.append(channel)

		if not success:
			return False, handled_channels
	handled_channels = list(set(handled_channels))
	if is_mixed == 0b011: # Handle mix case channel: cmau, ctho 2dai; 2dai tph, long an; mt lamdong dongnai,...
		parsed_messages.channels_code = explicit_channels_code
		return True, parsed_messages
	parsed_messages.channels_code = handled_channels
	return True, parsed_messages
#endregion Handle money

#region Handle number
def __get_implicit_link_numbers_by_config(implicit_number: str, connect_to_number: str) -> tuple[bool, list[str]]:
	if len(connect_to_number) == 0: return False, []
	for config in LINK_NUMBERS:
		for suffix in range(10):
			if config.name + str(suffix) == implicit_number:
				results = []
				for connect_suffix in range(suffix, int(connect_to_number) + 1):
					results.extend(get_link_numbers_by_config(config, connect_suffix))
				return True, results
	return False, []

def __get_unit_linking_numbers(from_number: str, to_number: str) -> tuple[bool, list[str]]:
	'''
		Unit linking mean: 10 keo vi 90 = 10, 20, 30, 40, 50, 60, 70, 80, 90
		Return:
			bool: success
			list[str]: list of numbers
	'''
	if len(from_number) != len(to_number): return False, []
	if len(from_number) != 2 or len(to_number) != 2 or from_number[1] != to_number [1] or  from_number[0] >= to_number[0]: return False, []

	return True, [f"{i}{from_number[1]}" for i in range(int(from_number[0]), int(to_number[0]) + 1)]

def __get_continuous_linking_numbers(from_number: str, to_number: str) -> tuple[bool, list[str]]:
	'''
		Return:
			bool: success
			list[str]: list of numbers
	'''
	# Internal Method
	def __get_continuous_linking_numbers_at_diff(from_number: str, to_number: str, diff_index: int) -> list[str]:
		numbers = []
		temp_number = from_number
		for i in range(int(from_number[diff_index]), int(to_number[diff_index]) + 1):
			temp_number = temp_number[:diff_index] + f'{i}' + temp_number[diff_index + 1:]
			numbers.append(temp_number)
		return numbers
	#=================
	
	if from_number.isdigit():
		if len(from_number) != len(to_number): return False, []
		if int(from_number) >= int(to_number): return False, []
		if len(from_number) == 2:
			if from_number == "00" and to_number == "99":
				return True, get_implicit_numbers_by_config(IMPLICIT_NUMBER.CAP)
			elif from_number[0] == "0" and to_number[0] == "9" and from_number[1] == to_number[1]: # unit linking
				return __get_unit_linking_numbers(from_number, to_number)
			else:
				return True, ["{0:02}".format(i) for i in range(int(from_number), int(to_number) + 1)]
		elif len(from_number) == 3 or len(from_number) == 4:
			if from_number == "000" and to_number  == "999":
				return True, [f"{i}{i}{i}".format(i) for i in range(10)]
			elif from_number == "0000" and to_number == "9999":
				return True, [f"{i}{i}{i}{i}".format(i) for i in range(10)]
			else:
				success, diff_index = __get_diff_number_index_between_two_numbers(from_number, to_number)
				if not success: return False, []
				return True, __get_continuous_linking_numbers_at_diff(from_number, to_number, diff_index)
		else:
			return False, []
	else:
		to_number = "".join([n for n in to_number if n.isdigit()])
		return __get_implicit_link_numbers_by_config(from_number, to_number)

def __get_diff_number_index_between_two_numbers(first_number: str, second_number) -> tuple[bool, int]:
	'''
		Return:
			bool: success
			int: index of diff
	'''
	diff_index = -1
	for index in range(len(first_number)):
		if first_number[index] != second_number[index]:
			if diff_index == -1:
				diff_index = index
			else:
				return False, diff_index
	return diff_index >= 0, diff_index

def __get_link_numbers(in_linking_numbers: list[str], connect_to_number: str, is_unit_linking: bool) -> tuple[bool, list[str]]:
	linking_numbers = in_linking_numbers
	last_number = linking_numbers[-1]
	linking_numbers = linking_numbers[:len(linking_numbers) - 1]

	if is_unit_linking:
		success, numbers = __get_unit_linking_numbers(last_number, connect_to_number)
	else:
		success, numbers = __get_continuous_linking_numbers(last_number, connect_to_number)
	return success, numbers

def __convert_implicit_number_to_explicit_number(numbers: list[str]) -> list[str]:
	numbers_converted = []
	for number in numbers:
		is_implicit = False
		for config in IMPLICIT_NUMBER:
			if config.name == number:
				is_implicit = True
				numbers_converted.extend(get_implicit_numbers_by_config(config))
				break
		if not is_implicit:
			for config in LINK_NUMBERS:
				for suffix in range(10):
					if config.name + str(suffix) == number:
						is_implicit = True
						numbers_converted.extend(get_link_numbers_by_config(config, suffix))
						break
					if is_implicit:
						break
			if not is_implicit:
				numbers_converted.append(number)
	return numbers_converted

def __handle_number(in_parsed_messages: ParseMessage) -> tuple[bool, ParseMessage]:
	'''
		Return:
			bool: success
			ParseMessage: parsed message after handle
	'''
	parsed_messages = in_parsed_messages
	numbers = parsed_messages.numbers
	ignores = []
	linked_numbers = []

	is_ignore_phrase = False
	has_unit_linking = False
	has_continuous_linking = False
	for index in range(len(numbers)):
		if numbers[index] in NUMBER_IGNORE:
			is_ignore_phrase = True
			# Specials
			if numbers[index] == "bchuc":
				ignores.append(get_implicit_numbers_by_config(IMPLICIT_NUMBER.CHUC))
			elif numbers[index] == "bcap":
				ignores.append(get_implicit_numbers_by_config(IMPLICIT_NUMBER.CAP))
		elif numbers[index] in NUMBER_LINK_UNIT:
			has_unit_linking = True
		elif numbers[index] in NUMBER_LINK_CONTINUOUS:
			has_continuous_linking = True
		else:
			if is_ignore_phrase:
				if has_unit_linking or has_continuous_linking:
					success, link_numbers = __get_link_numbers(ignores, numbers[index], has_unit_linking)
					if not success: return False, parsed_messages
					ignores = link_numbers
				else:
					ignores.append(numbers[index])
			else:
				if has_unit_linking or has_continuous_linking:
					success, link_numbers = __get_link_numbers(linked_numbers, numbers[index], has_unit_linking)
					if not success: return False, parsed_messages
					linked_numbers = link_numbers
				else:
					linked_numbers.append(numbers[index])
			has_unit_linking = False
			has_continuous_linking = False
	if has_unit_linking or has_continuous_linking:
		return False, parsed_messages # It is linking bet message without second number
	
	linked_numbers = __convert_implicit_number_to_explicit_number(linked_numbers)
	ignores = __convert_implicit_number_to_explicit_number(ignores)
	parsed_messages.numbers = [element for element in linked_numbers if element not in ignores]
	return True, parsed_messages
#endregion Handle money

def basic_processing(in_parsed_messages: list[ParseMessage], parsed_checkpoint: list[ParseMessagePartIndexes], parse_config: ParseConfig, date_check: datetime, side: SIDE) \
					-> tuple[bool, list[ParseMessage], list[PairInt]]:
	'''
		Uses: 
			Correct channels: dc, dp, 2dai,...
			Connect numbers: h123, 12k24,...
			Normalize type: DAOXIU2 -> DAOXIU
			Correct money: 0,5 -> 0.5
		Return:
			bool: success
			list[Message]: parsed messages after handle
			list[PairInt]: indexes of error part
	'''
	#========================
	def __handle_process_error(in_error_checkpoint: list[PairInt], origin_parse_message: ParseMessage, error_pair_index: PairInt):
		internal_error_checkpoint = in_error_checkpoint
		internal_error_checkpoint.append(error_pair_index)
		return True, origin_parse_message, internal_error_checkpoint
	#========================

	parsed_messages = in_parsed_messages
	error_checkpoint: list[PairInt] = []

	for index in range(len(parsed_messages)):
		current_message = parsed_messages[index]
		pre_message = None
		next_message = None
		if index > 0:
			pre_message = parsed_messages[index - 1]
		if index < len(parsed_messages) - 1:
			next_message = parsed_messages[index + 1]

		has_error = False
		success, current_message, next_message = __handle_type_bet(pre_message, current_message, next_message, parse_config, side)
		if not success:
			has_error, current_message, error_checkpoint = __handle_process_error(error_checkpoint, parsed_messages[index], parsed_checkpoint[index].type_bet_pair_index)
			parsed_messages[index].is_failed_message = True

		success, current_message = __handle_money(current_message)
		if not success:
			has_error, current_message, error_checkpoint = __handle_process_error(error_checkpoint, parsed_messages[index], parsed_checkpoint[index].point_bet_pair_index)
			parsed_messages[index].is_failed_message = True

		success, current_message = __handle_channel(current_message, parse_config, date_check, side)
		if not success:
			has_error, current_message, error_checkpoint = __handle_process_error(error_checkpoint, parsed_messages[index], parsed_checkpoint[index].channel_pair_index)
			parsed_messages[index].is_failed_message = True

		success, current_message = __handle_number(current_message)
		if not success:
			has_error, current_message, error_checkpoint = __handle_process_error(error_checkpoint, parsed_messages[index], parsed_checkpoint[index].number_pair_index)
			parsed_messages[index].is_failed_message = True

		if not has_error:
			parsed_messages[index] = current_message
			if next_message != None:
				parsed_messages[index + 1] = next_message

	return len(error_checkpoint) == 0, parsed_messages, error_checkpoint