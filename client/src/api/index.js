// api.js
import axios from 'axios';
import { useAppStore } from '@/stores/app';
import { pinia } from '@/main';

const api = axios.create({
	baseURL: import.meta.env.VITE_API_URL,
	timeout: 30000,
	headers: {
		'Content-Type': 'application/json'
	}
})

// Request interceptor — set loading to true
api.interceptors.request.use(
	config => {
		const appStore = useAppStore(pinia)
		appStore.setLoading(true)
		return config
	},
	error => {
		const appStore = useAppStore(pinia)
		appStore.setLoading(false)
		return Promise.reject(error)
	}
)

// Response interceptor — set loading to false
api.interceptors.response.use(
	response => {
		const appStore = useAppStore(pinia)
		appStore.setLoading(false)
		return response
	},
	error => {
		const appStore = useAppStore(pinia)
		appStore.setLoading(false)
		console.error('API Error:', error)
		return Promise.reject(error)
	}
);

export default api;
