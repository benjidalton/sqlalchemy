from fastapi import Query
from datetime import datetime
from controllers import BaseController
from enums import HTTPMethod
from services.megabonk_service import MegaBonkService
from schemas import CreateRunSchema

class MegaBonkController(BaseController):
	def __init__(self):
		super().__init__(prefix="/megabonk", tags=["Megabonk"])

		
		@self.route("/create", HTTPMethod.POST.value)
		def create_run(body: CreateRunSchema):
			return MegaBonkService.create_run(body)
		
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

	

megabonk_controller = MegaBonkController()
megabonk_router = megabonk_controller.router