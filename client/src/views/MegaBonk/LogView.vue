<template>
	<v-container
		class="fill-height d-flex align-center justify-center pa-0"
		fluid
	>
		<v-row
			align="center"
			justify="center"
			class="ma-0 theme-row"
		>
			<v-col cols="12" sm="10" md="8" lg="6">
				<v-card id="formInput" elevation="6" class="pa-6 rounded-xl">
					<v-card-title class="text-h5 font-weight-bold text-primary">
						Log Run
					</v-card-title>

					<v-card-text>
						<v-form ref="formRef" v-model="isValid" lazy-validation>
							<v-divider class="my-4" />
							<CharaceterSelect 
								v-model="form.characterId"
								:characters="characters"
							/>

							<!-- Weapons -->
							<v-divider class="my-4" />
								<AnimatedSelection 
									v-model="form.weapons"
									:options="weapons"
									label="Weapons"
									icon="mdi-sword"
								/>

							<!-- Tomes -->
							<v-divider class="my-4" />
								<AnimatedSelection 
									v-model="form.tomes"
									:options="tomes"
									label="Tomes"
									icon="mdi-book"
								/>
							<!-- Items -->
							<v-divider class="my-4" />
								<ItemSelection 
									v-model="form.items"
									:options="items"
									label="Items"
									icon="mdi-treasure-chest"
								/>

							<v-divider class="my-4" />

							<v-row align="center" dense>
								<!-- Duration -->
								<v-col cols="12" sm="3">
									<v-text-field
										v-model="form.durationMinutes"
										label="Duration (minutes)"
										prepend-inner-icon="mdi-timer"
										type="number"
										variant="outlined"
										:rules="[rules.required]"
										clearable
									/>
								</v-col>

								<!-- Score -->
								<v-col cols="12" sm="3">
									<v-text-field
										v-model="form.score"
										label="Kills"
										prepend-inner-icon="mdi-numeric"
										type="number"
										variant="outlined"
										clearable
									/>
								</v-col>

								<!-- Map Dropdown -->
								<v-col cols="12" sm="3">
									<v-select
										v-model="form.map"
										:items="['Forest', 'Desert']"
										label="Map"
										prepend-inner-icon="mdi-map"
										variant="outlined"
									/>
								</v-col>
								
								<!-- Win Checkbox -->
								<v-col cols="12" sm="3" class="d-flex flex-column justify-end">
									<span class="text-subtitle-2 mb-0 ml-14">Win?</span>
									<div class="d-flex align-center">
										<v-checkbox
											v-model="form.won"
											color="success"
											hide-details
											density="compact"
											class="ma-0 pa-0 mb-5 ml-14"
										/>
									</div>
								</v-col>

							</v-row>
							

							<!-- Notes -->
							<v-divider class="my-4" />
								<v-textarea
									v-model="form.notes"
									label="Notes"
									prepend-inner-icon="mdi-note-text"
									variant="outlined"
									rows="3"
									clearable
								/>

							<!-- Submit -->
							<v-btn
								class="mt-6"
								:disabled="!isValid"
								color="primary"
								block
								size="large"
								@click="submitForm"
							>
								<v-icon start>mdi-content-save</v-icon>
								Submit Run
							</v-btn>

						</v-form>
					</v-card-text>
				</v-card>
			</v-col>
		</v-row>
	</v-container>
</template>

<script setup>
import { ref, computed, onMounted, reactive, watch } from "vue";
import { MegaBonkAPI } from "@/api/megabonk";
import CharaceterSelect from "@/components/MegaBonk/CharaceterSelect.vue";
import AnimatedSelection from "@/components/MegaBonk/AnimatedSelect.vue";
import ItemSelection from "@/components/MegaBonk/ItemSelect.vue";
// import { CharacterAPI } from "@/api/characters";

const displayCharacters = ref(false);
const isValid = ref(false);
const characters = ref([]);
const weapons = ref([]);
const items = ref([]);
const tomes = ref([]);

const form = reactive({
	characterId: null,
	durationMinutes: null,
	score: null,
	won: false,
	notes: "",
	weapons: [],
	tomes: [],
	items: [],
	map: 'Forest'
});

const formRef = ref(null);

const rules = {
	required: (v) => !!v || "This field is required"
};


onMounted(async () => {
	const response = await MegaBonkAPI.getStaticData();
	
	const withQuantity = (arr) => {
		return Array.isArray(arr)
			? arr.map((obj) => ({
				...obj,
				quantity: obj.quantity ?? 1
			}))
			: [];
	};

	characters.value = withQuantity(response.data.characters);
	weapons.value = withQuantity(response.data.weapons);
	items.value = withQuantity(response.data.items);
	tomes.value = withQuantity(response.data.tomes);
});

watch(
	() => form.characterId,
	(newCharacterId) => {
		if (!newCharacterId) {
			form.weapons = [];
			return;
		}

		const selectedCharacter = characters.value.find(
			(c) => c.id === newCharacterId
		);
		console.log("selected character: ", selectedCharacter)
		if (selectedCharacter?.default_weapon_id) {
			const defaultWeapon = weapons.value.find(
				(w) => w.id === selectedCharacter.default_weapon_id
			);

			if (defaultWeapon) {
				form.weapons = [{ ...defaultWeapon, quantity: 1 }];
			}
		}
	},
	{ immediate: true } // optional: runs once on mount
);

async function submitForm() {
	try {
	

		 const requestBody = {
			characterId: Number(form.characterId),
			durationMinutes: Number(form.durationMinutes),
			score: Number(form.score),
			won: Boolean(form.won),
			notes: form.notes ?? "",
			weapons: form.weapons.map(w => ({
				weaponId: w.id,
				quantity: w.quantity
			})),
			tomes: form.tomes.map(t => ({
				tomeId: t.id,
				quantity: t.quantity
			})),
			items: form.items.map(i => ({
				itemId: i.itemId ?? i.id,
				quantity: i.quantity
			}))
		};

		console.log("Sending body:", requestBody);
		const response = await MegaBonkAPI.create(requestBody);
		if (response.status !== 200) throw new Error("Failed to submit run");
		alert("Run submitted successfully!");
		// resetForm();
	} catch (err) {
		console.error(err);
		alert("Failed to create run");
	}
}

</script>

<style scoped>
.v-container {
	min-height: 100vh;
	min-width: 100vw;
	display: flex;
	align-items: center;
	justify-content: center;
}

#formInput {
	min-width: 50vw;
}

.theme-row {
	background-color: var(--v-theme-background);
	color: var(--v-theme-on-surface);
}
</style>
