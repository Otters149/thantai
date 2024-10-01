from src.enums import SIDE

class CalculateConfig:
	def __init__(self, brokers: list[float] = [], reward: list[float] = [], half_ki: list[bool] = [], is_brokers_multiplied: bool = False) -> None:
		self.brokers = brokers
		self.rewards = reward
		self.half_ki = half_ki
		self.is_brokers_multiplied = is_brokers_multiplied

	def is_halfKI_enabled(self, side: SIDE) -> bool:
		return self.half_ki[side]