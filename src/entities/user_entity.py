from src.entities.entities_helper import DBConnector, DB_TABLE_NAME, AppLogger
from src.models.export import User, UserInfo, Subscription, UserDetail

def user_create_user(user: User, userinfo: UserInfo, subscription: Subscription) -> tuple[bool, User, UserInfo, Subscription]:
	try:
		query = ("insert into " + DB_TABLE_NAME.USERS + \
		   				" (`username`, `password`, `role`, `is_blocked`, `is_deleted`) \
						VALUES (%s, %s, %s, %s, %s)")
		params = (user.username, user.password, user.role, user.is_blocked, user.is_deleted)
		insert_id = DBConnector.instance().exe_insert(query, params)
		if insert_id != None:
			user.user_id = insert_id
			query = ("insert into " + DB_TABLE_NAME.USER_INFOS + \
							" (`userid`, `display_name`, `warning`, `created_date`, `note`) \
							VALUES (%s, %s, %s, %s, %s)")
			params = (insert_id, userinfo.display_name, userinfo.warning, userinfo.create_date, userinfo.note)
			userinfo_insert_id = DBConnector.instance().exe_insert(query, params)
			userinfo.userid = userinfo_insert_id

			query = ("insert into " + DB_TABLE_NAME.SUBSCRIPTION + \
							" (`userid`, `is_premium`, `subscribe_tele_bot`, `expired_date`) \
							VALUES (%s, %s, %s, %s)")
			params = (insert_id, subscription.is_premium, subscription.subscribe_tele_bot, subscription.expired_date)
			subs_insert_id = DBConnector.instance().exe_insert(query, params)
			subscription.userid = subs_insert_id
			return True, user, userinfo, subscription
		return False, None, None, None
	except Exception as e:
		AppLogger.e(f"[user_create_user] Fatal: {e}")
		return False, None, None, None

def user_get_user_by_username_password(username: str, hash_pass: str) -> tuple[bool, User]:
	try:
		query = f"select * from {DB_TABLE_NAME.USERS} where username='{username}' and password='{hash_pass}'"
		result = DBConnector.instance().exe_select(query)
		if len(result) > 0:
			return True, User.from_query(result[0])
		return False, None
	except Exception as e:
		AppLogger.e(f"[user_get_user_by_username_password] Fatal: {e}")
		return False, None

def user_check_user_existing_by_username(username: str) -> bool:
	try:
		query = f"select 'userid' from {DB_TABLE_NAME.USERS} where username='{username}'"
		result = DBConnector.instance().exe_select(query)
		return result != None and len(result) > 0
	except Exception as e:
		AppLogger.e(f"[user_check_user_existing_by_username] Fatal: {e}")
		return True	

def user_get_user_by_id(userid: str) -> User:
	try:
		query = f"select * from {DB_TABLE_NAME.USERS} where userid='{userid}'"
		result = DBConnector.instance().exe_select(query)
		if len(result) > 0:
			return User.from_query(result[0])
		return None
	except Exception as e:
		AppLogger.e(f"[user_get_user_by_id] Fatal: {e}")
		return None
	
def user_update_user_password(userid: str, new_hash_pwd: str) -> bool:
	try:
		query = "update " + DB_TABLE_NAME.USERS + " set password=%s where userid=%s"
		params = (new_hash_pwd, userid)
		return DBConnector.instance().exe_update(query, params)
	except Exception as e:
		AppLogger.e(f"[user_update_user_password] Fatal: {e}")
		return False
	
def user_soft_delete_user(userid: str) -> bool:
	try:
		query = "update " + DB_TABLE_NAME.USERS + " set is_deleted=%s where userid=%s"
		params = (1, userid)
		return DBConnector.instance().exe_update(query, params)
	except Exception as e:
		AppLogger.e(f"[user_soft_delete_user] Fatal: {e}")
		return False
	
def user_soft_delete_user_recovery(userid: str) -> bool:
	try:
		query = "update " + DB_TABLE_NAME.USERS + " set is_deleted=%s where userid=%s"
		params = (0, userid)
		return DBConnector.instance().exe_update(query, params)
	except Exception as e:
		AppLogger.e(f"[user_soft_delete_user_recovery] Fatal: {e}")
		return False
	
def user_count_num_of_activate_users() -> int:
	try:
		query = f"select count(*) from {DB_TABLE_NAME.USERS} where is_deleted='0'"
		result = DBConnector.instance().exe_select(query)[0]
		return result[0]
	except Exception as e:
		AppLogger.e(f"[user_count_num_of_activate_users] Fatal: {e}")
		return 0
	
def user_count_num_of_recyclebin_users() -> int:
	try:
		query = f"select count(*) from {DB_TABLE_NAME.USERS} where is_deleted='1'"
		result = DBConnector.instance().exe_select(query)[0]
		return result[0]
	except Exception as e:
		AppLogger.e(f"[user_count_num_of_recyclebin_users] Fatal: {e}")
		return 0
	
def user_get_range_activate_users(admin_id:str, limit: int, offset: int) -> list[UserDetail]:
	try:
		query = f'''select {DB_TABLE_NAME.USERS}.userid, username, role, is_blocked, is_deleted, 
				display_name, warning, created_date, note, 
				is_premium, subscribe_tele_bot, expired_date
				from {DB_TABLE_NAME.USERS} 
				join {DB_TABLE_NAME.USER_INFOS} on {DB_TABLE_NAME.USERS}.userid = {DB_TABLE_NAME.USER_INFOS}.userid
				join {DB_TABLE_NAME.SUBSCRIPTION} on {DB_TABLE_NAME.USERS}.userid = {DB_TABLE_NAME.SUBSCRIPTION}.userid
				where {DB_TABLE_NAME.USERS}.userid != '{admin_id}' && is_deleted='0' limit {limit} offset {offset}'''
		result = DBConnector.instance().exe_select(query)
		users: list[UserDetail] = []
		for item in result:
			AppLogger.d(f"[Fetch Item] {item}")
			user_detail = UserDetail.from_query(item)
			users.append(user_detail)
		return users
	except Exception as e:
		AppLogger.e(f"[user_get_all_range_users] Fatal: {e}")
		return []
	
def user_get_range_recyclebin_users(limit: int, offset: int) -> list[UserDetail]:
	try:
		query = f'''select {DB_TABLE_NAME.USERS}.userid, username, role, is_blocked, is_deleted, 
				display_name, warning, created_date, note, 
				is_premium, subscribe_tele_bot, expired_date
				from {DB_TABLE_NAME.USERS} 
				join {DB_TABLE_NAME.USER_INFOS} on {DB_TABLE_NAME.USERS}.userid = {DB_TABLE_NAME.USER_INFOS}.userid
				join {DB_TABLE_NAME.SUBSCRIPTION} on {DB_TABLE_NAME.USERS}.userid = {DB_TABLE_NAME.SUBSCRIPTION}.userid
				where is_deleted='1' limit {limit} offset {offset}'''
		result = DBConnector.instance().exe_select(query)
		users: list[UserDetail] = []
		for item in result:
			AppLogger.d(f"[Fetch Item] {item}")
			user_detail = UserDetail.from_query(item)
			users.append(user_detail)
		return users
	except Exception as e:
		AppLogger.e(f"[user_get_range_recyclebin_users] Fatal: {e}")
		return []
