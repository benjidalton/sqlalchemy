from fastapi import APIRouter

class BaseController:
	def __init__(self, prefix: str, tags: list[str]):
		self.router = APIRouter(prefix=prefix, tags=tags)

	def route(self, path: str, method: str):
		def decorator(func):
			self.router.add_api_route(
				path, 
				func, 
				methods=[method]
			)
			return func
		return decorator