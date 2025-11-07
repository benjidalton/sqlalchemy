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
    },
    getPaginatedRuns(page = 1 , pageSize = 10) {
        return api.get(`/${basePath}/runs?page=${page}&page_size=${pageSize}`)
    },
    getRunDetailsById(runId) {
         return api.get(`/${basePath}/fetch/run/${runId}`)
    }
}