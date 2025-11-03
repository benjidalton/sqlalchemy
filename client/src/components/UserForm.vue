<template>
	<v-container
	class="fill-height d-flex align-center justify-center pa-0"
	fluid
>
	<v-row
		align="center"
		justify="center"
		class="ma-0"
		:style="{
			backgroundColor: backgroundColor,
			color: textColor,
		}"
	>
		<v-col cols="12" sm="8" md="6" lg="4">
			<v-card id="formInput" elevation="6" class="pa-6 rounded-xl">
				<v-card-title class="text-h5 font-weight-bold text-primary">
					Create User
				</v-card-title>

				<v-card-text>
					<v-form ref="form" v-model="isValid" lazy-validation>
						<v-text-field
							v-model="form.name"
							label="Full Name"
							prepend-inner-icon="mdi-account"
							:rules="[rules.required]"
							variant="outlined"
							clearable
						/>

						<v-text-field
							v-model="form.email"
							label="Email"
							prepend-inner-icon="mdi-email"
							:rules="[rules.required, rules.email]"
							variant="outlined"
							clearable
						/>

						<v-menu
							v-model="menu"
							:close-on-content-click="false"
							transition="scale-transition"
							offset-y
							max-width="290px"
							min-width="290px"
						>
							<template #activator="{ props }">
								<v-text-field
									v-model="form.birthdate"
									label="Birthdate"
									prepend-inner-icon="mdi-calendar"
									readonly
									v-bind="props"
									variant="outlined"
									clearable
								/>
							</template>
							<v-date-picker
								v-model="form.birthdate"
								@update:model-value="menu = false"
							/>
						</v-menu>

						<v-btn
							class="mt-6"
							:disabled="!isValid"
							color="primary"
							block
							size="large"
							@click="submitForm"
						>
							<v-icon start>mdi-content-save</v-icon>
							Submit
						</v-btn>
					</v-form>
				</v-card-text>
			</v-card>
		</v-col>
	</v-row>
</v-container>

</template>

<script setup>
import { ref, computed } from "vue";
import { useTheme } from "vuetify";
import { UserAPI } from "@/api/users";

const form = ref({
	name: "",
	email: "",
	birthdate: "",
});

const menu = ref(false);
const isValid = ref(false);

const theme = useTheme();
const backgroundColor = computed(() => theme.current.value.colors.background);
const cardColor = computed(() => theme.current.value.colors.surface);
const textColor = computed(() => theme.current.value.colors.onSurface);

const rules = {
	required: (v) => !!v || "This field is required",
	email: (v) => /.+@.+\..+/.test(v) || "Enter a valid email",
};

async function submitForm() {
	try {
		const requestBody = {
			name: form.value.name,
			email: form.value.email,
			birthdate: form.value.birthdate
		}
		const response = await UserAPI.create(requestBody);
		if (response.status !== 200) throw new Error("Failed to submit form");
		alert("User created successfully!");
		resetForm();
	} catch (err) {
		console.error(err);
		alert("Failed to create user");
	}
}

function resetForm() {
	form.value = { name: "", email: "", birthdate: "" };
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
	min-width: 25vw;
}
</style>
