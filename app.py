### OS Import
import os
import sys

### 3rd Import
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
import argparse

### PRJ Import
import configure
import preprocessor
from src.enums import RESPONSE_CODE
from src.apis.export import cheat_api, auth_api, user_api

#############################################################################################
app = Flask(__name__)
swagger = Swagger(app)
swagger.config['title'] = f'{configure.app_name} APIs'
swagger.config['version'] = configure.app_version

if preprocessor.IS_DEV_BUILD:
	app.register_blueprint(cheat_api)
app.register_blueprint(auth_api)
app.register_blueprint(user_api)

cors = CORS(app, resources={r"/*": {"origins": configure.allow_origin_collection}})

@app.route('/', methods=['GET'])
def main_route():
	"""
		Main Route
	"""
	return f"Welcome To {configure.app_name} !!!", RESPONSE_CODE.OK

@app.route('/version', methods=['GET'])
def version():
	return configure.app_version, RESPONSE_CODE.OK

@app.route('/client-validate/<client_version>', methods=['GET'])
def client_validate(client_version: str):
	if client_version in configure.client_supported:
		return True, RESPONSE_CODE.OK
	else:
		return False, RESPONSE_CODE.OK
	
#############################################################################################
if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8080))

	parser = argparse.ArgumentParser(description='App config from command-line')
	parser.add_argument('-d','--dev', dest='debug', help='Use Local Config')
	args = parser.parse_args(sys.argv[1:])

	if preprocessor.IS_DEV_BUILD or args.dev:
		app.run(use_reloader =False, threaded=True, host='0.0.0.0', port=port, debug=True)
	else:
		from waitress import serve
		serve(app, host="0.0.0.0", port=port)