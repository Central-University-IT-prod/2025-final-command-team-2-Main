<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

import MovieInfoModal from '@/components/MovieInfoModal.vue';
import WideMovieCard from '@/components/WideMovieCard.vue';

import {
	deleteFilmFromCollection,
	getCollection,
	getMovieById,
} from '@/api/collections';
import { Collection, Film, Movie } from '@/api/types';

import router from '@/services/router';
import { useViewStore } from '@/services/stores';

const route = useRoute();
const viewStore = useViewStore();
const collection = ref<Partial<Collection>>(null);
const selectedMovie = ref<Movie | null>(null);
const loadingMovieId = ref<string | null>(null);

const openMovieModal = async (id: number) => {
	try {
		const movie = await getMovieById(id);
		if (movie) {
			selectedMovie.value = movie;
		}
	} catch (error) {
		console.error('Ошибка загрузки фильма:', error);
	}
};

const handleDeleteMovie = async (movieId: number) => {
	try {
		if (!collection.value?.id) return;

		loadingMovieId.value = movieId.toString();
		await deleteFilmFromCollection(Number(collection.value.id), movieId);

		const res = await getCollection(route.params.id as string);
		if (res) {
			collection.value = res;
			viewStore.showNotification(
				'Фильм успешно удален из коллекции',
				'success',
			);
		}
	} catch (error) {
		console.error('Ошибка при удалении фильма:', error);
		viewStore.showNotification('Ошибка при удалении фильма', 'error');
	} finally {
		loadingMovieId.value = null;
	}
};

onMounted(async () => {
	const res = await getCollection(useRoute().params.id as string);

	if (typeof res === 'number') {
		if (res === 404 || res === 403) {
			router.push('/collections');
		} else {
			collection.value = {
				name: 'Не удалось загрузить коллекцию',
			};
		}

		return;
	}

	collection.value = res;
});
</script>
<template>
	<h1
		v-if="collection === null"
		class="text-white ml-3 text-3xl"
	>
		Загрузка...
	</h1>
	<h1
		v-else
		class="text-white ml-3 text-3xl"
	>
		{{ collection.name }}
	</h1>
	<div
		v-if="
			collection !== null &&
			collection.name !== 'Не удалось загрузить коллекцию'
		"
		class="mt-10"
	>
		<div
			v-if="collection.movies.length"
			class="flex flex-col gap-6 overflow-y-scroll"
			style="height: calc(100svh - 64px - 40px - 32px - 40px)"
		>
			<WideMovieCard
				v-for="movie in collection.movies"
				:key="movie.id"
				:title="movie.title"
				:description="movie.description"
				:img-url="
					movie.loaded_from_tmdb
						? movie.image_base64
						: movie.image_url && movie.image_url !== 'null'
							? movie.image_url
							: '/movielogo.png'
				"
				:rating="movie.rating"
				:genre="movie.genre"
				:date="movie.year"
				:show-delete="true"
				:is-loading="loadingMovieId === String(movie.id)"
				@click="openMovieModal(Number(movie.id))"
				@delete="handleDeleteMovie(Number(movie.id))"
			/>
		</div>
		<h3
			v-else
			class="text-center text-white text-3xl mt-20"
		>
			В коллекции нет фильмов
		</h3>
	</div>

	<MovieInfoModal
		:movie="selectedMovie"
		:is-keyboard-open="false"
		@close="selectedMovie = null"
	/>
</template>
