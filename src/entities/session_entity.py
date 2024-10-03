from src.entities.entities_helper import DBConnector, DB_TABLE_NAME
from src.models.export import Session

def session_get_session_by_id(user_id: str) -> tuple[bool, Session]:
	try:
		query = f"select * from {DB_TABLE_NAME.SESSIONS} where userid='{user_id}'"
		result = DBConnector.instance().exe_select(query)
		if len(result) > 0:
			return True, Session.from_query(result)
		return False, None
	except:
		return False, None
	
def session_create_new_session(user_id: str, token: str, client_ip: str) -> bool:
	try:
		query = "insert into " + DB_TABLE_NAME.SESSIONS + " (`userid`, `refresh_token`, `client_ip`) values (%s, %s, %s)"
		params = (user_id, token, client_ip)
		insert_id  = DBConnector.instance().exe_insert(query, params)
		return insert_id != None
	except:
		return False
	
def session_update_session(user_id: str, new_token: str, new_client_ip: str) -> bool:
	try:
		query = "update " + DB_TABLE_NAME.SESSIONS + " set token=%s, client_ip=%s where id=%s"
		params = (new_token, new_client_ip, user_id)
		return DBConnector.instance().exe_update(query, params)
	except:
		return False
	
def session_close_session(user_id: str):
	try:
		query = "update " + DB_TABLE_NAME.SESSIONS + " set token=%s, client_ip=%s where id=%s"
		params = ("LOG_OUT", "LOG_OUT", user_id)
		return DBConnector.instance().exe_update(query, params)
	except:
		return False