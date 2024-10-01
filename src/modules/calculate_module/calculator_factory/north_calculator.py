from src.modules.parse_module.parse_models.parse_message import ParseMessage
from src.modules.calculate_module.calculator_factory.calculator import Calculator, CalculateConfig, SIDE
from src.modules.calculate_module.calculator_models.calculate_result import CalculateResult
class NorthCalculator(Calculator):
	PRIZE_7_INDEX = 0
	PRIZE_6_INDEX = PRIZE_7_INDEX + 4
	PRIZE_5_INDEX = PRIZE_6_INDEX + 3
	PRIZE_4_INDEX = PRIZE_5_INDEX + 6
	PRIZE_3_INDEX = PRIZE_4_INDEX + 4
	PRIZE_2_INDEX = PRIZE_3_INDEX + 6
	PRIZE_1_INDEX = PRIZE_2_INDEX + 2
	PRIZE_JACKPOT_INDEX = PRIZE_1_INDEX + 1

	CONFIG_2D_DAU_INDEX = 0
	CONFIG_2D_DUOI_INDEX = CONFIG_2D_DAU_INDEX + 1
	CONFIG_2D_BAOLO_INDEX = CONFIG_2D_DUOI_INDEX + 1
	CONFIG_3D_DAU_INDEX = CONFIG_2D_BAOLO_INDEX + 1
	CONFIG_3D_DUOI_INDEX = CONFIG_3D_DAU_INDEX + 1
	CONFIG_3D_BAOLO_INDEX = CONFIG_3D_DUOI_INDEX + 1
	CONFIG_4D_DUOI_INDEX = CONFIG_3D_BAOLO_INDEX + 1
	CONFIG_4D_BAOLO_INDEX = CONFIG_4D_DUOI_INDEX + 1
	CONFIG_DA_INDEX = CONFIG_4D_BAOLO_INDEX + 1
	CONFIG_BROKERS_SIZE = CONFIG_DA_INDEX + 1

	def __init__(self, all_prizes: dict, calc_config: CalculateConfig, side: SIDE) -> None:
		super().__init__(all_prizes, calc_config, side)

	def __calc_a_prizes(self, message: ParseMessage, prize_index: int, in_calc_result: CalculateResult) -> CalculateResult:
		count_win = 0
		for channel_code in message.channels_code:
			for number in message.numbers:
				if number == self._all_prizes[channel_code][prize_index]:
					in_calc_result.win_numbers.append(number)
					count_win += 1
		return self._common_calc(in_calc_result, float(message.point_bet), count_win,
						   self._calc_config.brokers[self.CONFIG_2D_DAU_INDEX],
						   self._calc_config.rewards[self.CONFIG_2D_DAU_INDEX],
						   len(message.channels_code),
						   len(message.numbers),
						   Calculator.TYPE_BET_PRIZES_COUNT.SINGLE_PRIZE)
	
	def calc_a1(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		calc_result = in_calc_result.clone() if in_calc_result != None else CalculateResult()
		return self.__calc_a_prizes(message, self.PRIZE_7_INDEX, calc_result)
	
	def calc_a2(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		calc_result = in_calc_result.clone() if in_calc_result != None else CalculateResult()
		return self.__calc_a_prizes(message, self.PRIZE_7_INDEX + 1, calc_result)
	
	def calc_a3(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		calc_result = in_calc_result.clone() if in_calc_result != None else CalculateResult()
		return self.__calc_a_prizes(message, self.PRIZE_7_INDEX + 2, calc_result)
	
	def calc_a4(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		calc_result = in_calc_result.clone() if in_calc_result != None else CalculateResult()
		return self.__calc_a_prizes(message, self.PRIZE_7_INDEX + 3, calc_result)

	def calc_dau(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		calc_result = in_calc_result.clone() if in_calc_result != None else CalculateResult()
		count_win = 0
		for channel_code in message.channels_code:
			for number in message.numbers:
				for prize_index in range(self.PRIZE_7_INDEX, self.PRIZE_6_INDEX):
					if number == self._all_prizes[channel_code][prize_index]:
						calc_result.win_numbers.append(number)
						count_win += 1
		return self._common_calc(calc_result, float(message.point_bet), count_win,
						   self._calc_config.brokers[self.CONFIG_2D_DAU_INDEX],
						   self._calc_config.rewards[self.CONFIG_2D_DAU_INDEX],
						   len(message.channels_code), len(message.numbers),
						   Calculator.TYPE_BET_PRIZES_COUNT.A_PRIZES)
	
	def calc_duoi(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		calc_result = in_calc_result.clone() if in_calc_result != None else CalculateResult()
		count_win = 0
		if len(message.numbers[0]) == 2:
			broker_index = self.CONFIG_2D_DUOI_INDEX
		elif len(message.numbers[0]) == 3:
			broker_index = self.CONFIG_3D_DUOI_INDEX
		elif len(message.numbers[0]) == 4:
			broker_index = self.CONFIG_4D_DUOI_INDEX
		for channel_code in message.channels_code:
			for number in message.numbers:
				calc_result, count_win = self._check_win(channel_code, number, self.PRIZE_JACKPOT_INDEX, 
											 			calc_result, count_win)
		return self._common_calc(calc_result, float(message.point_bet), count_win,
						   		self._calc_config.brokers[broker_index],
								self._calc_config.rewards[broker_index],
								len(message.channels_code), len(message.numbers),
								Calculator.TYPE_BET_PRIZES_COUNT.SINGLE_PRIZE)
	
	def calc_xdau(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		calc_result = in_calc_result.clone() if in_calc_result != None else CalculateResult()
		count_win = 0
		for channel_code in message.channels_code:
			for number in message.numbers:
				for prize_index in range(self.PRIZE_6_INDEX, self.PRIZE_5_INDEX):
					calc_result, count_win = self._check_win(channel_code, number, prize_index, 
											  				calc_result, count_win)
		return self._common_calc(message, float(message.point_bet), count_win,
						   		self._calc_config.brokers[self.CONFIG_3D_DAU_INDEX],
								self._calc_config.rewards[self.CONFIG_3D_DAU_INDEX],
								len(message.channels_code), len(message.numbers),
								self.PRIZE_5_INDEX - self.PRIZE_6_INDEX)
	
	def calc_xduoi(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		calc_result = in_calc_result.clone() if in_calc_result != None else CalculateResult()
		count_win = 0
		for channel_code in message.channels_code:
			for number in message.numbers:
				calc_result, count_win = self._check_win(channel_code, number, self.PRIZE_JACKPOT_INDEX, 
											 			calc_result, count_win)
		return self._common_calc(message, float(message.point_bet), count_win,
						   		self._calc_config.brokers[self.CONFIG_3D_DUOI_INDEX],
								self._calc_config.rewards[self.CONFIG_3D_DUOI_INDEX],
								len(message.channels_code), len(message.numbers),
								Calculator.TYPE_BET_PRIZES_COUNT.SINGLE_PRIZE)
	
	def calc_dxdau(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		calc_result = in_calc_result.clone() if in_calc_result != None else CalculateResult()
		count_win = 0
		for channel_code in message.channels_code:
			num_of_number = 0
			for number in message.numbers:
				permutation_numbers = self._get_number_permutations(number)
				num_of_number += len(permutation_numbers)
				for permutaion_number in permutation_numbers:
					for prize_index in range(self.PRIZE_6_INDEX, self.PRIZE_5_INDEX):
						calc_result, count_win = self._check_win(channel_code, permutaion_number, 
											  					prize_index, calc_result, count_win)
		return self._common_calc(message, float(message.point_bet), count_win,
						   		self._calc_config.brokers[self.CONFIG_3D_DAU_INDEX],
								self._calc_config.rewards[self.CONFIG_3D_DAU_INDEX],
								len(message.channels_code), len(message.numbers),
								self.PRIZE_5_INDEX - self.PRIZE_6_INDEX)
	
	def calc_dxduoi(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		calc_result = in_calc_result.clone() if in_calc_result != None else CalculateResult()
		count_win = 0
		for channel_code in message.channels_code:
			num_of_number = 0
			for number in message.numbers:
				permutation_numbers = self._get_number_permutations(number)
				num_of_number += len(permutation_numbers)
				for permutaion_number in permutation_numbers:
					calc_result, count_win = self._check_win(channel_code, permutaion_number, 
											  				self.PRIZE_JACKPOT_INDEX, calc_result, count_win)
		return self._common_calc(message, float(message.point_bet), count_win,
						   		self._calc_config.brokers[self.CONFIG_3D_DUOI_INDEX],
								self._calc_config.rewards[self.CONFIG_3D_DUOI_INDEX],
								len(message.channels_code), num_of_number,
								Calculator.TYPE_BET_PRIZES_COUNT.SINGLE_PRIZE)
	
	def calc_daodacbiet(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		calc_result = in_calc_result.clone() if in_calc_result != None else CalculateResult()
		count_win = 0
		for channel_code in message.channels_code:
			num_of_number = 0
			for number in message.numbers:
				permutation_numbers = self._get_number_permutations(number)
				num_of_number += len(permutation_numbers)
				for permutaion_number in permutation_numbers:
					calc_result, count_win = self._check_win(channel_code, permutaion_number, 
											  				self.PRIZE_JACKPOT_INDEX, calc_result, count_win)
		return self._common_calc(message, float(message.point_bet), count_win,
						   		self._calc_config.brokers[self.CONFIG_4D_DUOI_INDEX],
								self._calc_config.rewards[self.CONFIG_4D_DUOI_INDEX],
								len(message.channels_code), num_of_number,
								Calculator.TYPE_BET_PRIZES_COUNT.SINGLE_PRIZE)
	
	def calc_baodao(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		calc_result = in_calc_result.clone() if in_calc_result != None else CalculateResult()
		count_win = 0
		for channel_code in message.channels_code:
			num_of_number = 0
			for number in message.numbers:
				if len(number) == 3:
					start_prize = self.PRIZE_6_INDEX
					broker_index = self.CONFIG_3D_DUOI_INDEX
				elif len(number) == 4:
					start_prize = self.PRIZE_5_INDEX
					broker_index = self.CONFIG_4D_DUOI_INDEX
					is_broker_multiplied = False
				permutation_numbers = self._get_number_permutations(number)
				num_of_number += len(permutation_numbers)
				for permutaion_number in permutation_numbers:
					for prize_index in range(start_prize, self.PRIZE_JACKPOT_INDEX + 1):
						calc_result, count_win = self._check_win(channel_code, permutaion_number, prize_index, 
																calc_result, count_win)
		return self._common_calc(message, float(message.point_bet), count_win,
						   		self._calc_config.brokers[broker_index],
								self._calc_config.rewards[broker_index],
								len(message.channels_code), len(message.numbers),
								Calculator.TYPE_BET_PRIZES_COUNT.ALL_NORTH - start_prize,
								is_broker_multiplied)
					
	def calc_baolo(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		calc_result = in_calc_result.clone() if in_calc_result != None else CalculateResult()
		count_win = 0
		is_broker_multiplied = self._calc_config.is_brokers_multiplied
		for channel_code in message.channels_code:
			for number in message.numbers:
				if len(number) == 2:
					start_prize = self.PRIZE_7_INDEX
					broker_index = self.CONFIG_2D_DUOI_INDEX
				elif len(number) == 3:
					start_prize = self.PRIZE_6_INDEX
					broker_index = self.CONFIG_3D_DUOI_INDEX
				elif len(number) == 4:
					start_prize = self.PRIZE_5_INDEX
					broker_index = self.CONFIG_4D_DUOI_INDEX
					is_broker_multiplied = False
				for prize_index in range(start_prize, self.PRIZE_JACKPOT_INDEX + 1):
					calc_result, count_win = self._check_win(channel_code, number, prize_index, 
											  				calc_result, count_win)
		return self._common_calc(message, float(message.point_bet), count_win,
						   self._calc_config.brokers[broker_index],
						   self._calc_config.rewards[broker_index],
						   len(message.channels_code), len(message.numbers),
						   Calculator.TYPE_BET_PRIZES_COUNT.ALL_NORTH - start_prize,
						   is_broker_multiplied)
	
	def calc_dathang(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		calc_result = in_calc_result.clone() if in_calc_result != None else CalculateResult()
		count_win = 0
		numbers_combinations = self._get_combinations(message.numbers)
		for combination_number in numbers_combinations:
			for channel_code in message.channels_code:
				first_count = 0
				second_count = 0
				pair_count_win = 0
				for prize in self._all_prizes[channel_code]:
					if combination_number[0][-2:] == prize[-2:] and \
						not (combination_number[0][-2:] == combination_number[1][-2:] \
		   						and first_count > second_count):
						first_count += 1
					elif combination_number[1][-2:] == prize[-2:]:
						second_count += 1
				if first_count > 0 and second_count > 0:
					calc_result.win_numbers.extend(combination_number)
					count_win += min(first_count, second_count)
					pair_count_win = min(first_count, second_count)

					if self._calc_config.is_halfKI_enabled(self._side):
						if first_count - second_count != 0 and pair_count_win == 1:
							count_win += 0.5
		return self._common_calc(message, float(message.point_bet), count_win,
						   		self._calc_config.brokers[self.CONFIG_DA_INDEX],
								self._calc_config.rewards[self.CONFIG_DA_INDEX],
								len(message.channels_code),
								len(message.numbers) * (len(message.numbers)-1),
								Calculator.TYPE_BET_PRIZES_COUNT.ALL_NORTH,
								self._calc_config.is_brokers_multiplied)