class ParseConfig:
	def __init__(self, syntax = "DSK", south_channels_order = [123, 123, 123, 123, 123, 123, 1234], 
			  		mid_channels_order = [123, 12, 12, 12, 123, 12, 123], enable_b_equal_duoi = False, 
					enable_da_trung = False, enable_da_cap = False, allow_duoi_3c_4c = False) -> None:
		self.syntax = syntax.upper()
		self.south_channels_order = south_channels_order
		self.mid_channels_order = mid_channels_order
		self.enable_b_equal_duoi = enable_b_equal_duoi
		self.enable_da_trung = enable_da_trung
		self.enable_da_cap = enable_da_cap
		self.allow_duoi_3c_4c = allow_duoi_3c_4c