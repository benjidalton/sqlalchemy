from typing import Dict, Any, List
from datetime import datetime
from sqlalchemy import func, case
from pydantic import BaseModel
# ------ custom imports ----- +
from schemas import *
from database import db
from services import modifying
from models.megabonk import *

class IGNameDTO(BaseModel):
    game_ref: str

class MegaBonkService:

	@staticmethod
	def submit_run(data):
		char = db.session.query(Character).filter_by(game_ref=data["character"]).first()
		if not char:
			char = Character(game_ref=data["character"], label=data["character"])
			db.session.add(char)
			db.session.flush()

		# --- 2. Create Run ---
		run = Run(
			character_id=char.id,
			duration_minutes=None,
			won=False
		)
		db.session.add(run)
		db.session.flush()

		# --- 3. Handle junctions dynamically --
		# --- Items ---
		for game_ref, qty in data.get("items", {}).items():
			item = db.get_or_create(Item, game_ref)
			db.session.add(RunItem(run_id=run.id, item_id=item.id, quantity=qty))

		# --- Weapons ---
		for game_ref, qty in data.get("weapons", {}).items():
			weapon = db.get_or_create(Weapon, game_ref)
			db.session.add(RunWeapon(run_id=run.id, weapon_id=weapon.id, quantity=qty))

		# --- Tomes ---
		for game_ref, qty in data.get("tomes", {}).items():
			tome = db.get_or_create(Tome, game_ref)
			db.session.add(RunTome(run_id=run.id, tome_id=tome.id, quantity=qty))

		# --- Run Stats ---
		for stat_name, value in data.get("run_stats", {}).items():
			stat = db.get_or_create(Stat, stat_name)
			db.session.add(RunStat(run_id=run.id, stat_id=stat.id))

		for damage_source, amount in data.get("damage_by_source", {}).items():
			damage_source = db.get_or_create(DamageSource, damage_source)
			db.session.add(RunDamageSource(run_id=run.id, damage_source_id=damage_source.id, amount=amount))

		db.session.commit()


	@staticmethod
	def get_static_data():
		characters = db.session.query(Character).all()
		weapons = db.session.query(Weapon).all()
		tomes = db.session.query(Tome).all()
		items = db.session.query(Item).all()
		
		return {
			"characters": characters,
			"weapons": weapons,
			"tomes": tomes,
			"items": items
		}
	
	@staticmethod
	def get_win_rates(filters: dict | None = None, sort_desc: bool = True):
		"""
		Get win rates for each character, weapon, tome, and item.
		Optionally filter by character_id, weapon_id, tome_id, item_id.
		"""
		filters = filters or {}

		results = {
			"characters": MegaBonkService._get_character_win_rates(filters, sort_desc),
			"weapons": MegaBonkService._get_weapon_win_rates(filters, sort_desc),
			"tomes": MegaBonkService._get_tome_win_rates(filters, sort_desc),
			"items": MegaBonkService._get_item_win_rates(filters, sort_desc),
		}

		return results

	# =====================================================
	# Characters
	# =====================================================
	@staticmethod
	def _get_character_win_rates(filters: dict, sort_desc: bool):
		query = (
			db.session.query(
				Character.id,
				Character.name,
				Character.img_source,
				func.count(Run.id).label("total_runs"),
				func.sum(case((Run.won == True, 1), else_=0)).label("wins"),
				(func.sum(case((Run.won == True, 1), else_=0)) / func.count(Run.id) * 100).label("win_rate"),
			)
			.join(Run, Run.character_id == Character.id)
			.group_by(Character.id)
		)

		if filters.get("weapon_id"):
			query = query.join(RunWeapon).filter(RunWeapon.weapon_id == filters["weapon_id"])
		if filters.get("tome_id"):
			query = query.join(RunTome).filter(RunTome.tome_id == filters["tome_id"])
		if filters.get("item_id"):
			query = query.join(RunItem).filter(RunItem.item_id == filters["item_id"])

		query = query.order_by(func.coalesce("win_rate", 0).desc() if sort_desc else func.coalesce("win_rate", 0))
		return [dict(r._asdict()) for r in query.all()]

	# =====================================================
	# Weapons
	# =====================================================
	@staticmethod
	def _get_weapon_win_rates(filters: dict, sort_desc: bool):
		query = (
			db.session.query(
				Weapon.id,
				Weapon.name,
				Weapon.img_source,
				func.count(Run.id).label("total_runs"),
				func.sum(case((Run.won == True, 1), else_=0)).label("wins"),
				(func.sum(case((Run.won == True, 1), else_=0)) / func.count(Run.id) * 100).label("win_rate"),
			)
			.join(RunWeapon, RunWeapon.weapon_id == Weapon.id)
			.join(Run, Run.id == RunWeapon.run_id)
			.group_by(Weapon.id)
		)

		if filters.get("character_id"):
			query = query.filter(Run.character_id == filters["character_id"])
		if filters.get("tome_id"):
			query = query.join(RunTome).filter(RunTome.tome_id == filters["tome_id"])
		if filters.get("item_id"):
			query = query.join(RunItem).filter(RunItem.item_id == filters["item_id"])

		query = query.order_by(func.coalesce("win_rate", 0).desc() if sort_desc else func.coalesce("win_rate", 0))
		return [dict(r._asdict()) for r in query.all()]

	# =====================================================
	# Tomes
	# =====================================================
	@staticmethod
	def _get_tome_win_rates(filters: dict, sort_desc: bool):
		query = (
			db.session.query(
				Tome.id,
				Tome.name,
				Tome.img_source,
				func.count(Run.id).label("total_runs"),
				func.sum(case((Run.won == True, 1), else_=0)).label("wins"),
				(func.sum(case((Run.won == True, 1), else_=0)) / func.count(Run.id) * 100).label("win_rate"),
			)
			.join(RunTome, RunTome.tome_id == Tome.id)
			.join(Run, Run.id == RunTome.run_id)
			.group_by(Tome.id)
		)

		if filters.get("character_id"):
			query = query.filter(Run.character_id == filters["character_id"])
		if filters.get("weapon_id"):
			query = query.join(RunWeapon).filter(RunWeapon.weapon_id == filters["weapon_id"])
		if filters.get("item_id"):
			query = query.join(RunItem).filter(RunItem.item_id == filters["item_id"])

		query = query.order_by(func.coalesce("win_rate", 0).desc() if sort_desc else func.coalesce("win_rate", 0))
		return [dict(r._asdict()) for r in query.all()]

	# =====================================================
	# Items
	# =====================================================
	@staticmethod
	def _get_item_win_rates(filters: dict, sort_desc: bool):
		query = (
			db.session.query(
				Item.id,
				Item.name,
				Item.img_source,
				func.count(Run.id).label("total_runs"),
				func.sum(case((Run.won == True, 1), else_=0)).label("wins"),
				(func.sum(case((Run.won == True, 1), else_=0)) / func.count(Run.id) * 100).label("win_rate"),
			)
			.join(RunItem, RunItem.item_id == Item.id)
			.join(Run, Run.id == RunItem.run_id)
			.group_by(Item.id)
		)

		if filters.get("character_id"):
			query = query.filter(Run.character_id == filters["character_id"])
		if filters.get("weapon_id"):
			query = query.join(RunWeapon).filter(RunWeapon.weapon_id == filters["weapon_id"])
		if filters.get("tome_id"):
			query = query.join(RunTome).filter(RunTome.tome_id == filters["tome_id"])

		query = query.order_by(func.coalesce("win_rate", 0).desc() if sort_desc else func.coalesce("win_rate", 0))
		return [dict(r._asdict()) for r in query.all()]