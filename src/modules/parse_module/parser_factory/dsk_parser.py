from src.modules.parse_module.parser_factory.parser import Parser, ParseConfig, ParseMessage, datetime, SIDE, PairInt, ParseMessagePartIndexes
from src.modules.module_hepler import get_channel_code_by_date
from src.logger import AppLogger

class DSKParser(Parser):
	def __init__(self) -> None:
		super().__init__()
		self.cache_use_same_type = []
		self.cache_use_same_raw_type = []
		self.cache_use_same_number = []

	def __dsk_parse_order(self, in_message_str: str, in_pre_parse_msg: ParseMessage, in_current_parse_msg: ParseMessage, ceiling: int = 100) -> tuple[bool, str, ParseMessage]:
		'''
			Return:
				bool: success
				str: message after cut off
				ParseMessage: current parsed message
		'''
		message_str = in_message_str
		pre_parse_msg = in_pre_parse_msg
		current_parse_msg = in_current_parse_msg
		success, message_str, order_index, raw_order_str = self._parse_order(message_str, ceiling)

		current_parse_msg.raw_order = raw_order_str
		if not success and pre_parse_msg != None:
			current_parse_msg.order_index = pre_parse_msg.order_index
		else:
			current_parse_msg.order_index = order_index
		message_str = self._skip_whitespace_dot_and_comma(message_str)
		AppLogger.d(f"[PARSE ORDER] Order = {order_index}")	
		return success, message_str, current_parse_msg	

	def __dsk_parse_channels(self, in_message_str: str, in_pre_parse_msg: ParseMessage, in_current_parse_msg: ParseMessage, channels_code_for_check: list[str], side: SIDE) \
							-> tuple[bool, str, ParseMessage]:
		'''
			Return:
				bool: success
				str: message after cut off
				ParseMessage: previous parsed message
		'''
		message_str = in_message_str
		pre_parse_msg = in_pre_parse_msg
		current_parse_msg = in_current_parse_msg
		success, message_str, channels_code_found, raw_channels_str = self._parse_channel(message_str, channels_code_for_check, side)
		
		if success:
			current_parse_msg.raw_channels = raw_channels_str
			current_parse_msg.channels_code = channels_code_found
		else:
			current_parse_msg.raw_channels = ""
			if side == SIDE.NORTH:
				success = True
				current_parse_msg.channels_code = ["MB"]
			elif len(channels_code_found) == 0 and pre_parse_msg != None:
				success = True
				current_parse_msg.channels_code = pre_parse_msg.channels_code
			else:
				AppLogger.e(f"[PARSE CHANNEL] Fatal: {raw_channels_str}")
		message_str = self._skip_whitespace_dot_and_comma(message_str)
		AppLogger.d(f"[PARSE CHANNEL] Parsed: {current_parse_msg.channels_code}")
		return success, message_str, current_parse_msg

	def __dsk_parse_numbers(self, in_message_str: str, in_pre_parse_msg: ParseMessage, in_current_parse_msg: ParseMessage) -> tuple[bool, str, ParseMessage]:
		'''
			Return:
				bool: success
				str: message after cut off
				ParseMessage: previous parsed message
		'''
		message_str = in_message_str
		pre_parse_msg = in_pre_parse_msg
		current_parse_msg = in_current_parse_msg
		success, message_str, numbers_found, raw_numbers_str = self._parse_number(message_str)

		if success:
			current_parse_msg.raw_numbers = raw_numbers_str
			current_parse_msg.numbers = numbers_found
			self.cache_use_same_type = []
			self.cache_use_same_number = []
			self.cache_use_same_raw_type = []
		else:
			current_parse_msg.raw_numbers = ""
			if len(numbers_found) == 0 and pre_parse_msg != None and current_parse_msg.raw_channels == "" and current_parse_msg.raw_order == "":
				success = True
				current_parse_msg.numbers = pre_parse_msg.numbers
			else:
				AppLogger.e(f"[PARSE NUMBERS] Fatal: {raw_numbers_str}")
		message_str = self._skip_whitespace_dot_and_comma(message_str)
		AppLogger.d(f"[PARSE NUMBERS] Parsed: {current_parse_msg.numbers}")
		return success, message_str, current_parse_msg

	def __dsk_parse_type_bet(self, in_message_str: str, in_pre_parse_msg: ParseMessage, in_current_parse_msg: ParseMessage) -> tuple[bool, str, ParseMessage]:
		'''
			Return:
				bool: success
				str: message after cut off
				ParseMessage: previous parsed message
		'''
		message_str = in_message_str
		pre_parse_msg = in_pre_parse_msg
		current_parse_msg = in_current_parse_msg
		success, message_str, type_bet_found, raw_type_bet_str = self._parse_type_bet(message_str)

		current_parse_msg.raw_typebet = raw_type_bet_str
		if success:
			current_parse_msg.type_bet = type_bet_found

			if current_parse_msg.raw_numbers == "":
				is_same_type_bet_flag = False
				for index in range(len(self.cache_use_same_type) - 1, -1, -1):
					if type_bet_found == self.cache_use_same_type[index]:
						if type_bet_found == "UNDETERMINED" and (raw_type_bet_str != self.cache_use_same_raw_type[index] or raw_type_bet_str == "d"):
							AppLogger.i(f"[DIFF] type: {raw_type_bet_str} - cache_type: {self.cache_use_same_raw_type[index]} => Do not cut off number")
							pass
						else:
							is_same_type_bet_flag = True
							new_num = []
							for number in self.cache_use_same_number[index]:
								new_num.append(number[1:])
								if len(new_num[1:]) == 1:
									success = False
									break
							current_parse_msg.numbers = new_num
							break
				if not is_same_type_bet_flag: # That mean: same numbers but didn't same type => use origin numbers
					current_parse_msg.numbers = self.cache_use_same_number[0]
			
			self.cache_use_same_type.append(type_bet_found)
			self.cache_use_same_raw_type.append(raw_type_bet_str)
			self.cache_use_same_number.append(current_parse_msg.numbers)
		else:
			AppLogger.e(f"[PARSE TYPEBET] Fatal: {raw_type_bet_str}")
		message_str = self._skip_whitespace_dot_and_comma(message_str)
		AppLogger.d(f"[PARSE TYPEBET] Parsed: {current_parse_msg.type_bet} - raw='{current_parse_msg.raw_typebet}'")
		return success, message_str, current_parse_msg

	def __dsk_parse_point_pet(self, in_message_str: str, in_pre_parse_msg: ParseMessage, in_current_parse_msg: ParseMessage, syntax: str) -> tuple[bool, str, ParseMessage]:
		'''
			Return:
				bool: success
				str: message after cut off
				ParseMessage: previous parsed message
		'''
		message_str = in_message_str
		pre_parse_msg = in_pre_parse_msg
		current_parse_msg = in_current_parse_msg
		success, message_str, point_bet_found, point_bet_unit = self._parse_point_bet(message_str, syntax)
		if success:
			current_parse_msg.point_bet = point_bet_found
			current_parse_msg.point_bet_unit = point_bet_unit
		else:
			AppLogger.i(f"[PARSE POINTBET] Can not found point bet")
		message_str = self._skip_whitespace_dot_and_comma(message_str)
		AppLogger.d(f"[PARSE POINTBET] Parsed: {current_parse_msg.point_bet} - unit='{current_parse_msg.point_bet_unit}'")
		return success, message_str, current_parse_msg

	def __check_error_phrase(self, in_message_str: str, is_checking_skip_error_phrase: bool, in_pair_error_index: PairInt, msg_len_before_process: int) -> tuple[str, PairInt]:
			'''
				Return:
					str: message after cut off
					PairInt: range of error
			'''
			message_str = in_message_str
			pair_error_index = in_pair_error_index

			if not is_checking_skip_error_phrase:
				pair_error_index.first = msg_len_before_process - len(message_str)
				message_str = message_str[1:]
			else:
				message_str = message_str[1:]
				pair_error_index.second = msg_len_before_process - len(message_str)

			return message_str, pair_error_index


	def run(self, input: str, parse_config: ParseConfig, date_check: datetime, side: SIDE) -> tuple[bool, str, list[ParseMessage], list[ParseMessagePartIndexes], list[PairInt], str]:
		results: list[ParseMessage] = []
		checkpoint: list[ParseMessagePartIndexes] = []
		error_checkpoint: list[PairInt] = []

		message_standardized = super()._standardization(input)
		handling_str = message_standardized
		channels_code_for_check = get_channel_code_by_date(side, date_check)

		pre_parse_msg: ParseMessage = None
		current_parse_msg: ParseMessage = None

		msg_len_before_process = len(handling_str)

		is_checking_skip_error_phrase = False
		pair_error_index = PairInt()
		while len(handling_str) > 0:
			has_error_in_signle_loop = False
			current_parse_msg = ParseMessage.new()
			parse_message_indexes = ParseMessagePartIndexes()
			

			#=================================================================================================
			pair_index = PairInt(msg_len_before_process - len(handling_str), msg_len_before_process)
			success, handling_str, current_parse_msg = self.__dsk_parse_order(handling_str, pre_parse_msg, current_parse_msg, ceiling=100)
			if not success and current_parse_msg.order_index == 100:
				success, handling_str, current_parse_msg = self.__dsk_parse_order(handling_str, pre_parse_msg, current_parse_msg, ceiling=300)
			pair_index.second = msg_len_before_process - len(handling_str)
			parse_message_indexes.order_pair_index = pair_index

			pair_index = PairInt(msg_len_before_process - len(handling_str), msg_len_before_process)
			success, handling_str, current_parse_msg = self.__dsk_parse_channels(handling_str, pre_parse_msg, current_parse_msg, channels_code_for_check, side)
			if success:
				pair_index.second = msg_len_before_process - len(handling_str)
				parse_message_indexes.channel_pair_index = pair_index

				pair_index = PairInt(msg_len_before_process - len(handling_str), msg_len_before_process)
				success, handling_str, current_parse_msg = self.__dsk_parse_numbers(handling_str, pre_parse_msg, current_parse_msg)
				if success:
					pair_index.second = msg_len_before_process - len(handling_str)
					parse_message_indexes.number_pair_index = pair_index

					pair_index = PairInt(msg_len_before_process - len(handling_str), msg_len_before_process)
					success, handling_str, current_parse_msg = self.__dsk_parse_type_bet(handling_str, pre_parse_msg, current_parse_msg)
					if success:
						pair_index.second = msg_len_before_process - len(handling_str)
						parse_message_indexes.type_bet_pair_index = pair_index

						pair_index = PairInt(msg_len_before_process - len(handling_str), msg_len_before_process)
						success, handling_str, current_parse_msg = self.__dsk_parse_point_pet(handling_str, pre_parse_msg, current_parse_msg, parse_config.syntax)
						pair_index.second = msg_len_before_process - len(handling_str)
						parse_message_indexes.point_bet_pair_index = pair_index

			if not success:
				handling_str, pair_error_index = self.__check_error_phrase(handling_str, is_checking_skip_error_phrase, pair_error_index, msg_len_before_process)
				is_checking_skip_error_phrase = True
				has_error_in_signle_loop = True

			if not has_error_in_signle_loop:
				if is_checking_skip_error_phrase:
					is_checking_skip_error_phrase = False
					error_checkpoint.append(pair_error_index)
					pair_error_index = PairInt()
			#=================================================================================================

			if not is_checking_skip_error_phrase:
				pre_parse_msg = current_parse_msg
				results.append(current_parse_msg)
				checkpoint.append(parse_message_indexes)

		if is_checking_skip_error_phrase:
			error_checkpoint.append(pair_error_index)

		return len(error_checkpoint) == 0, message_standardized, results, checkpoint, error_checkpoint