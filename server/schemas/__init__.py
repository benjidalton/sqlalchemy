from pydantic import BaseModel, ConfigDict, StringConstraints, conint
from typing import Annotated, Optional, List
from datetime import datetime
# ----- custom imports ----- +
from models import snake_to_camel

class SchemaBase(BaseModel):
	model_config = ConfigDict(
		alias_generator=snake_to_camel,
		populate_by_name=True # allows used of snake_case or camelCase
	)

class CreateUserSchema(SchemaBase):
	name: Annotated[str, StringConstraints(max_length=50)] = None
	

class RunWeaponSchema(SchemaBase):
	weapon_id: int
	quantity: Annotated[int, conint(ge=1)] = 1


class RunTomeSchema(SchemaBase):
	tome_id: int
	quantity: Annotated[int, conint(ge=1)] = 1


class RunItemSchema(SchemaBase):
	item_id: int
	quantity: Annotated[int, conint(ge=1)] = 1
	
# ===============================
# Create Run Schema
# ===============================

class CreateRunSchema(SchemaBase):
	character_id: int
	duration_minutes: Optional[int] = None
	score: Optional[int] = None
	won: bool = False
	notes: Optional[str] = None
	weapons: Optional[List[RunWeaponSchema]] = []
	tomes: Optional[List[RunTomeSchema]] = []
	items: Optional[List[RunItemSchema]] = []


# ===============================
# Response Schemas
# ===============================

class RunSchema(SchemaBase):
	id: int
	character_id: int
	date_played: datetime
	duration_minutes: Optional[int]
	score: Optional[int]
	won: bool
	notes: Optional[str]

	weapons: Optional[List[RunWeaponSchema]] = []
	tomes: Optional[List[RunTomeSchema]] = []
	items: Optional[List[RunItemSchema]] = []
