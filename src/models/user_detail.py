from datetime import date, datetime

class UserDetail:
	FIELD_USER_ID = 0
	FIELD_USER_NAME = 1
	FIELD_ROLE = 2
	FIELD_IS_BLOCKED = 3
	FIELD_IS_DELETED = 4
	FIELD_DISPLAY_NAME = 5
	FIELD_WARNING = 6
	FIELD_CREATE_DATE = 7
	FIELD_NOTE = 8
	FIELD_IS_PREMIUM = 9
	FIELD_SUBSCRIBE_TELE_BOT = 10
	FIELD_EXPIRED_DATE = 11

	def __init__(self, user_id = "", username = "", role = "", is_blocked = False, is_deleted = False, \
				display_name = "", warning = False, create_date = None, note = "", \
				is_premium = False, subscribe_tele_bot = False, expired_date: date = None) -> None:
		self.user_id = user_id
		self.username = username
		self.role = role
		self.is_blocked = is_blocked
		self.is_deleted = is_deleted
		self.display_name = display_name
		self.warning = warning
		self.create_date = create_date
		self.note = note
		self.is_premium = is_premium
		self.subscribe_tele_bot = subscribe_tele_bot
		self.expired_date: date = expired_date		

	@classmethod
	def from_query(cls, query_data):
		return cls( query_data[UserDetail.FIELD_USER_ID], 
			 		query_data[UserDetail.FIELD_USER_NAME], 
					query_data[UserDetail.FIELD_ROLE], 
					query_data[UserDetail.FIELD_IS_BLOCKED], 
					query_data[UserDetail.FIELD_IS_DELETED], 
			 		query_data[UserDetail.FIELD_DISPLAY_NAME], 
					query_data[UserDetail.FIELD_WARNING],
					query_data[UserDetail.FIELD_CREATE_DATE], 
					query_data[UserDetail.FIELD_NOTE],
					query_data[UserDetail.FIELD_IS_PREMIUM], 
					query_data[UserDetail.FIELD_SUBSCRIBE_TELE_BOT],
					query_data[UserDetail.FIELD_EXPIRED_DATE] )
	
	def to_json(self):
		return {
			"userid": self.user_id,
			"username": self.username,
			"role": self.role,
			"is_blocked": self.is_blocked,
			"displayname": self.display_name,
			"warning": self.warning,
			"create_date": self.create_date,
			"note": self.note,
			"is_premium": self.is_premium,
			"is_subscribe_tele_bot": self.subscribe_tele_bot,
			"expired_date": self.expired_date
		}