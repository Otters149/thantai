from src.apis.api_hepler import *
from src.utils import str_remove_accents, str_replace_uncommon_char, md5_get_hash, rsa_decode, format_id
from src.entities.export import user_update_user_password, user_get_user_by_id, user_get_user_by_username_password, \
                                session_create_new_session, session_close_session, \
                                subs_get_subs_by_userid
from configure import access_token_expired_time_in_minute, refresh_token_expired_time_in_day

auth_api = Blueprint('auth_api', __name__)

@auth_api.route('/auth/login', methods=['POST'])
@swag_from({
    'summary': 'Login',
    'description': 'This endpoint login user account',
    'parameters': [
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
                    "client_ip": {
                        "type": "string",
                        "description": "Client IP address"
                    }
                },
                "required": ["username", "password", "client_ip"]
            }
        }     
    ],
    'responses': {
        200: {
            "description": "Login success",
            "schema": {
              "type": "object",
              "properties": {
                "userid": { "type": "string" },
                "access_token": { "type": "string" },
                "refresh_token": { "type": "string" },
                "role": { "type": "string" },
                "expired_date": { "type": "string" },
                "is_premium": { "type": "boolean" },
                "subscribe_tele_bot": { "type": "boolean" },
              }
            }
        },
        400: {
            "description": "Bad request",
            "schema": {
              "type": "object",
              "properties": {
                "error": { "type": "string" }
              }
            }            
        },
    }
})
def login():
    if 'username' not in request.json or 'password' not in request.json or 'client_ip' not in request.json:
        return jsonify({"error": "Dữ liệu không hợp lệ!"}), RESPONSE_CODE.BAD_REQUEST
    username = str_remove_accents(request.json['username'])
    username = str_replace_uncommon_char(username)
    username = username.replace(" ", "")
    username = username.lower()
    if username != "":
        pwd = request.json['password']
        AppLogger.d(f'[Decode_Password] {rsa_decode(pwd)}')
        AppLogger.d(f'[Hash_Password] {md5_get_hash(rsa_decode(pwd))}')
        password = md5_get_hash(rsa_decode(request.json['password']))
        success, user = user_get_user_by_username_password(username, password)
        if not success:
            return jsonify({"error": "Tài khoản hoặc mật khẩu không đúng!"}), RESPONSE_CODE.BAD_REQUEST
        if user.is_deleted:
            return jsonify({"error": "Tài khoản không tồn tại!"}), RESPONSE_CODE.BAD_REQUEST

        subscription = subs_get_subs_by_userid(user.user_id)
        is_expired = True
        if subscription != None:
            is_expired = subscription.expired_date < datetime.now(tz=app_timezone).date()
        if is_expired or user.is_blocked:
            return jsonify({"error": "Tài khoản hiện tại không khả dụng!"}), RESPONSE_CODE.BAD_REQUEST
        now = datetime.now(tz=timezone.utc)
        access_token_expired = now + timedelta(minutes=access_token_expired_time_in_minute),
        access_token_data = JWTData(user.user_id, user.role,
                                    access_token_expired[0],
                                    subscription.expired_date,
                                    JWTData.JWT_TYPE.ACCESS)
        access_token = access_token_data.generate()
        refresh_token_expired: datetime = min(now + timedelta(days=refresh_token_expired_time_in_day),
                                    datetime(subscription.expired_date.year, subscription.expired_date.month, 
                                               subscription.expired_date.day, tzinfo=timezone.utc))
        refresh_token_data = JWTData(user.user_id, user.role, 
                                    refresh_token_expired,
                                    subscription.expired_date,
                                    JWTData.JWT_TYPE.ACCESS)
        refresh_token = refresh_token_data.generate()
        session_create_new_session(user.user_id, refresh_token, request.json['client_ip'])
        return jsonify({
            "user_id": format_id(user.user_id),
            "access_token": access_token,
            "refresh_token": refresh_token,
            "role": user.role,
            "expired_date": subscription.expired_date.strftime("%d/%m/%Y"),
            "is_premium": subscription.is_premium,
            "subscribe_tele_bot": subscription.subscribe_tele_bot
        }), RESPONSE_CODE.OK
    else:
        return jsonify({"error": "Dữ liệu không hợp lệ!"}), RESPONSE_CODE.BAD_REQUEST
    

@auth_api.route('/auth/refresh-token', methods=['GET'])
@swag_from({
    'summary': 'Refresh access token',
    'description': 'This endpoint re-new an access token with refresh token',
    'parameters': [
        SWAGGER_AUTHORIZATION_HEADER
    ],
    'responses': {
        200: {
            "description": "Refresh success",
            "type": "string"
        },
        401: SWAGGER_UNAUTHORIZE_ERROR_CODE_RESPONSE,
    }
})
@wraps_jwt_refresh_check
def refresh_token(jwt_data: JWTData):
    # refresh_token_expired = min(datetime.now(tz=timezone.utc) + timedelta(minutes=refresh_token_expired_time_in_day), 
    # 											jwt_data.subs_expired)
    access_token_expired = datetime.now(tz=timezone.utc) + \
                            timedelta(minutes=access_token_expired_time_in_minute),
    access_token_data = JWTData(jwt_data.user_id, jwt_data.role,
                                access_token_expired[0],
                                jwt_data.expired_date,
                                JWTData.JWT_TYPE.ACCESS)
    access_token = access_token_data.generate()
    return access_token, RESPONSE_CODE.OK

@auth_api.route('/auth/logout', methods=['DELETE'])
@swag_from({
    'summary': 'Logout',
    'description': 'This endpoint logout session',
    'parameters': [
        SWAGGER_AUTHORIZATION_HEADER
    ],
    'responses': {
        200: {
            "description": "Refresh success",
            "type": "string"
        },
        401: SWAGGER_UNAUTHORIZE_ERROR_CODE_RESPONSE,
    }
})
@wraps_jwt_check
def logout(jwt_data: JWTData):
    session_close_session(jwt_data.id)
    return "", 200