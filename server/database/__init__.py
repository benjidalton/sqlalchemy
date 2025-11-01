from sqlalchemy.orm import DeclarativeBase, scoped_session, sessionmaker
from sqlalchemy.orm._typing import _O
from sqlalchemy import create_engine
import os, typing
from pydantic import BaseModel
from fastapi import HTTPException

engine = create_engine(os.getenv("DATABASE_URI"), pool_size=100, pool_timeout=45, echo=True, echo_pool=True)

_O = typing.TypeVar("_O", bound=object)

class SQLAlchemy:
	
	def __init__(self, model_class):
		self.session = scoped_session(sessionmaker(bind=engine))
		self.model = model_class

	def create_entity(
		self, 
		entity: type[_O],
		dto_input: BaseModel
	):
		data = dto_input.model_dump(exclude_unset=True)
		new_entity = entity(**data)
		db.session.add(new_entity)
		return new_entity

	def get_or_404(
		self,
		entity: type[_O],
		id: typing.Any,
		not_found_msg: str | None = None,
		**kwargs: typing.Any
	):
		value = self.session.get(entity, id, **kwargs)
		if value is None:
			raise HTTPException(404, detail=not_found_msg)
		return value
	
class Base(DeclarativeBase):
	pass
	
db = SQLAlchemy(model_class=Base)