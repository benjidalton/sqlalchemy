<template>
	<div class="container">
		<div class="item-select">
			<div class="item-btn-wrapper">
				<v-btn
					color="primary"
					variant="elevated"
					block
					class="animated-btn"
					@click="dialog = true"
				>
					<template v-if="selectedCharacter">
						<v-img
							:src="AssetsAPI.getImageUrl(selectedCharacter.img_source)"
							alt="Selected character"
							width="60"
							height="60"
							contain
							class="mr-2 rounded-xl"
						/>
						{{ selectedCharacter.label }}
					</template>

					<!-- Otherwise show the label -->
					<template v-else>
						<v-icon start>mdi-account-group</v-icon>
						Characters
						<v-icon end>mdi-plus</v-icon>
					</template>
				</v-btn>
				</div>
		</div>
	</div>
	<v-dialog v-model="dialog" fullscreen transition="dialog-bottom-transition">
		<v-card class="pa-4">
			<!-- Header -->
			<v-toolbar flat>
				<v-toolbar-title class="text-h5 font-weight-bold">Characters</v-toolbar-title>
				<v-spacer />
				<v-btn icon="mdi-close" @click="closeDialog" />
			</v-toolbar>

			<v-divider class="mb-4" />

			<!-- Image grid -->
			<v-container fluid>
				<v-row>
					<v-col
						v-for="char in characters"
						:key="char.id"
						cols="5"
						sm="5"
						md="4"
						lg="3"
						class="d-flex flex-column align-center mb-4"
					>
						<v-card
							elevation="6"
							rounded="xl"
							class="d-flex flex-column align-center justify-center"
							style="width: 150px; height: 150px;"
							@click="selectCharacter(char.id)"
						>
							<v-img
								:src="AssetsAPI.getImageUrl(char.img_source)"
								alt="Character"
								contain
								width="100%"
								height="100%"
								@error="onError"
							>
								<template #placeholder>
									<v-skeleton-loader type="image" />
								</template>

							<template #error>
								<div class="d-flex align-center justify-center text-grey text-caption" style="height: 100%;">
									<v-icon color="grey" size="40">mdi-image-off</v-icon>
									<span class="ml-2">No image</span>
								</div>
							</template>
							</v-img>
						</v-card>

						<span class="mt-2 text-center text-subtitle-2 font-weight-medium">
							{{ char.label }}
						</span>
					</v-col>
				</v-row>
			</v-container>
		</v-card>
	</v-dialog>
</template>

<script setup>
import { ref, computed, defineProps, defineEmits, onMounted } from "vue";
import { AssetsAPI } from "@/api/assets";

const props = defineProps({
	modelValue: { 
		type: [Number, null], 
		required: true 
	},
	characters: {
		type: Array,
		default: () => [
			// Example shape
			{ id: 1, label: "Fox", image: "/assets/megabonk/characters/fox.png" },
			{ id: 2, label: "Goose", image: "/assets/megabonk/characters/mini/mini_fox.png" }
		]
	}
});

const dialog = ref(false);
const emit = defineEmits(["update:show", "update:modelValue"]);

onMounted(() => console.log("props.char", props.characters))

const selectedCharacter = computed(() =>
	props.characters.find((c) => c.id === props.modelValue)
);

const closeDialog = () => (dialog.value = false);

const onError = (e) => {
	e.target.src = "/fallback.jpg";
};

function selectCharacter(id) {
	emit("update:modelValue", id);
	dialog.value = false;
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

/* Full-width add button */
.item-select {
	position: relative;
	width: 100%;
	z-index: 2;
}
.v-dialog {
	z-index: 2000;
}

.v-img {
	border-radius: 16px;
	background-color: var(--v-theme-surface);
}
</style>
