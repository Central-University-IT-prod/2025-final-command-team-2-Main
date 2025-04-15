export type CreateFilmType = {
	title: string;
	genre: string;
	year?: number;
	image_url?: string;
	image_base64?: string;
	description?: string;
	duration?: number;
	rating?: number;
	loaded_from_tmdb?: boolean;
	user_added?: boolean;
};

export interface SearchMovie {
	id: number;
	title: string;
	rating?: number;
	year?: number;
	image_url?: string;
	image_base64?: string;
	description?: string;
	genre?: string;
	loaded_from_tmdb?: boolean;
	user_added?: boolean;
  }

export interface Movie {
	description: string;
	genre: string;
	id: number;
	image_base64?: string;
	image_url: string;
	loaded_from_tmdb: boolean;
	originalTitle: string;
	rating: number;
	title: string;
	user_added: boolean;
	year: number;
}

export interface Film extends CreateFilmType {
	id: string;
	notes: string;
}

export interface TGUser {
	id: string;
	username: string;
	avatarUrl: string;
}

export interface User extends TGUser {
	userId: string;
	addedAt: string;
}

export interface Collection {
	id: string;
	name: string;
	description: string;
	groupId: string;
	movies: Film[];
	users: User[];
	isDefault: boolean;
	isGroupCollection: boolean;
	createdAt: string;
	updatedAt: string;
}

export interface CreateCollectionRequest {
	name: string;
	description?: string;
	isDefault?: boolean;
	initialUsers: {
		telegramId: number;
	}[];
}
