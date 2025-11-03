<template>
	<v-app-bar
		elevation="2"
	>
		<v-app-bar-title class="font-weight-bold">
			My App
		</v-app-bar-title>

		<template v-for="(item, index) in buttons" :key="index">
			<v-btn
				color="primary"
				variant="text"
				:title=item.label
				@click="router.push({ name: item.route })"
			>
				{{ item.label }}
			</v-btn>
		</template>

		<v-spacer />


		<!-- Theme toggle button -->
		<v-select
			v-model="selectedTheme"
			:items="themes"
			label="Theme"
			variant="outlined"
			density="compact"
			hide-details
			style="max-width: 160px; margin-right: 10px;"
			@update:model-value="applyTheme"
		></v-select>
	</v-app-bar>
</template>

<script setup>
import { computed, ref } from 'vue';
import { useTheme } from 'vuetify';
import { useRouter } from 'vue-router';

const router = useRouter();
const theme = useTheme();
const themes = [
	{ title: 'Light', value: 'myCustomLightTheme' },
	{ title: 'Dark', value: 'myCustomDarkTheme' },
	{ title: 'Forest', value: 'forestTheme' },
	{ title: 'Sakura', value: 'sakuraTheme' },
]

const buttons = [
	{ label: "Log", route: "log" },
	{ label: "Stats", route: "stats" }
]

const selectedTheme = ref(theme.global.name.value);

function applyTheme(value) {
	theme.change(value);
}

</script>

<style scoped>
.v-app-bar {
	position: fixed;
	top: 0;
	left: 0;
	width: 100%;
	z-index: 10;
}
</style>
