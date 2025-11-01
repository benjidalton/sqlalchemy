from pydantic import BaseModel, ConfigDict, StringConstraints
from typing import Annotated, Optional
# ----- custom imports ----- +
from models import snake_to_camel

class SchemaBase(BaseModel):
	model_config = ConfigDict(
		alias_generator=snake_to_camel,
		populate_by_name=True # allows used of snake_case or camelCase
	)

class CreateUserSchema(SchemaBase):
	name: Annotated[str, StringConstraints(max_length=50)] = None