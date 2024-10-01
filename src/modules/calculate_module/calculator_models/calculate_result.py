class CalculateResult:
	def __init__(self, win_numbers: list[str] = [], win_money: float = 0, real_money: float = 0, minus_brokers_money: float = 0, total_money: float = 0, reward: float = 0) -> None:
		self.win_numbers = win_numbers
		self.win_money = win_money
		self.real_money = real_money
		self.minus_brokers_money = minus_brokers_money
		self.total_money = total_money
		self.reward = reward

	def to_readable_str(self):
		return f"Win numbers: {' '.join(self.win_numbers)} - Win money: {self.win_money} - Real money: {self.real_money} - Brokers money: {self.minus_brokers_money} - Total money: {self.total_money} - Reward: {self.reward}"
	
	def clone(self):
		return CalculateResult(self.win_numbers.copy(),
						 self.win_money,
						 self.real_money,
						 self.minus_brokers_money,
						 self.total_money,
						 self.reward)