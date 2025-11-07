<template>
	<div class="main-layout">
		<!-- Left panel (chart) -->
		<div class="left-panel d-flex flex-column">
			<RunHistory class="mb-2" @runSelected="handleRunSelected"/>
			<v-divider />
			<ChartPanel class="mt-2 flex-grow-1" />
		</div>

		<!-- Right panel -->
		<div class="right-panel d-flex align-center justify-center">
			<!-- <v-card
				class="pa-8 text-center"
				:style="{ backgroundColor: theme.current.value.colors.surface }"
				elevation="2"
			>
				<h2>Stats Overview</h2>
				<p>Additional info or widgets will go here.</p>
			</v-card> -->

            <RunDetails v-if="displayRunDetails"/>
		</div>
	</div>
</template>

<script setup>
import { ref } from "vue";
import { useTheme } from "vuetify";
import ChartPanel from "@/components/MegaBonk/ChartPanel.vue";
import RunHistory from "@/components/MegaBonk/RunHistory.vue";
import RunDetails from "@/components/MegaBonk/RunDetails.vue";
import { MegaBonkAPI } from "@/api/megabonk";

const theme = useTheme();
const displayRunDetails = ref(false);

async function handleRunSelected(runId) {
    console.log("Run clicked:", runId);
    const response = await MegaBonkAPI.getRunDetailsById(runId);
    console.log("response", response)
    displayRunDetails.value = true;
}

</script>

<style scoped>
.main-layout {
	display: flex;
	height: calc(100vh - 64px); /* account for navbar */
	margin-top: 64px;
	width: 100vw;
}

.left-panel {
	width: 20%;
	border-right: 1px solid rgba(255, 255, 255, 0.1);
	overflow-y: auto;
}

.right-panel {
	width: 70%;
	display: flex;
	align-items: flex-start;
	justify-content: center;
	overflow-y: auto;
	padding: 24px;
}
</style>
