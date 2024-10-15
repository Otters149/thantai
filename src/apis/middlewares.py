from functools import wraps
from flask import request, jsonify
from src.utils import jwt_validate
from src.enums import RESPONSE_CODE, ROLE
from src.entities.export import session_get_session_by_id
from src.apis.jwt_data import JWTData

def get_jwt_in_header(json_data) -> str:
	return json_data['Authorization']

def is_auth_jwt(jwt_data: JWTData) -> bool:
	return jwt_data.type == JWTData.JWT_TYPE.ACCESS

def __wraps_success(jwt_data: JWTData, f, *args, **kwargs):
	kwargs['jwt_data'] = jwt_data
	return f(*args, **kwargs)

def wraps_admin_check(f):
	@wraps(f)
	def decorated_function(*args, **kwargs): 
		token = get_jwt_in_header(request.headers)
		data, success, err_code = jwt_validate(token)
		if success:
			jwt_data = JWTData.from_data(data)
			if is_auth_jwt(jwt_data):			
				if jwt_data.role != ROLE.Admin.name:
					return jsonify({"error": "Forbiden"}), RESPONSE_CODE.FORBIDDEN
				return __wraps_success(jwt_data, f, *args, **kwargs)
			return jsonify({"error": "Token invalid"}), RESPONSE_CODE.UNAUTHORIZED
		return jsonify({"error": data}), err_code
	return decorated_function

def wraps_admin_or_owner_check(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		token = get_jwt_in_header(request.headers)
		data, success, err_code = jwt_validate(token)
		if success:
			jwt_data = JWTData.from_data(data)
			if is_auth_jwt(jwt_data):
				if jwt_data.role == ROLE.Admin.name or jwt_data.id == str(kwargs['user_id']):
					return __wraps_success(jwt_data, f, *args, **kwargs)
				return jsonify({"error": "Forbiden"}), RESPONSE_CODE.FORBIDDEN
			return jsonify({"error": "Token invalid"}), RESPONSE_CODE.UNAUTHORIZED
		return jsonify({"error": data}), err_code
	return decorated_function

def wraps_admin_or_manager_check(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		token = get_jwt_in_header(request.headers)
		data, success, err_code = jwt_validate(token)
		if success:
			jwt_data = JWTData.from_data(data)
			if is_auth_jwt(jwt_data):
				if jwt_data.role == ROLE.Admin.name or jwt_data.role == ROLE.Manager.name:
					return __wraps_success(jwt_data, f, *args, **kwargs)
				return jsonify({"error": "Forbiden"}), RESPONSE_CODE.FORBIDDEN
			return jsonify({"error": "Token invalid"}), RESPONSE_CODE.UNAUTHORIZED
		return jsonify({"error": data}), err_code
	return decorated_function

def wraps_jwt_check(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		token = get_jwt_in_header(request.headers)
		data, success, err_code = jwt_validate(token)
		if success:
			jwt_data = JWTData.from_data(data)
			if is_auth_jwt(jwt_data):
				return __wraps_success(jwt_data, f, *args, **kwargs)
			return jsonify({"error": "Token invalid"}), RESPONSE_CODE.UNAUTHORIZED
		return jsonify({"error": data}), err_code
	return decorated_function

def wraps_jwt_refresh_check(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		token = get_jwt_in_header(request.headers)
		ip = request.headers['IP']
		data, success, err_code = jwt_validate(token)
		if success:
			jwt_data = JWTData.from_data(data)
			if is_auth_jwt(jwt_data):
				return jsonify({"error": "jwt invalid!"}), RESPONSE_CODE.UNAUTHORIZED
			success, session = session_get_session_by_id(data['id'])
			if success and session.refresh_token == token and session.client_ip == ip:
				return __wraps_success(jwt_data, f, *args, **kwargs)
			return jsonify({"error": "Session expired"}), RESPONSE_CODE.UNAUTHORIZED 
		return jsonify({"error": data}), err_code
	return decorated_function
