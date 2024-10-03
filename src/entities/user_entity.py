from src.entities.entities_helper import DBConnector, DB_TABLE_NAME
from src.models.export import User

def user_create_user(user: User) -> tuple[bool, User]:
	try:
		query = ("insert into " + DB_TABLE_NAME.USERS + \
		   				" (`username`, `password`, `role`, `is_blocked`, `is_deleted`) \
						VALUES (%s, %s, %s, %s, %s)")
		params = (user.username, user.password, user.role, user.is_blocked, user.is_deleted)
		insert_id = DBConnector.instance().exe_insert(query, params)
		if insert_id != None:
			user.user_id = insert_id
			return True, user
		return False, None
	except:
		return False, None
