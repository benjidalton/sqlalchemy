from typing import Dict, Any
# ------ custom imports ----- +
from schemas import CreateUserSchema
from models.all_models import User
from database import db
from services import modifying

@modifying
def create_user(dto_input: CreateUserSchema) -> Dict[str, Any]:

	user: User = db.create_entity(User, dto_input)

	return { "user": user.to_json() }

def get_user_by_id(user_id: int) -> Dict[str, Any]:
	
	user: User = db.get_or_404(User, user_id, f"User not found matching this ID: {user_id}")

	return { "user": user.to_json() }