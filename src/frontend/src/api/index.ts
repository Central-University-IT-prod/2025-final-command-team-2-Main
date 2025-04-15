import axios from 'axios';

const Axios = axios.create({
	baseURL: 'https://prod-team-2-b2gtedt8.REDACTED/api/',
});

Axios.interceptors.response.use(
	res => res,
	error => {
		if (error.status === 401) {
			localStorage.removeItem('token');
		}
		return Promise.reject(error);
	},
);

// if (localStorage.getItem('token')) {
// 	Axios.defaults.headers.common['Authorization'] =
// 		`Bearer ${localStorage.getItem('token')}`;
// }

export { Axios };
