<template>
	<v-card
		class="fill-height d-flex flex-column align-center justify-start pa-4 h-100"
		elevation="3"
		:style="{ backgroundColor: theme.current.value.colors.background }"
	>
		<v-select
			v-model="selectedCategory"
			:items="categories"
			label="Select Category"
			variant="outlined"
			density="compact"
			hide-details
			class="mb-4"
			style="max-width: 240px; max-height: 5vh;"
		/>

		<div v-if="dataReady" class="bar-list w-100">
			<div
				v-for="(item, index) in currentData"
				:key="index"
				class="bar-row d-flex align-center mb-3"
			>
				<!-- Name -->
				<div class="bar-label">{{ item.label != '' ? item.label : item.gameRef }}</div>

				<!-- Bar container -->
				<div class="bar-container flex-grow-1 mx-3">
					<div
						class="bar-fill"
						:style="{
							width: item.win_rate + '%',
							backgroundColor: theme.current.value.colors.secondary,
						}"
					></div>
				</div>

				<!-- Percentage -->
				<div class="bar-value">{{ item.win_rate.toFixed(1) }}%</div>
			</div>
		</div>
	</v-card>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useTheme } from "vuetify";
import { MegaBonkAPI } from "@/api/megabonk";

const theme = useTheme();

const responseData = ref(null);
const dataReady = ref(false);

const categories = ["Characters", "Weapons", "Tomes", "Items"];
const selectedCategory = ref("Weapons");

onMounted(async () => {
	const response = await MegaBonkAPI.getWinRates();
	responseData.value = response.data;
	dataReady.value = true;
});

const currentData = computed(() => {
	const sortOrder = "desc";
	if (!responseData.value) return [];
	const items = responseData.value[selectedCategory.value.toLowerCase()] || [];
	return [...items].sort((a, b) =>
		sortOrder === "asc"
			? a.win_rate - b.win_rate
			: b.win_rate - a.win_rate
	);

});
</script>

<style scoped>
.bar-list {
	width: 100%;
	max-height: calc(100vh - 180px);
	overflow-y: auto;
	padding-right: 4px;
}

.bar-row {
	display: flex;
	align-items: center;
}

.bar-label {
	width: 150px;
	font-weight: 500;
	color: var(--v-theme-on-surface);
	white-space: nowrap;
	overflow: hidden;
	text-overflow: ellipsis;
}

.bar-container {
	position: relative;
	height: 20px;
	background-color: rgba(255, 255, 255, 0.1);
	border-radius: 10px;
	overflow: hidden;
}

.bar-fill {
	height: 100%;
	border-radius: 10px;
	transition: width 0.6s ease;
}

.bar-value {
	width: 60px;
	text-align: right;
	font-weight: 500;
	color: var(--v-theme-on-surface);
}
</style>
