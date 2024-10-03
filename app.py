### OS Import
import os
import sys

### 3rd Import
from flask import Flask
from flask_cors import CORS
import argparse

### PRJ Import
import configure
import preprocessor

#############################################################################################
app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": configure.allow_origin_collection}})

@app.route('/', methods=['GET'])
def main_route():
	"""
		Main Route
	"""
	return f"Welcome To {configure.app_name} !!!", 200

@app.route('/version', methods=['GET'])
def version():
	return configure.app_version, 200

@app.route('/client-validate/<client_version>')
def client_validate(client_version: str):
	if client_version in configure.client_supported:
		return True, 200
	else:
		return False, 200
	
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