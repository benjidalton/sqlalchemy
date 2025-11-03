<template>
	<div class="container">
		<!-- Button to open selection dialog -->
		<div class="item-select">
			<div class="item-btn-wrapper">
				<v-btn
					color="primary"
					variant="elevated"
					block
					class="animated-btn"
					@click="dialog = true"
					:class="{ sweeping: sweepActive }"
				>
					<v-icon start>{{ icon }}</v-icon>
					{{ label }}
					<v-icon end>mdi-plus</v-icon>
				</v-btn>
			</div>

			<!-- Item Selection Dialog -->
			<v-dialog v-model="dialog" max-width="600px">
				<v-card>
					<v-card-title class="text-h6">
						Select Items
					</v-card-title>
					<v-divider></v-divider>

					<v-card-text>
						<v-container>
							<v-row
								v-for="item in options"
								:key="item.id"
								align="center"
								class="py-1"
							>
								<!-- Left column: item name toggle -->
								<v-col cols="7">
									<v-btn
										block
										variant="outlined"
										:color="isSelected(item.id) ? 'secondary' : 'primary'"
										@click="toggleItem(item)"
									>
										{{ item.name }}
									</v-btn>
								</v-col>

								<!-- Right column: quantity input -->
								<v-col cols="5">
									<v-text-field
										v-model.number="tempQuantities[item.id]"
										label="Qty"
										type="number"
										variant="outlined"
										density="compact"
										min="1"
										:disabled="!isSelected(item.id)"
									/>
								</v-col>
							</v-row>
						</v-container>
					</v-card-text>

					<v-card-actions>
						<v-spacer></v-spacer>
						<v-btn text color="grey" @click="dialog = false">Cancel</v-btn>
						<v-btn color="primary" variant="elevated" @click="confirmSelection">
							Confirm
						</v-btn>
					</v-card-actions>
				</v-card>
			</v-dialog>
		</div>
	</div>
</template>

<script setup>
import { ref, watch, nextTick } from "vue";

const props = defineProps({
	modelValue: {
		type: Array,
		default: () => []
	},
	options: {
		type: Array,
		default: () => []
	},
	label: String,
	icon: String
});

const emit = defineEmits(["update:modelValue"]);

const dialog = ref(false);
const sweepActive = ref(false);
const selectedItems = ref([...props.modelValue]);
const tempQuantities = ref({});

// Keep internal state in sync with parent
watch(
	() => props.modelValue,
	(newVal) => {
		selectedItems.value = [...newVal];
	},
	{ deep: true }
);

// Initialize quantities when options change
watch(
	() => props.options,
	(options) => {
		if (!options) return;
		for (const item of options) {
			tempQuantities.value[item.id] = tempQuantities.value[item.id] ?? 1;
		}
	},
	{ immediate: true }
);

const isSelected = (id) => selectedItems.value.some((i) => i.id === id);

function toggleItem(item) {
	const exists = isSelected(item.id);
	if (exists) {
		selectedItems.value = selectedItems.value.filter((i) => i.id !== item.id);
	} else if (selectedItems.value.length < 4) {
		selectedItems.value.push({
			id: item.id,
			name: item.name,
			quantity: 1
		});
	}
}

async function confirmSelection() {
	// Merge quantities into selected items
	const finalSelection = selectedItems.value.map((item) => ({
		...item,
		quantity: tempQuantities.value[item.id] ?? 1
	}));

	dialog.value = false;
	emit("update:modelValue", finalSelection);

	// trigger sweep animation when all 4 selected
	if (finalSelection.length === 4) {
		await nextTick();
		triggerButtonSweep();
	}
}

function triggerButtonSweep() {
	sweepActive.value = true;
	setTimeout(() => {
		sweepActive.value = false;
	}, 1500);
}
</script>

<style scoped>
.container {
	position: relative;
	width: 100%;
	min-height: 100px;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
}

/* Full-width add button */
.item-select {
	position: relative;
	width: 100%;
	z-index: 2;
}

.animated-btn {
	height: 80px;
	font-size: 18px;
	font-weight: 500;
	border-radius: 20px;
	display: flex;
	align-items: center;
	justify-content: center;
	text-transform: none;
}

.v-card-text {
	max-height: 70vh;
	overflow-y: auto;
}
</style>
