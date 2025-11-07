from fastapi import HTTPException
from sqlalchemy import func, case, select
from sqlalchemy.orm import joinedload
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
	def get_run_by_id(run_id: int):
		run = (
			db.session.query(Run)
			.filter(Run.id == run_id)
			.first()
		)

		if not run:
			raise HTTPException(status_code=404, detail=f"Run with id {run_id} not found")

		# Assemble full run data
		run_data = {
			"id": run.id,
			"character": run.character.to_json(),
			"date_played": run.date_played.isoformat(),
			"duration_minutes": run.duration_minutes,
			"won": run.won,
			"notes": run.notes,
			"weapons": [
				{
					"weapon": rw.weapon.to_json(),
					"quantity": rw.quantity
				}
				for rw in run.weapons
			],
			"items": [
				{
					"item": ri.item.to_json(),
					"quantity": ri.quantity
				}
				for ri in run.items
			],
			"tomes": [
				{
					"tome": rt.tome.to_json(),
					"quantity": rt.quantity
				}
				for rt in run.tomes
			],
			"stats": [
				{
					"stat": rs.stat.to_json(),
					"amount": rs.amount
				}
				for rs in run.stats
			],
			"damage_sources": [
				{
					"damage_source": rd.damage_source.to_json(),
					"amount": float(rd.amount)
				}
				for rd in run.damage_sources
			]
		}

		return run_data

	@staticmethod
	def get_paginated_runs(page: int = 1, per_page: int = 10):
		offset = (page - 1) * per_page

		# Query only base Run + weapons + tomes (no stats/items/damage_sources)
		runs = (
			db.session.query(Run)
			.options(
				joinedload(Run.character),
				joinedload(Run.weapons).joinedload(RunWeapon.weapon),
				joinedload(Run.tomes).joinedload(RunTome.tome),
			)
			.order_by(Run.date_played.desc())
			.limit(per_page)
			.offset(offset)
			.all()
		)

		if not runs:
			raise HTTPException(status_code=404, detail="No runs found")

		# Build response data
		results = []
		for run in runs:
			results.append({
				"id": run.id,
				"character": run.character.to_json(),
				"date_played": run.date_played.isoformat(),
				"duration_minutes": run.duration_minutes,
				"won": run.won,
				"notes": run.notes,
				"weapons": [
					{
						"weapon": rw.weapon.to_json(),
						"quantity": rw.quantity
					}
					for rw in run.weapons
				],
				"tomes": [
					{
						"tome": rt.tome.to_json(),
						"quantity": rt.quantity
					}
					for rt in run.tomes
				]
			})

		# Optional total count
		total_count = db.session.query(Run).count()

		return {
			"page": page,
			"per_page": per_page,
			"total": total_count,
			"results": results
		}

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
			db.session.add(RunStat(run_id=run.id, stat_id=stat.id, amount=value))

		stats = data.get("stats", {})
		merged_stats = {}

		for stat_name, modifiers in stats.items():
			type_sums = {}
			for m in modifiers:
				mtype = m["type"]
				type_sums[mtype] = type_sums.get(mtype, 0) + m["amount"]

			# Replace list with summed version
			merged_stats[stat_name] = [{"type": t, "amount": amt} for t, amt in type_sums.items()]

		# Now merged_stats looks like:
		# "extra_jumps": [{"type": "Flat", "amount": 2}]
		# "luck": [{"type": "Flat", "amount": 0.11}], etc.

		# --- Run Stats ---
		for stat_name, modifiers in merged_stats.items():
			stat = db.get_or_create(Stat, stat_name)
			for mod in modifiers:
				db.session.add(RunStat(
					run_id=run.id,
					stat_id=stat.id,
					amount=mod["amount"]
				))

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
				Character.label,
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
				Weapon.label,
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
				Tome.label,
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
				Item.label,
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