// stores/app.js
import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', () => {
	const loading = ref(false)

	function setLoading(value) {
		loading.value = value
	}

	return { loading, setLoading }
})