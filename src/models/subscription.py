from datetime import date, datetime

class Subscription:
	FIELD_USER_ID = 0
	FIELD_IS_PREMIUM = 1
	FIELD_SUBSCRIBE_TELE_BOT = 2
	FIELD_EXPIRED_DATE = 3
	def __init__(self, userid = "", is_premium = False, subscribe_tele_bot = False, expired_date: date = None) -> None:
		self.userid = userid
		self.is_premium = is_premium
		self.subscribe_tele_bot = subscribe_tele_bot
		self.expired_date: date = expired_date

	@classmethod
	def from_query(cls, query_data):
		return cls( query_data[Subscription.FIELD_USER_ID], 
					query_data[Subscription.FIELD_IS_PREMIUM], 
					query_data[Subscription.FIELD_SUBSCRIBE_TELE_BOT],
					query_data[Subscription.FIELD_EXPIRED_DATE] )
	
	@classmethod
	def from_request_json(cls, request_json):
		try:
			subs = cls( "",
			  			request_json["is_premium"],
						request_json["is_subs_tele_bot"],
						datetime.strptime(request_json["expired_date"], '%d/%m/%Y').date())
			return subs
		except:
			return None