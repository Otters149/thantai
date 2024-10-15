from datetime import datetime, date
from src.utils import jwt_gen

class JWTData:
	class JWT_TYPE:
		ACCESS = "access_token"
		REFRESH = "refresh_token"

	def __init__(self, id: str, role: str, expired: datetime, subs_expired: datetime, type: str) -> None:
		self.id = id
		self.role = role
		self.token_expired = expired
		self.subs_expired= subs_expired
		self.type = type

	@classmethod
	def from_data(cls, data):
		return cls( data['id'],
			 		data['role'],
					data['exp'],
					data['subs_exp'],
					data['payload'])

	def generate(self) -> str:
		return jwt_gen(self.id, self.role, self.token_expired, (self.subs_expired - date(1970, 1, 1)).days * 24*60*60, self.type)