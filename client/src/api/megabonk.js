import api from './index.js'

const basePath = "megabonk"

export const MegaBonkAPI = {
	list() {
		return api.get(`/${basePath}/`);
	},
	get(userId) {
		return api.get(`/${basePath}/${userId}`);
	},
	create(data) {
		return api.post(`/${basePath}/create`, data);
	},
	getStaticData() {
		return api.get(`/${basePath}/static`)
    },
    getWinRates() {
        return api.get(`/${basePath}/winrates`)
    }
}