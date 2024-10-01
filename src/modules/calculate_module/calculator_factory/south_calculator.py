from src.modules.parse_module.parse_models.parse_message import ParseMessage
from src.modules.calculate_module.calculator_factory.calculator import Calculator, CalculateConfig, SIDE
from src.modules.calculate_module.calculator_models.calculate_result import CalculateResult
class SouthCalculator(Calculator):
	PRIZE_8_INDEX = 0
	PRIZE_7_INDEX = PRIZE_8_INDEX + 1
	PRIZE_6_INDEX = PRIZE_7_INDEX + 1
	PRIZE_5_INDEX = PRIZE_6_INDEX + 3
	PRIZE_4_INDEX = PRIZE_5_INDEX + 1
	PRIZE_3_INDEX = PRIZE_4_INDEX + 7
	PRIZE_2_INDEX = PRIZE_3_INDEX + 2
	PRIZE_1_INDEX = PRIZE_2_INDEX + 1
	PRIZE_JACKPOT_INDEX = PRIZE_1_INDEX + 1

	CONFIG_2D_DAU_INDEX = 0
	CONFIG_2D_DUOI_INDEX = CONFIG_2D_DAU_INDEX + 1
	CONFIG_2D_LO7_INDEX = CONFIG_2D_DUOI_INDEX + 1
	CONFIG_2D_BAOLO_INDEX = CONFIG_2D_LO7_INDEX + 1
	CONFIG_3D_DAU_INDEX = CONFIG_2D_BAOLO_INDEX + 1
	CONFIG_3D_DUOI_INDEX = CONFIG_3D_DAU_INDEX + 1
	CONFIG_3D_LO7_INDEX = CONFIG_3D_DUOI_INDEX + 1
	CONFIG_3D_BAOLO_INDEX = CONFIG_3D_LO7_INDEX + 1
	CONFIG_4D_DUOI_INDEX = CONFIG_3D_BAOLO_INDEX + 1
	CONFIG_4D_BAOLO_INDEX = CONFIG_4D_DUOI_INDEX + 1
	CONFIG_DA_INDEX = CONFIG_4D_BAOLO_INDEX + 1
	CONFIG_DAXIEN_INDEX = CONFIG_DA_INDEX + 1
	CONFIG_BROKERS_SIZE = CONFIG_DAXIEN_INDEX + 1

	def __init__(self, all_prizes: dict, calc_config: CalculateConfig, side: SIDE) -> None:
		super().__init__(all_prizes, calc_config, side)

	def __calc_dauduoi(self, message: ParseMessage, in_calc_result: CalculateResult, prize_index: int, broker_index: int) -> CalculateResult:
		calc_result = in_calc_result.clone() if in_calc_result != None else CalculateResult()
		count_win = 0
		for channel_code in message.channels_code:
			for number in message.numbers:
				calc_result, count_win = self._check_win(channel_code, number, prize_index, 
											 			calc_result, count_win)
				
		return self._common_calc(calc_result, float(message.point_bet), count_win,
						   self._calc_config.brokers[broker_index],
						   self._calc_config.rewards[broker_index],
						   len(message.channels_code), len(message.numbers),
						   Calculator.TYPE_BET_PRIZES_COUNT.SINGLE_PRIZE)
	def calc_dau(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		return self.__calc_dauduoi(message, in_calc_result, self.PRIZE_8_INDEX, self.CONFIG_2D_DAU_INDEX)
	
	def calc_duoi(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		if len(message.numbers[0]) == 2:
			broker_index = self.CONFIG_2D_DUOI_INDEX
		elif len(message.numbers[0]) == 3:
			broker_index = self.CONFIG_3D_DUOI_INDEX
		elif len(message.numbers[0]) == 4:
			broker_index = self.CONFIG_4D_DUOI_INDEX
		return self.__calc_dauduoi(message, in_calc_result, self.PRIZE_JACKPOT_INDEX, broker_index)

	def calc_xdau(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		return self.__calc_dauduoi(message, in_calc_result, self.PRIZE_7_INDEX, self.CONFIG_3D_DAU_INDEX)
	
	def calc_xduoi(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		return self.__calc_dauduoi(message, in_calc_result, self.PRIZE_JACKPOT_INDEX, self.CONFIG_3D_DUOI_INDEX)
	
	def __calc_dxdauduoi(self, message: ParseMessage, in_calc_result: CalculateResult, prize_index: int, broker_index: int) -> CalculateResult:
		calc_result = in_calc_result.clone() if in_calc_result != None else CalculateResult()
		count_win = 0
		for channel_code in message.channels_code:
			num_of_number = 0
			for number in message.numbers:
				permutation_numbers = self._get_number_permutations(number)
				num_of_number += len(permutation_numbers)
				for permutaion_number in permutation_numbers:
					calc_result, count_win = self._check_win(channel_code, permutaion_number, 
											  				prize_index, calc_result, count_win)
		return self._common_calc(calc_result, float(message.point_bet), count_win,
						   self._calc_config.brokers[broker_index],
						   self._calc_config.rewards[broker_index],
						   len(message.channels_code),
						   num_of_number,
						   Calculator.TYPE_BET_PRIZES_COUNT.SINGLE_PRIZE)

	def calc_dxdau(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		return self.__calc_dxdauduoi(message, in_calc_result, self.PRIZE_7_INDEX, self.CONFIG_3D_DAU_INDEX)
	
	def calc_dxduoi(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		return self.__calc_dxdauduoi(message, in_calc_result, self.PRIZE_JACKPOT_INDEX, self.CONFIG_3D_DUOI_INDEX)
	
	def calc_daodacbiet(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		return self.__calc_dxdauduoi(message, in_calc_result, self.PRIZE_JACKPOT_INDEX, self.CONFIG_4D_DUOI_INDEX)
	
	def calc_bao7lo(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		calc_result = in_calc_result.clone() if in_calc_result != None else CalculateResult()
		count_win = 0
		for channel_code in message.channels_code:
			for number in message.numbers:
				if len(number) == 2:
					start = self.PRIZE_8_INDEX
					broker = self._calc_config.brokers[self.CONFIG_2D_LO7_INDEX]
					reward = self._calc_config.rewards[self.CONFIG_2D_LO7_INDEX]
				elif len(number) >= 3:
					start = self.PRIZE_7_INDEX
					broker = self._calc_config.brokers[self.CONFIG_3D_LO7_INDEX]
					reward = self._calc_config.rewards[self.CONFIG_3D_LO7_INDEX]
					number = number[-3:]

				for prize in range(start, start + 7):
					calc_result, count_win = self._check_win(channel_code, number, prize, calc_result, count_win)
				calc_result, count_win = self._check_win(channel_code, number, self.PRIZE_JACKPOT_INDEX, calc_result, count_win)
		return self._common_calc(calc_result, float(message.point_bet), count_win, broker, reward, 
						   len(message.channels_code), len(message.numbers), 
						   Calculator.TYPE_BET_PRIZES_COUNT.SEVEN_PRIZE,
						   self._calc_config.is_brokers_multiplied)
	
	def calc_baodao7lo(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		calc_result = in_calc_result.clone() if in_calc_result != None else CalculateResult()
		count_win = 0
		for channel_code in message.channels_code:
			num_of_number = 0
			for number in message.numbers:
				start = self.PRIZE_7_INDEX
				broker = self._calc_config.brokers[self.CONFIG_3D_BAOLO_INDEX]
				reward = self._calc_config.rewards[self.CONFIG_3D_BAOLO_INDEX]
				permutation_numbers = self._get_number_permutations(number[-3:])
				num_of_number += len(permutation_numbers)
				for permutaion_number in permutation_numbers:
					for prize_index in range(start, start + 7):
						calc_result, count_win = self._check_win(channel_code, permutaion_number, prize_index, calc_result, count_win)
		return self._common_calc(calc_result, float(message.point_bet), count_win, broker, reward,
						   len(message.channels_code), num_of_number,
						   Calculator.TYPE_BET_PRIZES_COUNT.SEVEN_PRIZE,
						   self._calc_config.is_brokers_multiplied)
	
	def calc_baolo(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		calc_result = in_calc_result.clone() if in_calc_result != None else CalculateResult()
		count_win = 0
		is_broker_multiplied = self._calc_config.is_brokers_multiplied
		for channel_code in message.channels_code:
			for number in message.numbers:
				if len(number) == 2:
					start_prize = self.PRIZE_8_INDEX
					broker = self._calc_config.brokers[self.CONFIG_2D_BAOLO_INDEX]
					reward = self._calc_config.rewards[self.CONFIG_2D_BAOLO_INDEX]
				elif len(number) == 3:
					start_prize = self.PRIZE_7_INDEX
					broker = self._calc_config.brokers[self.CONFIG_3D_BAOLO_INDEX]
					reward = self._calc_config.rewards[self.CONFIG_3D_BAOLO_INDEX]
				elif len(number) == 4:
					start_prize = self.PRIZE_6_INDEX
					broker = self._calc_config.brokers[self.CONFIG_4D_BAOLO_INDEX]
					reward = self._calc_config.rewards[self.CONFIG_4D_BAOLO_INDEX]
					is_broker_multiplied = False
				for prize_index in range(start_prize, self.PRIZE_JACKPOT_INDEX + 1):
					calc_result, count_win = self._check_win(channel_code, number, prize_index, calc_result, count_win)
		return self._common_calc(calc_result, float(message.point_bet), count_win, broker, reward,
								len(message.channels_code), len(message.numbers),
								Calculator.TYPE_BET_PRIZES_COUNT.ALL_SOUTH - start_prize,
								is_broker_multiplied)
	
	def calc_baodao(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		calc_result = in_calc_result.clone() if in_calc_result != None else CalculateResult()
		count_win = 0
		is_broker_multiplied = self._calc_config.is_brokers_multiplied
		for channel_code in message.channels_code:
			num_of_number = 0
			for number in message.numbers:
				if len(number) == 3:
					start_prize = self.PRIZE_7_INDEX
					broker = self._calc_config.brokers[self.CONFIG_3D_BAOLO_INDEX]
					reward = self._calc_config.rewards[self.CONFIG_3D_BAOLO_INDEX]
				elif len(number) == 4:
					start_prize = self.PRIZE_6_INDEX
					broker = self._calc_config.brokers[self.CONFIG_4D_BAOLO_INDEX]
					reward = self._calc_config.rewards[self.CONFIG_4D_BAOLO_INDEX]     
					is_broker_multiplied = False
				permutation_numbers = self._get_number_permutations(number)
				num_of_number += len(permutation_numbers)
				for permutaion_number in permutation_numbers:
					for prize_index in range(start_prize, self.PRIZE_JACKPOT_INDEX + 1):
						calc_result, count_win = self._check_win(channel_code, permutaion_number, 
											   					prize_index, calc_result, count_win)
		return self._common_calc(calc_result, float(message.point_bet), count_win, broker, reward,
								len(message.channels_code), num_of_number,
								Calculator.TYPE_BET_PRIZES_COUNT.ALL_SOUTH - start_prize,
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
		return self._common_calc(calc_result, float(message.point_bet), count_win,
						   		self._calc_config.brokers[self.CONFIG_DA_INDEX],
								self._calc_config.rewards[self.CONFIG_DA_INDEX],
								len(message.channels_code),
								len(message.numbers) * (len(message.numbers)-1),
								Calculator.TYPE_BET_PRIZES_COUNT.ALL_SOUTH,
								self._calc_config.is_brokers_multiplied)
	
	def calc_daxien(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		calc_result = in_calc_result.clone() if in_calc_result != None else CalculateResult()
		count_win = 0
		numbers_combinations = self._get_combinations(message.numbers)
		for combination_number in numbers_combinations:
			channels_combinations = self._get_combinations(message.channels_code)
			for combination_channel in channels_combinations:
				first_count = 0
				second_count = 0
				all_prizes: list[str] = self._all_prizes[combination_channel[0]] + self._all_prizes[combination_channel[1]]
				for prize in all_prizes:
					if combination_number[0][-2:] == prize[-2:] and \
						not (combination_number[0][-2:] == combination_number[1][-2:] \
		   					and first_count > second_count):
						first_count += 1
					elif combination_number[1][-2:] == prize[-2:]:
						second_count += 1
				if first_count > 0 and second_count > 0:
					calc_result.win_numbers.extend(combination_number)
					count_win += min(first_count, second_count)
		return self._common_calc(calc_result, float(message.point_bet), count_win,
						   		self._calc_config.brokers[self.CONFIG_DAXIEN_INDEX],
								self._calc_config.rewards[self.CONFIG_DAXIEN_INDEX],
								len(message.channels_code) * (len(message.channels_code)-1),
								len(message.numbers) * (len(message.numbers) - 1),
								Calculator.TYPE_BET_PRIZES_COUNT.ALL_SOUTH,
								self._calc_config.is_brokers_multiplied)
