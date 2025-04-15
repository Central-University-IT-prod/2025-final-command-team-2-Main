import { Axios } from '.';

import { auth } from './auth';
import {
	Collection,
	CreateCollectionRequest,
	CreateFilmType,
	Movie,
} from './types';

export const getCollections = async (): Promise<Collection[]> => {
	try {
		await auth();

		const { data } = await Axios.get<Collection[]>('/collections/');

		return data;
	} catch (error) {
		console.log(error);
		return [];
	}
};

export const getAllMovies = async (): Promise<Movie[]> => {
	try {
		await auth();

		const { data } = await Axios.get<Movie[]>('/movies/');

		return data;
	} catch (error) {
		console.log(error);
		return [];
	}
};

export const createFilm = async (
	film: CreateFilmType,
): Promise<Movie | null> => {
	try {
		await auth();

		const { data } = await Axios.post<Movie>('/movies/', film);

		console.log('new film:', data);
		return data;
	} catch (error) {
		console.log(error);
		return null;
	}
};

export const deleteFilm = async (id: number): Promise<any> => {
	try {
		await auth();

		const { data } = await Axios.delete(`/movies/${id}/`);

		return data;
	} catch (error) {
		console.log(error);
		return null;
	}
};

export const addFilmToCollection = async (
	filmId: number,
	collectionId: number,
): Promise<Collection | null> => {
	try {
		await auth();

		const { data } = await Axios.post<Collection>(
			`/collections/${collectionId}/movies`,
			{
				movieId: filmId,
			},
		);

		return data;
	} catch (error) {
		console.log(error);
		return null;
	}
};

export const deleteFilmFromCollection = async (
	collectionId: number,
	movieId: number,
): Promise<Collection | null> => {
	try {
		await auth();

		const { data } = await Axios.delete(
			`/collections/${collectionId}/movies/${movieId}`,
		);

		return data;
	} catch (error) {
		console.error('Error deleting film from collection:', error);
		return null;
	}
};

export const createCollection = async (
	name: string,
	description: string,
): Promise<CreateCollectionRequest> => {
	try {
		const user = await auth();

		console.log('user:', user);

		const payload: CreateCollectionRequest = {
			name: name,
			description: description,
			isDefault: false,
			initialUsers: [
				{
					telegramId: Number(user?.id),
				},
			],
		};

		const { data } = await Axios.post<CreateCollectionRequest>(
			'/collections/',
			payload,
		);
		return data;
	} catch (error) {
		console.error('Error creating collection:', error);
		throw error;
	}
};

export const getCollection = async (
	id: string,
): Promise<Collection | number> => {
	try {
		await auth();

		const { data } = await Axios.get(`/collections/${id}`);

		return data;
	} catch (error) {
		console.warn(error);

		return error.status;
	}
};

export const getMovieById = async (id: number): Promise<Movie | null> => {
	try {
		await auth();
		const { data } = await Axios.get(`/movies/${id}`);
		return data;
	} catch (error) {
		console.warn(error);
		return null;
	}
};

export const deleteCollection = async (collectionId: string): Promise<void> => {
	try {
		await auth();
		await Axios.delete(`/collections/${collectionId}`);
	} catch (error) {
		console.error('Error deleting collection:', error);
		throw error;
	}
};
