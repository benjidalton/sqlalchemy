<template>
	<v-card
		class="d-flex flex-column pa-4 h-100"
		elevation="3"
		:style="{ backgroundColor: theme.current.value.colors.background }"
	>
		<h3 class="mb-4">Recent Runs</h3>

		<div class="run-table">
			<div class="table-header">
				<div class="col col-character">Character</div>
				<div class="col col-weapons">Weapons</div>
				<div class="col col-tomes">Tomes</div>
			</div>

			<div class="table-body">
				<div
					v-for="run in runs"
					:key="run.id"
					class="table-row"
					:class="{ win: run.won, loss: !run.won }"
					@click="onRowClick(run.id)"
				>
					<!-- Character -->
					<div class="col col-character d-flex align-center">
						<v-avatar size="32" >
							<v-img :src="AssetsAPI.getImageUrl(run.character.imgSource)" alt="char" />
						</v-avatar>
						<span class="truncate">{{ run.character.label }}</span>
					</div>

					<!-- Weapons -->
					<div class="col col-weapons d-flex flex-wrap align-center">
						<v-tooltip
							v-for="(w, i) in run.weapons"
							:key="i"
							location="top"
						>
							<template #activator="{ props }">
								<v-avatar
									v-bind="props"
									size="28"
									class="mr-1"
									style="border: 1px solid rgba(255,255,255,0.15)"
								>
									<v-img :src="AssetsAPI.getImageUrl(w.weapon.imgSource)" />
								</v-avatar>
							</template>
							<span>{{ w.weapon.label }} ×{{ w.quantity }}</span>
						</v-tooltip>
					</div>

					<!-- Tomes -->
					<div class="col col-tomes d-flex flex-wrap align-center">
						<template v-if="run.tomes.length">
							<v-tooltip
								v-for="(t, i) in run.tomes"
								:key="i"
								location="top"
							>
								<template #activator="{ props }">
									<v-avatar
										v-bind="props"
										size="24"
										class="mr-1"
										color="primary"
									>
										<v-icon size="16">mdi-book-open-variant</v-icon>
									</v-avatar>
								</template>
								<span>{{ t.tome.label }} ×{{ t.quantity }}</span>
							</v-tooltip>
						</template>
						<span v-else class="text-disabled">–</span>
					</div>
				</div>
			</div>
		</div>
	</v-card>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useTheme } from "vuetify";
import { MegaBonkAPI } from "@/api/megabonk";
import { AssetsAPI } from "@/api/assets";

const theme = useTheme();
const runs = ref([]);

const emit = defineEmits(["runSelected"]);

onMounted(async () => {
	const response = await MegaBonkAPI.getPaginatedRuns();
	runs.value = response.data.results;
});

function onRowClick(id) {
	if (id) emit("runSelected", id);
}
</script>

<style scoped>
.run-table {
	width: 100%;
	max-height: 45vh;
	overflow-y: auto;
	border-radius: 12px;
    overflow-x: hidden;
}

/* Header */
.table-header {
	display: flex;
	font-weight: 600;
	text-transform: uppercase;
	font-size: 0.9rem;
	padding: 8px 12px;
	background-color: rgba(255, 255, 255, 0.08);
	border-bottom: 1px solid rgba(255, 255, 255, 0.15);
	position: sticky;
	top: 0;
	z-index: 2;
	backdrop-filter: blur(6px);
    text-align: center;
}



/* Body rows */
.table-body {
	display: flex;
	flex-direction: column;
}

.table-row {
	display: flex;
	align-items: center;
	padding: 8px 12px;
	transition: background-color 0.2s ease, transform 0.15s ease;
	cursor: pointer;
	border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.table-row:hover {
	background-color: rgba(255, 255, 255, 0.08);
	transform: scale(1.01);
}

/* Win/Loss shading */
.table-row.win {
	background-color: rgba(0, 255, 0, 0.08);
}

.table-row.loss {
	background-color: rgba(255, 0, 0, 0.08);
}

/* Columns */
.col {
	flex: 1;
	display: flex;
	align-items: center;
    justify-content: center;
    text-align: center;
}

.col-character {
	flex: 1.1;
}

.col-weapons {
	flex: 1.5;
}

.col-tomes {
	flex: 1;
}

.truncate {
	white-space: nowrap;
	overflow: hidden;
	text-overflow: ellipsis;
}

/* Scrollbar styling */
.run-table::-webkit-scrollbar {
	width: 6px;
}
.run-table::-webkit-scrollbar-thumb {
	background-color: rgba(255, 255, 255, 0.2);
	border-radius: 4px;
}
</style>
