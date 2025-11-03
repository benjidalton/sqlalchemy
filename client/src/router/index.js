import { createRouter, createWebHistory } from 'vue-router'
import StatsView from '@/views/MegaBonk/StatsView.vue';
import LogView from '@/views/MegaBonk/LogView.vue';

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
        {
			path: '/',
			redirect: '/log' 
		},
		{
			path: '/log',
			name: 'log',
			component: LogView
		},
		{
			path: '/stats',
			name: 'stats',
			component: StatsView
		}
	],
});

export default router;
