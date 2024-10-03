class User:
	def __init__(self, user_id = "", username = "", password = "", role = "", is_blocked = False, is_deleted = False) -> None:
		self.user_id = user_id
		self.username = username
		self.password = password
		self.role = role
		self.is_blocked = is_blocked
		self.is_deleted = is_deleted