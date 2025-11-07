from fastapi import Query, Request
from datetime import datetime
import re, json
from pathlib import Path
from typing import Any
# ----- custom imports ----- +
from controllers import BaseController
from enums import HTTPMethod
from services.megabonk_service import MegaBonkService
from schemas import CreateRunSchema

def to_snake_case(name: str) -> str:
	"""Convert a string (camelCase, PascalCase, etc.) to snake_case."""
	s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
	return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

def keys_to_snake_case(obj: Any) -> Any:
	"""Recursively convert all dict keys in a JSON-like object to snake_case."""
	if isinstance(obj, dict):
		new_dict = {}
		for k, v in obj.items():
			new_key = to_snake_case(k)
			new_dict[new_key] = keys_to_snake_case(v)
		return new_dict
	elif isinstance(obj, list):
		return [keys_to_snake_case(i) for i in obj]
	else:
		return obj


class MegaBonkController(BaseController):
	def __init__(self):
		super().__init__(prefix="/megabonk", tags=["Megabonk"])
		
		@self.route("/static", HTTPMethod.GET.value)
		def get_static_data():
			return MegaBonkService.get_static_data()
		
		@self.route("/winrates", HTTPMethod.GET.value)
		def get_win_rates(
			character_ids: list[int] | None = Query(default=None, description="Filter by character IDs"),
			weapon_ids: list[int] | None = Query(default=None, description="Filter by weapon IDs"),
			tome_ids: list[int] | None = Query(default=None, description="Filter by tome IDs"),
			item_ids: list[int] | None = Query(default=None, description="Filter by item IDs"),
			start_date: datetime | None = Query(default=None, description="Filter runs after this date"),
			end_date: datetime | None = Query(default=None, description="Filter runs before this date"),
			sort_desc: bool = Query(default=True, description="Sort by win rate descending (default true)")
		):
			filters = {
				"character_ids": character_ids,
				"weapon_ids": weapon_ids,
				"tome_ids": tome_ids,
				"item_ids": item_ids,
				"start_date": start_date,
				"end_date": end_date,
			}
			return MegaBonkService.get_win_rates(filters=filters, sort_desc=sort_desc)

		@self.route("/submit", HTTPMethod.POST.value)
		async def upload(request: Request):
			raw = await request.body()

			# Parse and convert
			data = json.loads(raw.decode())
			snake_data = keys_to_snake_case(data)
			output_path = Path("last_run.json")

			with output_path.open("w", encoding="utf-8") as f:
				json.dump(snake_data, f, indent=4, ensure_ascii=False)
				  
			MegaBonkService.submit_run(snake_data)

			
			return {"status": "ok"}

		@self.route("/submit", HTTPMethod.POST.value)
		def submit():
			data ={
    "run_id": "2706b0ef-570a-4bfd-8483-353107b3216d",
    "timestamp": "2025-11-07T18:04:05.2858533Z",
    "character": "Calcium",
    "map": "UnknownMap",
    "win": 'false',
    "total_damage": 416.9937,
    "enemies_killed": 0,
    "level_reached": 0,
    "items": {},
    "weapons": {
        "bone": 1,
        "shotgun": 1
    },
    "tomes": {},
    "stats": {
        "silver_increase_multiplier": [
            {
                "type": "Addition",
                "amount": 0.11
            },
            {
                "type": "Addition",
                "amount": 0.5
            }
        ],
        "jump_height": [
            {
                "type": "Addition",
                "amount": 0.1
            }
        ]
    },
    "damage_by_source": {
        "bone": 349.00504,
        "shotgun": 67.98865
    },
    "run_stats": {
        "projectiles_fired": 39,
        "kills": 28,
        "mummy_kills": 28,
        "bone_kills": 25,
        "standing_still_kills": 7,
        "calcium_kills": 28,
        "gold_earned": 26,
        "xp_gained": 9,
        "shrine_charge": 1,
        "crits": 5,
        "shotgun_kills": 3,
        "runs": 1
    }
}
			MegaBonkService.submit_run(data)


megabonk_controller = MegaBonkController()
megabonk_router = megabonk_controller.router