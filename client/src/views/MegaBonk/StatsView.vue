<template>
	<div class="main-layout">
		<!-- Left panel (chart) -->
		<div class="left-panel">
			<ChartPanel />
		</div>

		<!-- Right panel -->
		<div class="right-panel d-flex align-center justify-center">
			<v-card
				class="pa-8 text-center"
				:style="{ backgroundColor: theme.current.value.colors.surface }"
				elevation="2"
			>
				<h2>Stats Overview</h2>
				<p>Additional info or widgets will go here.</p>
			</v-card>
		</div>
	</div>
</template>

<script setup>
import ChartPanel from "@/components/MegaBonk/ChartPanel.vue";
import { useTheme } from "vuetify";

const theme = useTheme();
</script>

<style scoped>
.main-layout {
	display: flex;
	height: calc(100vh - 64px); /* account for navbar */
	margin-top: 64px;
	width: 100vw;
}

.left-panel {
	width: 30%;
	border-right: 1px solid rgba(255, 255, 255, 0.1);
	overflow-y: auto;
}

.right-panel {
	width: 70%;
	display: flex;
	align-items: center;
	justify-content: center;
	overflow-y: auto;
	padding: 24px;
}
</style>
