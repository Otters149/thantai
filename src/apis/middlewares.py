from functools import wraps
from flask import request, jsonify
from src.utils import jwt_validate
from src.enums import RESPONSE_CODE
from src.entities.export import session_get_session_by_id

def is_auth_jwt(jwt_data: str) -> bool:
	'''
		TODO: Create JWT Object to save more data such as: subscription values
	'''
	return jwt_data['payload'] == 'auth'

def __wraps_success(data, f, *args, **kwargs):
	kwargs['jwt_data'] = data
	return f(*args, **kwargs)

def wraps_jwt_check(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		token = request.headers['Carrier']
		data, success, err_code = jwt_validate(token)
		if success:
			if is_auth_jwt(data):
				return __wraps_success(data, f, *args, **kwargs)
			else:
				return jsonify({"error": "Token invalid"}), RESPONSE_CODE.UNAUTHORIZED
		else:
			return jsonify({"error": data}), err_code
	return decorated_function

def wraps_jwt_refresh_check(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		token = request.headers['Carrier']
		ip = request.headers['IP']
		data, success, err_code = jwt_validate(token)
		if success:
			success, session = session_get_session_by_id(data['id'])
			if success and session.refresh_token == token and session.client_ip == ip:
				return __wraps_success(data, f, *args, **kwargs)
			else:
				return jsonify({"error": "Session expired"}), 401 
		else:
			return jsonify({"error": data}), err_code
	return decorated_function