import api from './index.js'

export const UserAPI = {
  	list() {
		return api.get('/users/');
  	},
	get(userId) {
		return api.get(`/users/${userId}`);
	},
	create(data) {
		return api.post('/users/create', data);
	}
}