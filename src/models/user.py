class User:
	FIELD_USER_ID = 0
	FIELD_USER_NAME = 1
	FIELD_PASSWORD = 2
	FIELD_ROLE = 3
	FIELD_IS_BLOCKED = 4
	FIELD_IS_DELETED = 5

	def __init__(self, user_id = "", username = "", password = "", role = "", is_blocked = False, is_deleted = False) -> None:
		self.user_id = user_id
		self.username = username
		self.password = password
		self.role = role
		self.is_blocked = is_blocked
		self.is_deleted = is_deleted

	@classmethod
	def from_query(cls, query_data):
		return cls( query_data[User.FIELD_USER_ID], 
			 		query_data[User.FIELD_USER_NAME], 
					query_data[User.FIELD_PASSWORD],
					query_data[User.FIELD_ROLE], 
					query_data[User.FIELD_IS_BLOCKED], 
					query_data[User.FIELD_IS_DELETED] )
	
	@classmethod
	def from_request_json(cls, request_json):
		try:
			user = cls( "0000",
			  			request_json['username'],
						request_json['password'],
						request_json['role'],
						False,
						False)
			return user
		except:
			return None