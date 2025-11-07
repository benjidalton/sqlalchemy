from fastapi import Query, Request
from datetime import datetime
import re, json, os
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
		
		@self.route("/fetch/run/{run_id}", HTTPMethod.GET.value)
		def get_run_by_id(run_id: int):
			return MegaBonkService.get_run_by_id(run_id=run_id)
		
		@self.route("/runs", HTTPMethod.GET.value)
		def get_paginated_runs(page: int = 1, per_page: int = 10):
			return MegaBonkService.get_paginated_runs(page, per_page)
		
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

		@self.route("/submit/last", HTTPMethod.POST.value)
		def submit_last_run():
			base_dir = os.path.dirname(os.path.abspath(__file__))

    		# Go up one level to project root, then point to last_run.json
			file_path = os.path.join(base_dir, "..", "last_run.json")

			# Normalize it (removes .. and converts slashes)
			file_path = os.path.normpath(file_path)

			# Load JSON data
			with open(file_path, "r", encoding="utf-8") as file:
				data = json.load(file)
			MegaBonkService.submit_run(data)


megabonk_controller = MegaBonkController()
megabonk_router = megabonk_controller.router