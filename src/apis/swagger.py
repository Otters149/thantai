SWAGGER_AUTHORIZATION_HEADER = {
        "name": "Authorization",
        "in": "header",
        "type": "string",
        "required": True,
        "description": 'Bearer token to access the protected route.'
    }

SWAGGER_UNAUTHORIZE_ERROR_CODE_RESPONSE = {
		"description": "Unauthorization",
		"schema": {
			"type": "object",
			"properties": {
				"error": {
					"type": "string"
				}
			}
		}
	}

SWAGGER_INTERNAL_SERVER_ERROR_CODE_RESPONSE = {
		"description": "Internal Server Error",
		"schema": {
			"type": "object",
			"properties": {
				"error": {
					"type": "string"
				}
			}
		}
	}