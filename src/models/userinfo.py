from datetime import datetime, timezone

class UserInfo:
	FIELD_USER_ID = 0
	FIELD_DISPLAY_NAME = 1
	FIELD_WARNING = 2
	FIELD_CREATE_DATE = 3
	FIELD_NOTE = 4

	def __init__(self, userid = "", display_name = "", warning = False, create_date = None, note = "") -> None:
		self.userid = userid
		self.display_name = display_name
		self.warning = warning
		self.create_date = create_date
		self.note = note
		
	@classmethod
	def from_query(cls, query_data):
		return cls( query_data[UserInfo.FIELD_USER_ID], 
			 		query_data[UserInfo.FIELD_DISPLAY_NAME], 
					query_data[UserInfo.FIELD_WARNING],
					query_data[UserInfo.FIELD_CREATE_DATE], 
					query_data[UserInfo.FIELD_NOTE] )
	
	@classmethod
	def from_request_json(cls, request_json):
		try:
			info = cls( "",
			  			request_json["display_name"],
						False,
						datetime.now(tz=timezone.utc),
						request_json["note"])
			return info
		except:
			return None