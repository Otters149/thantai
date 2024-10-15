from src.apis.api_hepler import *
from src.utils import rsa_gen_keypem, rsa_encode, rsa_decode, md5_get_hash, format_id
from src.models.export import User, UserInfo, Subscription
from src.entities.export import user_create_user, user_check_user_existing_by_username
cheat_api = Blueprint('cheat_api', __name__)

@cheat_api.route('/cheat/generate-keypem', methods=['GET'])
@swag_from({
    'summary': 'Generate keypem',
    'description': 'This endpoint generate private and public keypem, use for rsa encode and decode',
    'responses': {
        200: {
            "description": "Generate success",
            "schema": {
				"type": "object",
				"properties": {
					"publicPEM": { "type": "string"},
					"privatePEM": { "type": "string"}
				}
            }
        },
    }
})
def generate_keypem():
	public_keypem, private_keypem = rsa_gen_keypem()

	return jsonify({"publicPEM": public_keypem, "privatePEM": private_keypem}), 200

@cheat_api.route('/cheat/encode/<input>', methods=['GET'])
@swag_from({
    'summary': 'Encode text',
    'description': 'This endpoint rsa-encode input',
	'parameters':[
		{
			"name": "input",
			"description": "Input text will be encoded",
			"type": "string",
			"required": True,
			"in": "path"
		},
	],
    'responses': {
        200: {
            "description": "Encode success",
            "schema": {
				"type": "object",
				"properties": {
					"payload": { "type": "string"}
				}
            }
        },
    }
})
def encode(input):
	return jsonify({"payload": rsa_encode(input)}), 200

@cheat_api.route('/cheat/decode/<input>', methods=['GET'])
@swag_from({
    'summary': 'Decode text',
    'description': 'This endpoint rsa-decode input',
	'parameters':[
		{
			"name": "input",
			"description": "Input text will be decoded",
			"type": "string",
			"required": True,
			"in": "path"
		},
	],
    'responses': {
        200: {
            "description": "Decode success",
            "schema": {
				"type": "object",
				"properties": {
					"payload": { "type": "string"}
				}
            }
        },
    }
})
def decode():
	return jsonify({"payload": rsa_decode(input)}), 200

@cheat_api.route('/cheat/create-admin', methods=['POST'])
@swag_from({
    'summary': 'Create admin',
    'description': 'This endpoint create an admin account with password = 1',
    'responses': {
        200: {
            "description": "Create success",
            "type": "string"
        },
		500: {
			"description": "Create error",
            "schema": {
				"type": "object",
				"properties": {
					"error": {
						"type": "string"
					}
				}
            }
		}
    }
})
def create_admin():
	user = User("0000", "admin", md5_get_hash("1"), ROLE.Admin.name, False, False)
	user_info = UserInfo(user.user_id, "Administrator", False, datetime.now(), "")
	subscription = Subscription(user.user_id, True, True, datetime.now() + timedelta(hours=24*30*100))
	if user_check_user_existing_by_username(user.username):
		return jsonify({"error":"Username has taken!"}), RESPONSE_CODE.BAD_REQUEST
	success, user, user_info, subscription = user_create_user(user, user_info, subscription)
	if success:
		return format_id(user.user_id), RESPONSE_CODE.CREATED
	else:
		return jsonify({"error":"Internal Server Error!"}), RESPONSE_CODE.INTERNAL_SERVER_ERROR