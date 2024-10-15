from src.entities.entities_helper import DBConnector, DB_TABLE_NAME
from src.models.export import Session
from src.logger import AppLogger

def session_get_session_by_id(user_id: str) -> tuple[bool, Session]:
	try:
		query = f"select * from {DB_TABLE_NAME.SESSIONS} where userid='{user_id}'"
		result = DBConnector.instance().exe_select(query)
		if result != None and len(result) > 0:
			return True, Session.from_query(result[0])
		return False, None
	except Exception as ex:
		AppLogger.e(f"[session_get_session_by_id] {ex}")
		return False, None
	
def session_create_new_session(user_id: str, token: str, client_ip: str) -> bool:
	try:
		success, _ = session_get_session_by_id(user_id)
		if success:
			return session_update_session(user_id, token, client_ip)
		else:
			query = "insert into " + DB_TABLE_NAME.SESSIONS + " (`userid`, `refresh_token`, `client_ip`) values (%s, %s, %s)"
			params = (user_id, token, client_ip)
			insert_id  = DBConnector.instance().exe_insert(query, params)
			return insert_id != None
	except:
		return False
	
def session_update_session(user_id: str, new_token: str, new_client_ip: str) -> bool:
	try:
		query = "update " + DB_TABLE_NAME.SESSIONS + " set refresh_token=%s, client_ip=%s where userid=%s"
		params = (new_token, new_client_ip, user_id)
		return DBConnector.instance().exe_update(query, params)
	except:
		return False
	
def session_close_session(user_id: str):
	try:
		query = "update " + DB_TABLE_NAME.SESSIONS + " set refresh_token=%s, client_ip=%s where userid=%s"
		params = ("LOG_OUT", "LOG_OUT", user_id)
		return DBConnector.instance().exe_update(query, params)
	except:
		return False