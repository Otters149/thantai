from datetime import date
from src.entities.entities_helper import DBConnector, DB_TABLE_NAME, AppLogger
from src.models.export import User, UserInfo, Subscription

def subs_get_subs_by_userid(userid: str) -> Subscription:
	try:
		query = f"select * from {DB_TABLE_NAME.SUBSCRIPTION} where userid='{userid}'"
		result = DBConnector.instance().exe_select(query)
		if len(result) > 0:
			return Subscription.from_query(result[0])
		return None
	except Exception as e:
		AppLogger.e(f"[subs_get_subs_by_userid] Fatal: {e}")
		return None
	
def subs_update_expired_date(userid: str, new_expired: date) -> bool:
	try:
		query = f"update {DB_TABLE_NAME.SUBSCRIPTION} set expired_date='{new_expired}' where userid='{userid}"
		params = (new_expired, userid)
		return DBConnector.instance().exe_update(query, params)
	except Exception as e:
		AppLogger.e(f"[subs_update_expired_date] Fatal: {e}")
		return False
	