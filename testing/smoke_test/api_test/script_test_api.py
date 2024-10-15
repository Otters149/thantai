import requests
from datetime import datetime

BASE_URL = "http://localhost:8080/"
HEADERS = {
    'content-type': 'application/json',
}
PARAMS = (
    ('priority', 'normal'),
)

def check_server() -> bool:
	res = requests.get(BASE_URL)
	return res.status_code == 200

def count_user(access_token: str) -> int:
	url = BASE_URL + f"user/count/activate"
	headers = {
		'content-type': 'application/json',
		'Carrier': access_token
	}
	res = requests.get(url, headers=headers)
	if res.status_code == 200:
		return int(res.text)
	return 0

def get_rsa_encode(input: str) -> str:
	url = BASE_URL + f"cheat/encode/{input}"
	res = requests.get(url)
	if res.status_code == 200:
		return res.json()["payload"].replace("b'", "").replace("'", "")
	return None

def create_user_test(admin_token: str, username: str, password: str, is_premium: bool, is_subs_tele_bot: bool, expired_date: datetime):
	url = BASE_URL + "user/create"
	json = {
		"username": username,
		"password": password,
		"role": "User",
		"display_name": username.upper(),
		"note": "",
		"is_premium": is_premium,
		"is_subs_tele_bot": is_subs_tele_bot,
		"expired_date": expired_date.strftime('%d/%m/%Y')
	}
	headers = {
		'content-type': 'application/json',
		'Carrier': admin_token
	}	
	res = requests.post(url, json=json, headers=headers, params=PARAMS)
	if res.status_code == 201:
		return res.text
	return None

def cheat_create_admin() -> bool:
	url = BASE_URL + "/cheat/create-admin"
	res = requests.post(url, headers=HEADERS, params=PARAMS)
	return res.status_code == 201

def authen_test(username: str, password: str) -> tuple[str, str]:
	'''
		Return:
			str: access token
			str: refresh token
	'''
	url = BASE_URL + "auth/login"
	json = {
		"username": username,
		"password": password,
		"client_ip": "192.168.1.1"
	}
	res = requests.post(url, json=json, headers=HEADERS, params=PARAMS)
	if res.status_code == 200:
		res_json = res.json()
		return res_json['access_token'], res_json['refresh_token']
	return "", ""

def test_flow():
	if not check_server():
		print("Server not started!")
		return
	if not cheat_create_admin():
		print("Create admin failed!")
		return
	hash_pwd = get_rsa_encode("1")
	if hash_pwd != None:
		print(f"[HASH_PWD] {hash_pwd}")
		access_token, refresh_token = authen_test('admin', hash_pwd)
		print(f"[ADMIN_ACCESS_TOKEN] {access_token}")
		print(f"[ADMIN_REFRESH_TOKEN] {refresh_token}")
		if access_token != "":
			for i in range(30):
				user_id = create_user_test(access_token, f"test{i}", hash_pwd, False, False, datetime(2024, 12, 1))
		count = count_user(access_token)
		print(f"[ACTIVATE_USERS] {count}")
if __name__ == '__main__':
	test_flow()
