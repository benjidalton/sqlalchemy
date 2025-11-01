from controllers import BaseController
from enums import HTTPMethod
from services import user_service as US
from schemas import CreateUserSchema

class UserController(BaseController):
	def __init__(self):
		super().__init__(prefix="/users", tags=["Users"])

		
		@self.route("/create", HTTPMethod.POST.value)
		def create_user(body: CreateUserSchema):
			return US.create_user(body)
		
		# @self.route("/", HTTPMethod.GET.value)
		# def list_users():
		#     return US.get_user
		
		@self.route("/{user_id}", HTTPMethod.GET.value)
		def get_user(user_id: int):
			return US.get_user_by_id(user_id)

user_controller = UserController()
user_router = user_controller.router