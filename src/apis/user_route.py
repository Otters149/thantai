from src.apis.api_hepler import *
from src.models.export import User, UserInfo, Subscription, UserDetail
from src.utils import md5_get_hash, rsa_decode, format_id
from src.entities.export import user_create_user, user_check_user_existing_by_username, \
						user_count_num_of_activate_users, user_count_num_of_recyclebin_users, \
						user_get_range_activate_users, user_get_range_recyclebin_users, \
						user_get_user_by_id, user_update_user_password,\
						user_soft_delete_user, user_soft_delete_user_recovery, \
						subs_update_expired_date
user_api = Blueprint('user_api', __name__)

@user_api.route('/user/create', methods=['POST'])
@swag_from({
    'summary': 'Create new user',
    'description': 'This endpoint create a new user, only admin have this permission',
    'parameters': [
        SWAGGER_AUTHORIZATION_HEADER,
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string", 
                        "description": "Username"
                    },
                    "password": {
                        "type": "string",
                        "description": "RSA-encode password"
					},
					"role": {
                        "type": "string",
                        "description": "Role: Admin/Manager/User"
					},
					"note": {
                        "type": "string",
                        "description": "Note for user"
					},
					"is_premium": {
                        "type": "boolean",
                        "description": "Is premium user"
					},
					"is_subs_tele_bot": {
                        "type": "boolean",
                        "description": "Has subscribe telegram bot"
					},
					"expired_date": {
                        "type": "boolean",
                        "description": "Account expired date. Format: %d/%m/%Y"
					}
                },
                "required": ["old_pasword", "new_password"]
            }
        }		
    ],
    'responses': {
        200: {
            "description": "Create user success",
            "schema": {
                "type": "string",
				"description": "Id of user has been created"
            }
        },
		400: {
            "description": "Create failed",
            "schema": {
				"type": "object",
				"properties": {
					"error": {
						"type": "string"
					}
				}
            }
        },
        401: SWAGGER_UNAUTHORIZE_ERROR_CODE_RESPONSE,
    }
})
@wraps_admin_check
def create_new_user(jwt_data: JWTData):
	user = User.from_request_json(request.json)
	user_info = UserInfo.from_request_json(request.json)
	subscription = Subscription.from_request_json(request.json)
	if user != None and user_info != None and subscription != None:
		user.password = md5_get_hash(rsa_decode(user.password))
		if user_check_user_existing_by_username(user.username):
			return jsonify({"error":"Username has taken!"}), RESPONSE_CODE.BAD_REQUEST
		success, user, user_info, subscription = user_create_user(user, user_info, subscription)
		if success:
			return format_id(user.user_id), RESPONSE_CODE.CREATED
		return jsonify({"error" : "Internal Server Error!"}), RESPONSE_CODE.INTERNAL_SERVER_ERROR
	return jsonify({"error" : "Data Invalid!"}), RESPONSE_CODE.BAD_REQUEST

@user_api.route('/user/update-password', methods=['PATCH'])
@swag_from({
    'summary': 'Update user password',
    'description': 'This endpoint update password by onwer user from token',
    'parameters': [
        SWAGGER_AUTHORIZATION_HEADER,
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "old_password": {
                        "type": "string", 
                        "description": "RSA-encode old password"
                    },
                    "new_password": {
                        "type": "string",
                        "description": "RSA-encode new password"
                      }
                },
                "required": ["old_pasword", "new_password"]
            }
        }  
    ],
    'responses': {
        200: {
            "description": "Update success",
			"type": "string"
        },
		400: {
            "description": "Update failed",
            "schema": {
				"type": "object",
				"properties": {
					"error": {
						"type": "string"
					}
				}
            }
        },
        401: SWAGGER_UNAUTHORIZE_ERROR_CODE_RESPONSE,
    }
})
@wraps_jwt_check
def update_user_password(jwt_data: JWTData):
	old_pwd = md5_get_hash(rsa_decode(request.json['old_password']))
	new_pwd = md5_get_hash(rsa_decode(request.json["new_password"]))
	user = user_get_user_by_id(jwt_data.id)
	if user != None:
		if user.password != old_pwd:
			return jsonify({"error": "Old password incorrect!"}), RESPONSE_CODE.BAD_REQUEST
		if user_update_user_password(jwt_data.id, new_pwd):
			return "Success", RESPONSE_CODE.OK
		return jsonify({"error": "Can not update user's password!"}), RESPONSE_CODE.INTERNAL_SERVER_ERROR
	return jsonify({"error": "Can not find user!"}), RESPONSE_CODE.BAD_REQUEST

@user_api.route('/user/reset-password', methods=['PATCH'])
@swag_from({
    'summary': 'Reset user password',
    'description': 'This endpoint reset user password by admin',
    'parameters': [
        SWAGGER_AUTHORIZATION_HEADER,
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "userid": {
                        "type": "string", 
                        "description": "User id"
                    },
                    "password": {
                        "type": "string",
                        "description": "New password rsa-encode"
                      }
                },
                "required": ["userid", "password"]
            }
        }  
    ],
    'responses': {
        200: {
            "description": "Reset success",
			"type": "string"
        },
		400: {
            "description": "Reset failed",
            "schema": {
				"type": "object",
				"properties": {
					"error": {
						"type": "string"
					}
				}
            }
        },
        401: SWAGGER_UNAUTHORIZE_ERROR_CODE_RESPONSE,
    }
})
@wraps_admin_check
def reset_user_password(jwt_data: JWTData):
	if user_update_user_password(request.json["userid"], md5_get_hash(rsa_decode(request.json["password"]))):
		return "Success", RESPONSE_CODE.OK
	return jsonify({"error": "Can not reset password!"}), RESPONSE_CODE.BAD_REQUEST

@user_api.route('/user/subscribe', methods=['PATCH'])
@swag_from({
    'summary': 'Subscribe',
    'description': 'This endpoint update user subscribe',
    'parameters': [
        SWAGGER_AUTHORIZATION_HEADER,
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "userid": {
                        "type": "string", 
                        "description": "User id"
                    },
                    "date": {
                        "type": "string",
                        "description": "New expired date string. Format: %d/%m/%Y"
                      }
                },
                "required": ["userid", "date"]
            }
        }  
    ],
    'responses': {
        200: {
            "description": "Reset success",
			"type": "string"
        },
		400: {
            "description": "Reset failed",
            "schema": {
				"type": "object",
				"properties": {
					"error": {
						"type": "string"
					}
				}
            }
        },
        401: SWAGGER_UNAUTHORIZE_ERROR_CODE_RESPONSE,
		500: SWAGGER_INTERNAL_SERVER_ERROR_CODE_RESPONSE
    }
})
@wraps_admin_check
def update_expired_date(jwt_data: JWTData):
	try:
		date = datetime.strptime(request["date"], "%d/%m/%Y").date()
		if subs_update_expired_date(request["userid"], date):
			return "Success", RESPONSE_CODE.OK
		return jsonify({"error": "Can not update expired date!"}, RESPONSE_CODE.INTERNAL_SERVER_ERROR)
	except:
		return jsonify({"error": "Date format invalid. Please use format: %d/%m/%Y"}), RESPONSE_CODE.BAD_REQUEST

@user_api.route('/user/count/activate', methods=['GET'])
@swag_from({
    'summary': 'Count active user',
    'description': 'This endpoint get num of users which activated',
    'parameters': [
        SWAGGER_AUTHORIZATION_HEADER, 
    ],
    'responses': {
        200: {
            "description": "Count success",
			"schema": {
				"type": "integer",
				"description": "Number of users"
			}
        },
        401: SWAGGER_UNAUTHORIZE_ERROR_CODE_RESPONSE,
    }
})
@wraps_admin_check
def get_num_of_activate_users(jwt_data: JWTData):
	count = user_count_num_of_activate_users() - 1	# -1: Admin account (query account)
	return str(count), RESPONSE_CODE.OK

@user_api.route('/user/count/recyclebin', methods=['GET'])
@swag_from({
    'summary': 'Count inactive user',
    'description': 'This endpoint get num of users which already soft deleted',
    'parameters': [
        SWAGGER_AUTHORIZATION_HEADER, 
    ],
    'responses': {
        200: {
            "description": "Count success",
			"schema": {
				"type": "integer",
				"description": "Number of users"
			}
        },
        401: SWAGGER_UNAUTHORIZE_ERROR_CODE_RESPONSE,
    }
})
@wraps_admin_check
def get_num_of_recyclebin_users(jwt_data: JWTData):
	count = user_count_num_of_recyclebin_users()
	return str(count), RESPONSE_CODE.OK

@user_api.route('/user/delete/soft/<userid>', methods=['DELETE'])
@swag_from({
    'summary': 'Soft delete user',
    'description': 'This endpoint soft delete user (move user to group recyclebin)',
    'parameters': [
        SWAGGER_AUTHORIZATION_HEADER, 
    ],
    'responses': {
        200: {
            "description": "Delete success",
			"type": "string",
        },
        401: SWAGGER_UNAUTHORIZE_ERROR_CODE_RESPONSE,
		500: SWAGGER_INTERNAL_SERVER_ERROR_CODE_RESPONSE
    }
})
@wraps_admin_check
def soft_delete_user(jwt_data: JWTData, userid):
	if user_soft_delete_user(userid):
		return "Success", RESPONSE_CODE.OK
	return "Failed", RESPONSE_CODE.INTERNAL_SERVER_ERROR

@user_api.route('/user/recovery/<userid>', methods=['PATCH'])
@swag_from({
    'summary': 'Recovery user',
    'description': 'This endpoint recovery user which soft deleted',
    'parameters': [
        SWAGGER_AUTHORIZATION_HEADER, 
		{
			"name": "userid",
			"description": "Id of user which recovery",
			"type": "string",
			"required": True,
			"in": "path"
		},
    ],
    'responses': {
        200: {
            "description": "Recovery success",
			"type": "string",
        },
        401: SWAGGER_UNAUTHORIZE_ERROR_CODE_RESPONSE,
		500: SWAGGER_INTERNAL_SERVER_ERROR_CODE_RESPONSE
    }
})
@wraps_admin_check
def soft_delete_user_recovery(jwt_data: JWTData, userid):
	if user_soft_delete_user_recovery(userid):
		return "Success", RESPONSE_CODE.OK
	return "Failed", RESPONSE_CODE.INTERNAL_SERVER_ERROR

@user_api.route('/user/delete/permanently/<userid>', methods=['DELETE'])
@wraps_admin_check
def permanently_delete_user(jwt_data: JWTData, userid):
	pass

@user_api.route('/user/list/activate/<limit>/<offset>', methods=['GET'])
@swag_from({
    'summary': 'Get list user active',
    'description': 'This endpoint get list of active user with limit number of records and begin from offset',
    'parameters': [
        SWAGGER_AUTHORIZATION_HEADER, 
		{
			"name": "limit",
			"description": "Number of records fetching",
			"type": "string",
			"required": True,
			"in": "path"
		},
		{
			"name": "offset",
			"description": "Number of records skip fetching",
			"type": "string",
			"required": True,
			"in": "path"
		},
    ],
    'responses': {
        200: {
            "description": "Get success",
			"schema": {
				"type": "array",
				"description": "List of user-detail entity",
				"items": {
					"type": "object",
					"properties": {
						"userid": { "type": "string"},
						"username": { "type": "string"},
						"role": { "type": "string"},
						"is_blocked": { "type": "boolean"},
						"displayname": { "type": "string"},
						"warning": { "type": "boolean"},
						"create_date": { "type": "string"},
						"note": { "type": "string"},
						"is_premium": { "type": "boolean"},
						"is_subscribe_tele_bot": { "type": "boolean"},
						"expired_date": { "type": "string"},
					}
				}
			}
        },
        401: SWAGGER_UNAUTHORIZE_ERROR_CODE_RESPONSE,
		500: SWAGGER_INTERNAL_SERVER_ERROR_CODE_RESPONSE
    }
})
@wraps_admin_check
def list_of_activate_users(jwt_data: JWTData, limit: int, offset: int):
	user_details = user_get_range_activate_users(jwt_data.id, limit, offset)
	response = []
	for user in user_details:
		response.append(user.to_json())
	return jsonify(response), RESPONSE_CODE.OK

@user_api.route('/user/list/recyclebin/<limit>/<offset>', methods=['GET'])
@swag_from({
    'summary': 'Get list user inactive',
    'description': 'This endpoint get list of recyclebin user with limit number of records and begin from offset',
    'parameters': [
        SWAGGER_AUTHORIZATION_HEADER, 
		{
			"name": "limit",
			"description": "Number of records fetching",
			"type": "string",
			"required": True,
			"in": "path"
		},
		{
			"name": "offset",
			"description": "Number of records skip fetching",
			"type": "string",
			"required": True,
			"in": "path"
		},
    ],
    'responses': {
        200: {
            "description": "Get success",
			"schema": {
				"type": "array",
				"description": "List of user-detail entity",
				"items": {
					"type": "object",
					"properties": {
						"userid": { "type": "string"},
						"username": { "type": "string"},
						"role": { "type": "string"},
						"is_blocked": { "type": "boolean"},
						"displayname": { "type": "string"},
						"warning": { "type": "boolean"},
						"create_date": { "type": "string"},
						"note": { "type": "string"},
						"is_premium": { "type": "boolean"},
						"is_subscribe_tele_bot": { "type": "boolean"},
						"expired_date": { "type": "string"},
					}
				}
			}
        },
        401: SWAGGER_UNAUTHORIZE_ERROR_CODE_RESPONSE,
		500: SWAGGER_INTERNAL_SERVER_ERROR_CODE_RESPONSE
    }
})
@wraps_admin_check
def list_of_recyclebin_users(jwt_data: JWTData, limit: int, offset: int):
	user_details = user_get_range_recyclebin_users(limit, offset)
	response = []
	for user in user_details:
		response.append(user.to_json())
	return jsonify(response), RESPONSE_CODE.OK