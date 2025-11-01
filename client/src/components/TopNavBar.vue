<template>
	<v-app-bar
		elevation="2"
		:color="isDark ? 'surface' : 'primary'"
		:dark="isDark"
	>
		<v-app-bar-title class="font-weight-bold">
			My App
		</v-app-bar-title>

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

const theme = useTheme()
const themes = [
	{ title: 'Light', value: 'myCustomLightTheme' },
	{ title: 'Dark', value: 'myCustomDarkTheme' },
	{ title: 'Forest', value: 'forestTheme' },
	{ title: 'Sakura', value: 'sakuraTheme' },
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
