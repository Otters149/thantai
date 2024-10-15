class Session:
	FIELD_USER_ID = 0
	FIELD_REFRESH_TOKEN = 1
	FIELD_CLIENT_IP = 2
	
	def __init__(self, user_id = "", refesh_token = "", client_ip = "") -> None:
		self.user_id = user_id
		self.refresh_token = refesh_token
		self.client_ip = client_ip

	@classmethod
	def from_query(cls, query_data):
		return cls( query_data[Session.FIELD_USER_ID], 
					query_data[Session.FIELD_REFRESH_TOKEN], 
					query_data[Session.FIELD_CLIENT_IP] )