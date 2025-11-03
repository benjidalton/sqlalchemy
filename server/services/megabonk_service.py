from typing import Dict, Any, List
from datetime import datetime
from sqlalchemy import func, case
# ------ custom imports ----- +
from schemas import CreateRunSchema
from database import db
from services import modifying
from models.megabonk import *

class MegaBonkService:

	@modifying
	@staticmethod
	def create_run(run_data: CreateRunSchema) -> Dict[str, Any]:
		# --- 1️⃣ Create the run record ---
		new_run = Run(
			character_id=run_data.character_id,
			date_played=datetime.now(),
			duration_minutes=run_data.duration_minutes,
			score=run_data.score,
			won=run_data.won,
			notes=run_data.notes,
		)

		db.session.add(new_run)
		db.session.flush()  # ensures new_run.id is available

		# --- 2️⃣ Weapons ---
		if run_data.weapons:
			for weapon in run_data.weapons:
				# If weapon_id not provided, fall back to name
				if getattr(weapon, "weapon_id", None):
					weapon_obj = db.session.get(Weapon, weapon.weapon_id)
				else:
					weapon_obj = db.get_or_create(Weapon, name=weapon.name)

				run_weapon = RunWeapon(
					run_id=new_run.id,
					weapon_id=weapon_obj.id,
					quantity=weapon.quantity,
				)
				db.session.add(run_weapon)

		# --- 3️⃣ Tomes ---
		if run_data.tomes:
			for tome in run_data.tomes:
				if getattr(tome, "tome_id", None):
					tome_obj = db.session.get(Tome, tome.tome_id)
				else:
					tome_obj = db.get_or_create(Tome, name=tome.name)

				run_tome = RunTome(
					run_id=new_run.id,
					tome_id=tome_obj.id,
					quantity=tome.quantity
				)
				db.session.add(run_tome)

		# --- 4️⃣ Items ---
		if run_data.items:
			for item in run_data.items:
				if getattr(item, "item_id", None):
					item_obj = db.session.get(Item, item.item_id)
				else:
					item_obj = db.get_or_create(Item, name=item.name)

				run_item = RunItem(
					run_id=new_run.id,
					item_id=item_obj.id,
					quantity=item.quantity,
				)
				db.session.add(run_item)

		db.session.commit()
		db.session.refresh(new_run)

		return {"run": new_run}

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