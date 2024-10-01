from src.enums import MONEY_UNIT

class ParseMessage:

	def __init__(self, order_index = 0, channels_code: list[str] = [], numbers : list[str] = [], type_bet = "", point_bet = "0", 
				 point_bet_unit = MONEY_UNIT.NONE, raw_order = "", raw_channels = "", raw_numbers = "", raw_typebet = "") -> None:
		self.order_index = order_index
		self.channels_code = channels_code
		self.numbers = numbers
		self.type_bet = type_bet
		self.point_bet = point_bet
		self.point_bet_unit = point_bet_unit

		self.raw_order = raw_order
		self.raw_channels = raw_channels
		self.raw_numbers = raw_numbers
		self.raw_typebet = raw_typebet

		self.is_failed_message = False

	@classmethod
	def new(cls):
		return cls()
	
	def to_bet_str(self) -> str:
		money_unit_str = "err"
		if self.point_bet_unit == MONEY_UNIT.NGHIN:
			money_unit_str = "nghin" 
		elif self.point_bet_unit == MONEY_UNIT.TRIEU:
			money_unit_str = "trieu"
		return f"Tin{self.order_index} {' '.join(self.channels_code)} {' '.join(self.numbers)} {self.type_bet} {self.point_bet} {money_unit_str}"
	
	def clone(self):
		return ParseMessage(self.order_index, 
					  self.channels_code.copy(), 
					  self.numbers.copy(), 
					  self.type_bet, 
					  self.point_bet, 
					  self.point_bet_unit, 
					  self.raw_order, 
					  self.raw_channels, 
					  self.raw_numbers, 
					  self.raw_typebet)

