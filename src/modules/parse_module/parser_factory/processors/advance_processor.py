from datetime import datetime

from src.enums import SIDE
from src.modules.parse_module.parse_helper import PairInt, ParseMessagePartIndexes
from src.modules.parse_module.parse_models.parse_message import ParseMessage
from src.modules.parse_module.parse_models.parse_config import ParseConfig

def __handle_dauduoi_3digit(in_parsed_message: ParseMessage, numbers_track: list[str], parse_config: ParseConfig)\
							-> tuple[bool, ParseMessage]:
	'''
		Return:
			bool: success
			ParseMessage: message after handle
	'''
	new_msg = in_parsed_message.clone()
	new_msg.numbers = numbers_track.copy()
	for number in numbers_track:
		if len(number) != 3:
			new_msg.numbers = f"Cách đánh xỉu phải có 3 chữ số: {numbers_track}" 
			return False, new_msg
	if parse_config.allow_duoi_3c_4c:
		if in_parsed_message.type_bet == "DAUDUOI":
			new_msg.type_bet = "XIUCHU"
		else:
			new_msg.type_bet = "X" + new_msg.type_bet
	else:
		for i in range(len(new_msg.numbers)):
			new_msg.numbers[i] = new_msg.numbers[i][-2:]
	
	return True, new_msg

def __handle_dauduoi_4digit(in_parsed_message: ParseMessage, numbers_track: list[str], parse_config: ParseConfig)\
							-> tuple[bool, list[ParseMessage]]:
	'''
		Return:
			bool: success
			list[ParseMessage]: list of messages seperated
	'''
	new_msg = in_parsed_message.clone()
	new_msg.numbers = numbers_track.copy()
	for number in numbers_track:
		if len(number) != 4:
			return False, new_msg
	if new_msg.type_bet == "DAU" or new_msg.type_bet == "DAUDUOI":
		if parse_config.allow_duoi_3c_4c:
			for i in range(len(numbers_track)):
				new_msg.numbers[i] = new_msg.numbers[i][-2:]
		else:
			new_msg.numbers = f"Cách đánh đầu không thể có 4 chữ số: {new_msg.numbers}"
			return False, new_msg
	return True, new_msg

def __append_message_with_new_numbers(in_parsed_message: ParseMessage, new_numbers: list[str], in_origin_parsed_message_group: list[ParseMessage]) -> list[ParseMessage]:
	new_msg = in_parsed_message.clone()
	new_msg.numbers = new_numbers.copy()
	return in_origin_parsed_message_group.copy().append(new_msg)

def __is_number_valid(numbers: list[str]) -> bool:
	for number in numbers:
		if len(number) < 2 or len(number) > 4:
			return False
	return True

def __handle_dauduoi(in_parsed_messages: list[ParseMessage], in_parsed_checkpoint: list[ParseMessagePartIndexes], in_errors: list[PairInt], parse_config: ParseConfig, index: int)\
					-> tuple[list[ParseMessage], list[ParseMessagePartIndexes], list[PairInt], int]:
	'''
		Return:
			list[ParseMessage]: new parsed messages list - after seperate messages
			list[ParseMessagePartIndexes]: new check point - after append index for seperated messages
			list[PairInt]: new error list - after append new errors if failed
			int: new index
	'''
	parsed_messages = in_parsed_messages.copy()
	errors = in_errors.copy()
	parsed_checkpoint = in_parsed_checkpoint.copy()
	numbers_track = [[], [], []]	# [2D, 3D, 4D]
	for num in parsed_messages[index].numbers:
		numbers_track[len(num) - 2].append(num)
	
	if len(numbers_track[0]) < len(parsed_messages[index].numbers) \
			and len(numbers_track[1]) < len(parsed_messages[index].numbers) \
			and len(numbers_track[2]) < len(parsed_messages[index].numbers):
		seperate_messages: list[ParseMessage] = []
		seperate_checkpoint: list[ParseMessagePartIndexes] = []
		if len(numbers_track[0]) > 0:
			new_msg = parsed_messages[index].clone()
			new_msg.numbers = numbers_track[0]
			seperate_messages.append(new_msg)
			seperate_checkpoint.append(parsed_checkpoint[index])
		if len(numbers_track[1]) > 0:
			success, new_msg = __handle_dauduoi_3digit(parsed_messages[index], numbers_track[1], parse_config)
			seperate_messages.append(new_msg)
			seperate_checkpoint.append(parsed_checkpoint[index])
			if not success:
				parsed_messages[index].is_failed_message = True
				errors.append(parsed_checkpoint[index].number_pair_index)
		if len(numbers_track[2]) > 0:
			success, new_msg = __handle_dauduoi_4digit(parsed_messages[index], numbers_track[2], parse_config)
			seperate_messages.append(new_msg)
			seperate_checkpoint.append(parsed_checkpoint[index])
			if not success:
				parsed_messages[index].is_failed_message = True
				errors.append(parsed_checkpoint[index].number_pair_index)			

		parsed_messages = parsed_messages[:index] + seperate_messages + parsed_messages[index + 1:]
		parsed_checkpoint = parsed_checkpoint[:index] + seperate_checkpoint + parsed_checkpoint[index + 1:]
		index += len(seperate_messages)
	elif len(numbers_track[1]) == len(parsed_messages[index].numbers):
		success, new_msg = __handle_dauduoi_3digit(parsed_messages[index], numbers_track[1], parse_config)
		parsed_messages[index] = new_msg
		if not success:
			parsed_messages[index].is_failed_message = True
			errors.append(parsed_checkpoint[index].number_pair_index)		
	elif len(numbers_track[2]) == len(parsed_messages[index].numbers):
		success, new_msg = __handle_dauduoi_4digit(parsed_messages[index], numbers_track[2], parse_config)
		parsed_messages[index] = new_msg
		if not success:
			parsed_messages[index].is_failed_message = True
			errors.append(parsed_checkpoint[index].number_pair_index)

	return parsed_messages, parsed_checkpoint, errors, index

def __handle_bao(in_parsed_messages: list[ParseMessage], in_parsed_checkpoint: list[ParseMessagePartIndexes], in_errors: list[PairInt], parse_config: ParseConfig, index: int)\
				-> tuple[list[ParseMessage], list[ParseMessagePartIndexes], list[PairInt], int]:
	'''
		Return:
			list[ParseMessage]: new parsed messages list - after seperate messages
			list[ParseMessagePartIndexes]: new check point - after append index for seperated messages
			list[PairInt]: new error list - after append new errors if failed
			int: new index
	'''
	parsed_messages = in_parsed_messages.copy()
	errors = in_errors.copy()
	parsed_checkpoint = in_parsed_checkpoint.copy()
	numbers_track = [[], [], []]	# [2D, 3D, 4D]
	for num in parsed_messages[index].numbers:
		numbers_track[len(num) - 2].append(num)

	if len(numbers_track[0]) < len(parsed_messages[index].numbers) \
			and len(numbers_track[1]) < len(parsed_messages[index].numbers) \
			and len(numbers_track[2]) < len(parsed_messages[index].numbers):
		seperate_messages: list[ParseMessage] = []
		seperate_checkpoint: list[ParseMessagePartIndexes] = []
		if len(numbers_track[0]) > 0:
			seperate_messages = __append_message_with_new_numbers(parsed_messages[index], numbers_track[0], seperate_messages)
			seperate_checkpoint.append(parsed_checkpoint[index])
		if len(numbers_track[1]) > 0:
			seperate_messages = __append_message_with_new_numbers(parsed_messages[index], numbers_track[1], seperate_messages)
			seperate_checkpoint.append(parsed_checkpoint[index])
		if len(numbers_track[2]) > 0:
			seperate_messages = __append_message_with_new_numbers(parsed_messages[index], numbers_track[2], seperate_messages)
			seperate_checkpoint.append(parsed_checkpoint[index])
		parsed_messages = parsed_messages[:index] + seperate_messages + parsed_messages[index + 1:]
		parsed_checkpoint = parsed_checkpoint[:index] + seperate_checkpoint + parsed_checkpoint[index + 1:]
		index += len(seperate_messages)
	if len(numbers_track[0]) > 0:
		if parsed_messages[index].type_bet == "BAODAO":
			parsed_messages[index].numbers =  f"Số có 2 chữ số không thể đánh đảo: {parsed_messages[index].numbers}"
			parsed_messages[index].is_failed_message = True
			errors.append(parsed_checkpoint[index].number_pair_index)
	
	return parsed_messages, parsed_checkpoint, errors, index

def __handle_da(in_parsed_messages: list[ParseMessage], in_parsed_checkpoint: list[ParseMessagePartIndexes], in_errors: list[PairInt], parse_config: ParseConfig, index: int, side: SIDE)\
				-> tuple[list[ParseMessage], list[ParseMessagePartIndexes], list[PairInt], int]:
	'''
		Return:
			list[ParseMessage]: new parsed messages list - after seperate messages
			list[ParseMessagePartIndexes]: new check point - after append index for seperated messages
			list[PairInt]: new error list - after append new errors if failed
			int: new index
	'''
	parsed_messages = in_parsed_messages.copy()
	errors = in_errors.copy()
	parsed_checkpoint = in_parsed_checkpoint.copy()
	if parsed_messages[index].type_bet == "DA" or parsed_messages[index].type_bet == "DAVONG":
		if len(parsed_messages[index].channels_code) == 1:
			parsed_messages[index].type_bet = "DATHANG" if parsed_messages[index].type_bet == "DA" else "DATHANGVONG"
		else:
			parsed_messages[index].type_bet = "DAXIEN" if parsed_messages[index].type_bet == "DA" else "DAXIENVONG"
	
	# Addition check for north side
	if side == SIDE.NORTH:
		if parsed_messages[index].type_bet == "DAXIEN":
			parsed_messages[index].type_bet = "DATHANG"
		elif parsed_messages[index].type_bet == "DAXIENVONG":
			parsed_messages[index].type_bet = "DATHANGVONG"
	
	if not parse_config.enable_da_trung:
		parsed_messages[index].numbers = list(set(parsed_messages[index].numbers))

	if len(parsed_messages[index].numbers) < 2:
		parsed_messages[index].numbers = f"Số đá bắt buộc ít nhất 1 cặp số: {parsed_messages[index].numbers}"
		parsed_messages[index].is_failed_message = True
		errors.append(parsed_checkpoint[index].number_pair_index)

	if "VONG" not in parsed_messages[index].type_bet and parse_config.enable_da_cap:
		if len(parsed_messages[index].numbers) % 2 == 0:
			seperate_messages: list[ParseMessage] = []
			seperate_checkpoint: list[ParseMessagePartIndexes] = []
			for num_index in range(0, len(parsed_messages[index].numbers), 2):
				new_msg = parsed_messages[index].clone()
				new_msg.numbers = new_msg.numbers[num_index, num_index + 2]
				seperate_messages.append(new_msg)
				seperate_checkpoint.append(parsed_checkpoint[index])		
			parsed_messages = parsed_messages[:index] + seperate_messages + parsed_messages[index + 1:]
			parsed_checkpoint = parsed_checkpoint[:index] + seperate_checkpoint + parsed_checkpoint[index + 1:]
			index += len(seperate_messages)		
	return parsed_messages, parsed_checkpoint, errors, index

def advance_processing(in_parsed_messages: list[ParseMessage], in_parsed_checkpoint: list[ParseMessagePartIndexes], parse_config: ParseConfig, side: SIDE) \
						-> tuple[bool, list[ParseMessage], list[PairInt]]:
	'''
		Uses: 
			Seperate message: example 12, 123 dau => 12,13 dau; 156 xdau
		Return:
			bool: success
			list[Message]: parsed messages after handle
			list[PairInt]: indexes of error part
	'''
	parsed_checkpoint = in_parsed_checkpoint.copy()
	errors: list[PairInt] = []
	parsed_messages = in_parsed_messages
	index = 0
	while index < len(parsed_messages):
		if parsed_messages[index].is_failed_message:
			index += 1
			continue
		if not __is_number_valid(parsed_messages[index].numbers):
			parsed_messages[index].numbers = f"Số không đúng định dạng: {parsed_messages[index].numbers}"
			parsed_messages[index].is_failed_message = True
			errors.append(parsed_checkpoint[index].number_pair_index)
			index += 1
			continue
		if parsed_messages[index].type_bet == "DAUDUOI" or parsed_messages[index].type_bet == "DAU" or parsed_messages[index].type_bet == "DUOI":
			parsed_messages, parsed_checkpoint, errors, index = __handle_dauduoi(parsed_messages, parsed_checkpoint, errors, parse_config, index)

		elif parsed_messages[index].type_bet == "XDAU" or parsed_messages[index].type_bet == "XDUOI" or parsed_messages[index].type_bet == "XIUCHU":
			for number_index in range(len(parsed_messages[index].numbers)):
				if len(parsed_messages[index].numbers[number_index]) == 4:
					parsed_messages[index].numbers[number_index] = parsed_messages[index].numbers[number_index][-3:]	
				elif len(parsed_messages[index].numbers[number_index]) == 2:
					parsed_messages[index].numbers = f"Cách đánh xỉu không thể có 2 chữ số: {parsed_messages[index].numbers}" 
					parsed_messages[index].is_failed_message = True
					errors.append(parsed_checkpoint[index].number_pair_index)
					break
		elif "BAO" in parsed_messages[index].type_bet:
			parsed_messages, parsed_checkpoint, errors, index = __handle_bao(parsed_messages, parsed_checkpoint, errors, parse_config, index)
		elif "DAO" in parsed_messages[index].type_bet:
			for number_index in range(len(parsed_messages[index].numbers)):
				if len(parsed_messages[index].numbers[number_index]) == 2:
					parsed_messages[index].numbers =  f"Số có 2 chữ số không thể đánh đảo: {parsed_messages[index].numbers}"
					parsed_messages[index].is_failed_message = True
					errors.append(parsed_checkpoint[index].number_pair_index)
					break
				if len(parsed_messages[index].numbers[number_index]) == 4:
					if parsed_messages[index].type_bet == "DAODACBIET":
						parsed_messages[index].numbers = f"Cách đánh đảo đặc biệt phải có 4 chữ số: {parsed_messages[index].numbers}"
						parsed_messages[index].is_failed_message = True
						errors.append(parsed_checkpoint[index].number_pair_index)
						break
					elif "DAOXIU" in parsed_messages[index].type_bet:
						parsed_messages[index].numbers[number_index] = parsed_messages[index].numbers[number_index][-3:]

		elif parsed_messages[index].type_bet == "DAODACBIET":
			for number in parsed_messages[index].numbers:
				if len(number) != 4:
					parsed_messages[index].numbers = f"Cách đánh đảo đặc biệt phải có 4 chữ số: {parsed_messages[index].numbers}"
					parsed_messages[index].is_failed_message = True
					errors.append(parsed_checkpoint[index].number_pair_index)
					break
		elif parsed_messages[index].type_bet == "DA" or parsed_messages[index].type_bet == "DAVONG" or parsed_messages[index].type_bet == "DATHANG"\
				or parsed_messages[index].type_bet == "DAXIEN" or parsed_messages[index].type_bet == "DATHANGVONG" or parsed_messages[index].type_bet == "DAXIENVONG":		
			parsed_messages, parsed_checkpoint, errors, index = __handle_da(parsed_messages, parsed_checkpoint, errors, parse_config, index, side)

		index += 1

	return len(errors) == 0, parsed_messages, errors