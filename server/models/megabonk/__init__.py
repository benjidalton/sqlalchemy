from __future__ import annotations  # 👈 ADD THIS at the very top!

from sqlalchemy import (
	SmallInteger,
	Integer,
	String,
	Boolean,
	DateTime,
	Text,
	ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from database import db 
from models import BaseJsonSerializable


# =====================================================
# Run
# =====================================================
class Run(db.model, BaseJsonSerializable):
	__tablename__ = "run"

	id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
	character_id: Mapped[int] = mapped_column(ForeignKey("character.id"), nullable=False)
	date_played: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
	duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
	score: Mapped[int | None] = mapped_column(Integer, nullable=True)
	won: Mapped[bool] = mapped_column(Boolean, default=False)
	notes: Mapped[str | None] = mapped_column(Text, nullable=True)

	character: Mapped["Character"] = relationship("Character", back_populates="runs")
	weapons: Mapped[list["RunWeapon"]] = relationship("RunWeapon", back_populates="run")
	items: Mapped[list["RunItem"]] = relationship("RunItem", back_populates="run")
	tomes: Mapped[list["RunTome"]] = relationship("RunTome", back_populates="run")


# =====================================================
# Character
# =====================================================
class Character(db.model, BaseJsonSerializable):
	__tablename__ = "character"

	id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
	name: Mapped[str] = mapped_column(String(25), nullable=False)
	img_source: Mapped[str] = mapped_column(String(255), nullable=False)
	default_weapon_id: Mapped[int] = mapped_column(ForeignKey("weapon.id"), nullable=False)

	runs: Mapped[list["Run"]] = relationship("Run", back_populates="character")


# =====================================================
# Weapon
# =====================================================
class Weapon(db.model, BaseJsonSerializable):
	__tablename__ = "weapon"

	id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
	name: Mapped[str] = mapped_column(String(50), nullable=False)
	img_source: Mapped[str] = mapped_column(String(255), nullable=False)

	runs: Mapped[list["RunWeapon"]] = relationship("RunWeapon", back_populates="weapon")


# =====================================================
# Tome
# =====================================================
class Tome(db.model, BaseJsonSerializable):
	__tablename__ = "tome"

	id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
	name: Mapped[str] = mapped_column(String(50), nullable=False)
	img_source: Mapped[str] = mapped_column(String(255), nullable=False)

	runs: Mapped[list["RunTome"]] = relationship("RunTome", back_populates="tome")


# =====================================================
# Item
# =====================================================
class Item(db.model, BaseJsonSerializable):
	__tablename__ = "item"

	id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
	name: Mapped[str] = mapped_column(String(50), nullable=False)
	img_source: Mapped[str] = mapped_column(String(255), nullable=False)

	runs: Mapped[list["RunItem"]] = relationship("RunItem", back_populates="item")


# =====================================================
# RunWeapon (junction)
# =====================================================
class RunWeapon(db.model, BaseJsonSerializable):
	__tablename__ = "run_weapon"

	run_id: Mapped[int] = mapped_column(ForeignKey("run.id"), primary_key=True)
	weapon_id: Mapped[int] = mapped_column(ForeignKey("weapon.id"), primary_key=True)
	quantity: Mapped[int] = mapped_column(Integer, default=1)

	run: Mapped["Run"] = relationship("Run", back_populates="weapons")
	weapon: Mapped["Weapon"] = relationship("Weapon", back_populates="runs")


# =====================================================
# RunItem (junction)
# =====================================================
class RunItem(db.model, BaseJsonSerializable):
	__tablename__ = "run_item"

	run_id: Mapped[int] = mapped_column(ForeignKey("run.id"), primary_key=True)
	item_id: Mapped[int] = mapped_column(ForeignKey("item.id"), primary_key=True)
	quantity: Mapped[int] = mapped_column(Integer, default=1)

	run: Mapped["Run"] = relationship("Run", back_populates="items")
	item: Mapped["Item"] = relationship("Item", back_populates="runs")


# =====================================================
# RunTome (junction)
# =====================================================
class RunTome(db.model, BaseJsonSerializable):
	__tablename__ = "run_tome"

	run_id: Mapped[int] = mapped_column(ForeignKey("run.id"), primary_key=True)
	tome_id: Mapped[int] = mapped_column(ForeignKey("tome.id"), primary_key=True)
	quantity: Mapped[int] = mapped_column(Integer, default=1)

	run: Mapped["Run"] = relationship("Run", back_populates="tomes")
	tome: Mapped["Tome"] = relationship("Tome", back_populates="runs")