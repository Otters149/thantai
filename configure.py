app_name = "NongTrai"
app_version = "1.0.0"

client_supported = ["1.0.0"]

allow_origin_collection = ["http://localhost:8080", 
						   "https://daovang-df31a.web.app", 
						   "https://daovang-df31a.firebaseapp.com", 
						   "http://daovang.online", 
						   "https://daovang.online", 
						   "https://daovang.net", 
						   "https://www.daovang.net"]


access_token_expired_time_in_minute = 0.2
refresh_token_expired_time_in_day = 2
rsa_private_key_pem = ""
rsa_public_key_pem = ""

time_to_get_lottery_result = [
	(18, 38),	# North: 18h38
	(17, 38),	# Mid: 17h38
	(16, 38)	# South 17h38
]

use_database = "MYSQL"
local_mysql_config = {
  'user': 'root',
  'password': '',
  'host': '127.0.0.1',
  'port': '3306',
  'database': 'nongtrai'
}