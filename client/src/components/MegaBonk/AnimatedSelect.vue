<template>
	<div class="container">
		<!-- Before 4 items are chosen -->
		<div v-show="!showQuantityInputs" class="item-select">
			<div class="item-btn-wrapper">
				<v-btn
					v-show="!sweepActive"
					color="primary"
					variant="elevated"
					block
					class="animated-btn"
					@click="dialog = true"
					:disabled="modelValue.length >= 4"
				>
					<v-icon start>{{ icon }}</v-icon>
					{{ label }}
					<v-icon end>mdi-plus</v-icon>
				</v-btn>
				</div>
			</div>

			<!-- item Selection Dialog -->
			<v-dialog v-model="dialog" max-width="80vw">
				<v-card>
					<v-card-title class="text-h6">
						Select up to 4 {{ label }}
					</v-card-title>
					<v-divider></v-divider>

					<v-card-text>
						<v-container fluid>
							<v-row dense>
								<v-col
									v-for="item in options"
									:key="item.id"
									cols="2"
									class="d-flex justify-center mb-2"
								>
									<v-btn
										class="rounded-lg text-truncate"
										:color="isSelected(item.id) ? 'secondary' : 'primary'"
										variant="outlined"
										block
										@click="toggleItem(item)"
										style="height: 60px; font-size: 14px;"
									>
										<v-img
										:src="AssetsAPI.getImageUrl(item.img_source)"
										alt="Selected character"
										width="60"
										height="60"
										contain
									/>
                                    {{ item.label }}
									</v-btn>

									
								</v-col>
							</v-row>
						</v-container>
					</v-card-text>

					<v-card-actions>
						<v-spacer></v-spacer>
						<v-btn text color="grey" @click="dialog = false">Cancel</v-btn>
						<v-btn
							color="primary"
							variant="elevated"
							@click="confirmSelection"
						>
							Confirm
						</v-btn>
					</v-card-actions>
				</v-card>
			</v-dialog>

		<div
			class="quantity-container"
			:class="{ visible: showQuantityInputs }"
		>
			<v-row dense align="center" justify="center" no-gutters>
				<v-col
					v-for="item in selectedItems"
					:key="item.id"
					cols="auto"
					class="d-flex justify-center"
				>
					<v-text-field
						v-model.number="item.quantity"
						type="number"
						min="0"
						density="comfortable"
						variant="outlined"
						class="quantity-input"
						:label="item.label"
						@update:model-value="emit('update:modelValue', selectedItems)"
					/>
				</v-col>
			</v-row>
		</div>
	</div>

		<!-- After 4 items are chosen: sweeping vertical bar -->

</template>

<script setup>
import { ref, watch, nextTick } from "vue";
import { AssetsAPI } from "@/api/assets";

const props = defineProps({
	modelValue: {
		type: Array,
		default: () => []
	},
	options: {
		type: Array,
		default: () => []
	},
	label: {
		type: String
	},
	icon: {
		type: String
	}
});

const emit = defineEmits(["update:modelValue"]);

const dialog = ref(false);
const selectedItems = ref([...props.modelValue]);
const animationActive = ref(false);
const sweepActive = ref(false);
const showQuantityInputs = ref(false);

watch(
	() => props.modelValue,
	(newVal) => {
		selectedItems.value = [...newVal];
	},
	{ deep: true }
);

const isSelected = (id) => selectedItems.value.some((w) => w.id === id);

const toggleItem = (item) => {
	const exists = selectedItems.value.find((w) => w.id === item.id);

	if (exists) {
		selectedItems.value = selectedItems.value.filter(
			(w) => w.id !== item.id
		);
	} else if (selectedItems.value.length < 4) {
		selectedItems.value.push({
			id: item.id,
			label: item.label,
			quantity: 1
		});
	}

	if (selectedItems.value.length === 4) {
		confirmSelection();
	}
};

const confirmSelection = async () => {
	dialog.value = false;
	emit("update:modelValue", [...selectedItems.value]);

	await nextTick();
	triggerButtonSweep();
};
const removeitem = (id) => {
	const updated = props.modelValue.filter((w) => w.id !== id);
	emit("update:modelValue", updated);
};

const triggerButtonSweep = async () => {
	sweepActive.value = true;

	// Start fading in inputs partway through sweep
	setTimeout(() => {
		showQuantityInputs.value = true;
	}, 700); // halfway through the 1.5s sweep

	setTimeout(() => {
		sweepActive.value = false;
		animationActive.value = true;
	}, 1500);
};
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

.animated-btn.sweeping {
	animation: fadeLeftToRight 1s forwards;
	mask-image: linear-gradient(to right, transparent 0%, black 0%);
	-webkit-mask-image: linear-gradient(to right, transparent 0%, black 0%);
}

.reverse {
	transform: scaleX(-1);
}
.reverse .animated-btn {
	transform: scaleX(-1); /* unflip inner content */
}

/* Animation frame styling (transparent) */
.animation-frame {
	position: relative;
	width: 100%;
	min-height: 100px;
	display: flex;
	align-items: center;
	justify-content: center;
	background: transparent;
	overflow: hidden;
	border-radius: 12px;
	z-index: 1;
}

/* Sweeping vertical bar */
.sweep-line {
	position: absolute;
	left: 0;
	top: 7px;
	width: 3px;
	height: 85px;
	background: linear-gradient(to right, rgba(255,255,255,0.9), transparent);
	animation: sweepAcross 1s ease-in-out forwards;
	z-index: 99;
	box-shadow: 0 0 15px rgba(255,255,255,0.6);
	pointer-events: none;
}

@keyframes sweepAcross {
	from {
		transform: translateX(0);
		opacity: 1;
	}
	to {
		transform: translateX(100vw);
		opacity: 0;
	}
}

@keyframes fadeLeftToRight {
	from {
		mask-image: linear-gradient(to right, transparent 0%, black 0%);
		-webkit-mask-image: linear-gradient(to right, transparent 0%, black 0%);
		opacity: 1;
	}
	to {
		mask-image: linear-gradient(to right, transparent 0%, black 100%);
		-webkit-mask-image: linear-gradient(to right, transparent 0%, black 100%);
		opacity: 0;
	}
}

/* Quantity input wrapper */
.quantity-container {
	position: absolute;
	top: 0; /* same start point as the button */
	width: 100%;
	display: flex;
	flex-wrap: wrap;
	justify-content: center;
	align-items: center;
	gap: 20px;
	min-height: 100px;
	opacity: 0;
	z-index: 1; /* bottom layer */
	animation: revealInputs 1s ease-in 1.3s forwards;
}

.quantity-wrapper.visible {
	opacity: 1;
	transform: translateY(0);
}

@keyframes revealInputs {
	from {
		opacity: 0;
	}
	to {
		opacity: 1;
	}
}

/* Inputs styling */
.quantity-input {
	width: 150px;
	margin: 10px;
	font-size: 20px;
}
</style>
