from datetime import datetime

from src.enums import SIDE
from src.modules.parse_module.parse_models.parse_message import ParseMessage
from src.modules.calculate_module.calculator_factory.calculator_creator import CalculatorCreator, Calculator
from src.modules.calculate_module.calculator_models.calculate_config import CalculateConfig
from src.modules.calculate_module.calculator_models.calculate_result import CalculateResult
from src.modules.calculate_module.crawler_factory.crawler_creator import CrawlerCreator, Crawler

def __get_all_prize(lottery_result: dict[str, str]):
	'''
		Convert dictionary result into list of prizes
	'''
	prizes = []
	for i in range(8, 0, -1):
		prizes.extend(lottery_result[f"g{i}"].split(" "))
	prizes.append(lottery_result['db'])
	return prizes

def run_calculator_machine(messages: list[ParseMessage], calc_config: CalculateConfig, date_check: datetime, side: SIDE, force_result_not_available: bool, force_calc: bool) \
		-> tuple[bool, list[CalculateResult]]:
	'''
		Return:
			bool: success
			list[CalculateResult]: list of result mapping 1:1 with list of messsage
	'''
	crawler: Crawler = CrawlerCreator.create_crawler()
	success, lottery_result = crawler.crawl_result(side, date_check, force_result_not_available)
	if not success and not force_calc:
		return success, []
	
	all_prizes = {}
	for channel_code in lottery_result:
		all_prizes[channel_code] = __get_all_prize(lottery_result[channel_code])

	calculator: Calculator = CalculatorCreator().create_calculator(all_prizes, calc_config, side)
	calc_results: list[CalculateResult] = []
	for msg in messages:
		if msg.type_bet == "DAU":
			calc_results.append(calculator.calc_dau(msg))
		elif msg.type_bet == "DUOI":
			calc_results.append(calculator.calc_dau(msg))
		elif msg.type_bet == "DAUDUOI":
			rs = calculator.calc_dau(msg)
			rs = calculator.calc_dau(msg, rs)
			calc_results.append(rs)
		elif msg.type_bet == "XDAU":
			calc_results.append(calculator.calc_xdau(msg))
		elif msg.type_bet == "XDUOI":
			calc_results.append(calculator.calc_xduoi(msg))
		elif msg.type_bet == "XIUCHU":
			rs = calculator.calc_xdau(msg)
			rs = calculator.calc_xduoi(msg, rs)
			calc_results.append(rs)
		elif msg.type_bet == "DAOXIUDAU":
			calc_results.append(calculator.calc_dxdau(msg))
		elif msg.type_bet == "DAOXIUDUOI":
			calc_results.append(calculator.calc_dxduoi(msg))
		elif msg.type_bet == "DAOXIU":
			rs = calculator.calc_dxdau(msg)
			rs = calculator.calc_dxduoi(msg, rs)
			calc_results.append(rs)
		elif msg.type_bet =="BAOLO7":
			calc_results.append(calculator.calc_bao7lo(msg))
		elif msg.type_bet == "BAYLODAO":
			calc_results.append(calculator.calc_baodao7lo(msg))
		elif msg.type_bet == "BAOLO":
			calc_results.append(calculator.calc_baolo(msg))
		elif msg.type_bet == "BAODAO":
			calc_results.append(calculator.calc_baodao(msg))
		elif msg.type_bet == "DATHANG" or msg.type_bet == "DATHANGVONG":
			calc_results.append(calculator.calc_dathang(msg))
		elif msg.type_bet == "DAXIEN" or msg.type_bet == "DAXIENVONG":
			calc_results.append(calculator.calc_daxien(msg))
		elif msg.type_bet == "DAVONG":
			if len(msg.channels_code) == 1 or side == SIDE.NORTH:
				calc_results.append(calculator.calc_dathang(msg))
			else:
				calc_results.append(calculator.calc_daxien(msg))
		elif msg.type_bet == "BAODAO":
			calc_results.append(calculator.calc_baodao(msg))
		else:
			raise Exception("Not Implementation")

	return success, calc_results