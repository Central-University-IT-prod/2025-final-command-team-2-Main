<script setup lang="ts">
import { onMounted, ref } from 'vue';
import WideMovieCard from '@/components/WideMovieCard.vue';
import { getCollections, getMovieById, deleteFilmFromCollection } from '@/api/collections';
import { Film, SearchMovie } from '@/api/types';
import MovieInfoModal from "@/components/MovieInfoModal.vue";
import { useViewStore } from '@/services/stores.js';

const viewStore = useViewStore();
const movieObject = ref<SearchMovie | null>(null);
const isOpenModal = ref(false);
const savedMovies = ref<Film[]>([]);
const loadingMovieId = ref<string | null>(null);
const isAddingToCollection = ref(false);

const openMovieModal = async (id: number) => {
  try {
    const movie = await getMovieById(id);
    if (movie) {
      movieObject.value = {
        id: movie.id,
        title: movie.title,
        rating: movie.rating,
        year: movie.year,
        image_url: movie.image_url,
        image_base64: movie.image_base64,
        description: movie.description,
        genre: movie.genre,
        loaded_from_tmdb: movie.loaded_from_tmdb,
        user_added: movie.user_added,
      };
    }
    isOpenModal.value = true;
  } catch (error) {
    console.error('Ошибка загрузки фильма:', error);
  }
};

const deleteMovie = async (movieId: string) => {
  try {
    loadingMovieId.value = movieId;
    const collections = await getCollections();
    const defaultCollection = collections.find(collection => collection.isDefault);
    if (defaultCollection) {
      await deleteFilmFromCollection(Number(defaultCollection.id), Number(movieId));
      savedMovies.value = savedMovies.value.filter(film => film.id !== movieId);
      viewStore.showNotification('Фильм успешно удален');
    }
  } catch (error) {
    console.error('Ошибка удаления фильма:', error);
    viewStore.showNotification('Ошибка при удалении фильма', 'error');
  } finally {
    loadingMovieId.value = null;
  }
};

onMounted(async () => {
  try {
    const collections = await getCollections();
    savedMovies.value = collections.flatMap(col => col.movies);
  } catch (error) {
    console.error('Ошибка загрузки коллекций:', error);
  }
});
</script>

<template>
  <div class="container">
    <h1 class="text-2xl font-bold mb-4 text-white">Сохраненные фильмы</h1>
    <div class="flex flex-col gap-4">
      <WideMovieCard
        v-for="movie in savedMovies"
        :key="movie.id"
        :title="movie.title"
        :description="movie.description"
        :imgUrl="movie.loaded_from_tmdb ? movie.image_base64 : (movie.image_url && movie.image_url !== 'null' ? movie.image_url : '/movielogo.png')"
        :rating="movie.rating"
        :genre="movie.genre"
        :date="movie.year"
        :showDelete="true"
        :is-loading="loadingMovieId === movie.id"
        @click="openMovieModal(Number(movie.id))"
        @delete="deleteMovie(movie.id)"
      />
    </div>

    <MovieInfoModal
      :movie="movieObject"
      @close="movieObject = null"
      :is-keyboard-open="false"
      :is-loading="isAddingToCollection"
    />
  </div>
</template>