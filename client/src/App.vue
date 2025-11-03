<template>
	<v-app :style="{ backgroundColor: backgroundColor, color: textColor }">
		 <TopNavBar />
	<!-- <v-app :style="{ backgroundColor: backgroundColor, color: textColor }"> -->
		<RouterView />

	</v-app>
   
	<!-- </v-app> -->
</template>

<script setup>
import { computed } from 'vue';
import { RouterView } from 'vue-router';
import { useTheme } from 'vuetify';
import TopNavBar from './components/TopNavBar.vue';

const theme = useTheme()
const backgroundColor = computed(() => theme.current.value.colors.background)
const textColor = computed(() => theme.current.value.colors.onSurface)
</script>

<style>
html,
body,
#app,
.v-application,
.v-main {
	margin: 0;
	padding: 0;
	width: 100%;
	height: 100%;
}
.v-main {
	padding: 0 !important;
	display: flex;
	align-items: center;
	justify-content: center;
}
</style>
