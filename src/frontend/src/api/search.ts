import { Axios } from '.';
import { auth } from './auth';
import { Movie } from './types';

interface SearchResponse {
    results: Movie[];
    total_pages: number;
    total_results: number;
}

interface AISearchResponse {
    film_name: string;
}

export const search = async (query: string, page: number = 1): Promise<SearchResponse> => {
    try {
        await auth();
        const response = await Axios.post<SearchResponse>('/movie/search/', {
            query: query,
            page: page
        });
        console.log(response.data);
        return response.data;
    } catch (error) {
        console.error(error);
        return {
            results: [],
            total_pages: 0,
            total_results: 0
        };
    }
};

export const searchAI = async (query: string): Promise<string> => {
    try {
        await auth();
        const response = await Axios.post<AISearchResponse>('/movie/search/ai', {
            query: query
        });
        return response.data.film_name;
    } catch (error) {
        console.error('AI Search error:', error);
        throw error;
    }
};