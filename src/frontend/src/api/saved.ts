import { Axios } from '.';

import { auth } from './auth';
import { Film } from './types';

export const getSavedFilms = async (): Promise<Film[]> => {
	try {
		await auth();

		const { data } = await Axios.get('/movies/');

		return data;
	} catch (error) {
		console.warn(error);
		return [];
	}
};

// export const addFilm
