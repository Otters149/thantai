from abc import ABC, abstractmethod

from itertools import permutations, combinations

from src.enums import SIDE
from src.modules.parse_module.parse_models.parse_message import ParseMessage
from src.modules.calculate_module.calculator_models.calculate_result import CalculateResult
from src.modules.calculate_module.calculator_models.calculate_config import CalculateConfig

class Calculator(ABC):
	class TYPE_BET_PRIZES_COUNT:
		SINGLE_PRIZE = 1
		A_PRIZES = 4
		SEVEN_PRIZE = 7
		ALL_SOUTH = 18
		ALL_NORTH = 27

	def __init__(self, all_prizes: dict, calc_config: CalculateConfig, side: SIDE) -> None:
		self._calc_config = calc_config
		self._all_prizes = all_prizes
		self._side = side

	def _get_number_permutations(self, number: str) -> list[str]:
		return list(set(["".join(i) for i in permutations(number)]))
	
	def _get_combinations(self, list_of_str: list[str]):# -> combinations[tuple[str, str]]:
		return combinations(list_of_str, 2)

	def _check_win(self, channel_code: str, number: str, prize_index: int, in_calc_result: CalculateResult, in_count_win: float) -> tuple[CalculateResult, int]:
		'''
			Return:
				CalculateResult: out calculate result
				int: count win
		'''
		if number == self._all_prizes[channel_code][prize_index][-len(number):]:
			in_calc_result.win_numbers.append(number)
			in_count_win += 1
		return in_calc_result, in_count_win

	def _common_calc(self, calc_result: CalculateResult, point_bet: float, count_win: float, brokers: float, reward: float, num_of_channels: int, num_of_numbers: int, num_of_prize:int, brokers_multiplied = False) -> CalculateResult:
		# Công thức: Xác = (Tổng số lượng số chơi) x Điểm x (Tổng số giải dò) x (Tổng số đài dò)
		real_money = num_of_numbers * point_bet * num_of_prize * num_of_channels
		calc_result.real_money = calc_result.real_money + real_money
		calc_result.reward = reward
		if brokers_multiplied:
			brokers_money_rounded = round(point_bet * num_of_numbers * num_of_channels * brokers, 2)
		else:
			brokers_money_rounded = round(real_money * brokers * 0.01, 2)
		calc_result.minus_brokers_money = calc_result.minus_brokers_money + brokers_money_rounded
		
		win_money_rounded = round(point_bet * count_win, 2)
		calc_result.win_money = calc_result.win_money + win_money_rounded

		total_money_rounded = round(brokers_money_rounded - win_money_rounded * reward, 2)
		calc_result.total_money = calc_result.total_money + total_money_rounded
		return calc_result

	@abstractmethod
	def calc_a1(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		pass

	@abstractmethod
	def calc_a2(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		pass

	@abstractmethod
	def calc_a3(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		pass
	
	@abstractmethod
	def calc_a4(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		pass	

	@abstractmethod
	def calc_dau(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		pass

	@abstractmethod
	def calc_duoi(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		pass

	@abstractmethod
	def calc_xdau(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		pass

	@abstractmethod
	def calc_xduoi(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		pass

	@abstractmethod
	def calc_dxdau(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		pass

	@abstractmethod
	def calc_dxduoi(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		pass

	@abstractmethod
	def calc_daodacbiet(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		pass

	@abstractmethod
	def calc_baodao7lo(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		pass

	@abstractmethod
	def calc_bao7lo(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		pass

	@abstractmethod
	def calc_baodao(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		pass

	@abstractmethod
	def calc_baolo(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		pass

	@abstractmethod
	def calc_dathang(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		pass

	@abstractmethod
	def calc_daxien(self, message: ParseMessage, in_calc_result: CalculateResult = None) -> CalculateResult:
		pass