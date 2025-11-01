from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.mysql import INTEGER

from models import BaseJsonSerializable
from database import db

class User(db.model, BaseJsonSerializable):

	__tablename__="user"

	id: Mapped[int] = mapped_column(INTEGER(10), primary_key=True, autoincrement=True)
	name: Mapped[str] = mapped_column(String(50), nullable=False)