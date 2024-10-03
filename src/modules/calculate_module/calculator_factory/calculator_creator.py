from src.modules.calculate_module.calculator_factory.calculator import Calculator, SIDE, CalculateConfig
from src.modules.calculate_module.calculator_factory.south_calculator import SouthCalculator
from src.modules.calculate_module.calculator_factory.north_calculator import NorthCalculator
class CalculatorCreator:
	def __init__(self) -> None:
		pass

	@classmethod
	def create_calculator(self, all_prizes: dict, calc_config: CalculateConfig, side: SIDE) -> Calculator:
		self.calculator = None
		if side == SIDE.NORTH:
			self.calculator = NorthCalculator(all_prizes, calc_config, side)
		else:
			self.calculator = SouthCalculator(all_prizes, calc_config, side)

		return self.calculator