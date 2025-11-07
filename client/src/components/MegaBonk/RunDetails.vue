<template>
    <v-card
        class="stats-card"
        elevation="8"
        :style="{ backgroundColor: theme.current.value.colors.primary }"
    >
        <div class="stats-card-header">
            <h2>Stats Overview</h2>
            <p class="subtitle">Detailed insights from your last run</p>
        </div>

        <v-divider class="my-3" />

        <div class="stats-content">
            <p>This area could show charts, KPIs, or summaries.</p>
        </div>
    </v-card>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useTheme } from "vuetify";
import { MegaBonkAPI } from "@/api/megabonk";
import { AssetsAPI } from "@/api/assets";

const props = defineProps({
    runDetails: {
        required: true
    }
})

const theme = useTheme();

</script>

<style scoped>
/* The stats card itself */
.stats-card {
    width: 80%;              /* Takes 80% of right panel width */
    height: 20vh;  
    border-radius: 24px;
    padding: 32px;
    color: white;
    transition: box-shadow 0.3s ease, transform 0.2s ease;
}

/* Subtle hover animation */
.stats-card:hover {
    /* transform: translateY(-4px); */
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
}

/* Header inside the card */
.stats-card-header {
    text-align: center;
}

.stats-card-header h2 {
    margin: 0;
    font-weight: 600;
    letter-spacing: 1px;
}

.stats-card-header .subtitle {
    margin-top: 4px;
    opacity: 0.8;
    font-size: 0.9rem;
}

/* Optional content styling */
.stats-content {
    text-align: center;
    font-size: 1rem;
    opacity: 0.9;
}

</style>
