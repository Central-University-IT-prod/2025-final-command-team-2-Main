<template>
  <div class="text-white p-2 container flex flex-col">
    <div class="flex-none">
      <h1 class="text-2xl font-bold mb-4">Поиск по фильмам</h1>
      <input
        placeholder="Search"
        class="w-full mb-6 outline-none border-none rounded-2xl p-2 bg-[#3A3F47] text-white"
        @click="handleClick"
      />

      <h3 class="text-xl font-semibold mb-4">Ваша подборка фильмов</h3>
    </div>

    <h4 v-if="state === 'pending'" class="text-center text-3xl">Загрузка...</h4>

    <div
      v-if="savedFilms.length || state === 'pending'"
      class="flex flex-col gap-4 overflow-y-scroll"
      style="height: calc(100svh - 64px - 48px - 48px - 44px - 68px)"
    >
      <WideMovieCard
        v-for="movie in savedFilms"
        :key="movie.id"
        :date="movie.year"
        :title="movie.title"
        :imgUrl="
          movie.loaded_from_tmdb
            ? movie.image_base64
            : movie.image_url !== 'null'
              ? movie.image_url
              : '/movielogo.png'
        "
        :rating="movie.rating"
        :duration="movie.duration"
        :genre="movie.genre"
        :showDelete="true"
        :is-loading="loadingMovieId === movie.id"
        @click="openMovieModal(Number(movie.id))"
        @delete="deleteMovie(movie.id)"
      />
    </div>

    <MovieInfoModal
      :movie="movieObject"
      :is-keyboard-open="false"
      :is-loading="isAddingToCollection"
      @close="movieObject = null"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import {
  getCollections,
  getMovieById,
  deleteFilmFromCollection,
} from '@/api/collections';
import { Film, SearchMovie } from '@/api/types';
import { useViewStore } from '@/services/stores.js';
import WideMovieCard from '@/components/WideMovieCard.vue';
import MovieInfoModal from '@/components/MovieInfoModal.vue';

const router = useRouter();
const viewStore = useViewStore();
const state = ref('pending');
const savedFilms = ref<Film[]>([]);
const movieObject = ref<SearchMovie | null>(null);
const isOpenModal = ref(false);
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
    const defaultCollection = collections.find(
      (collection) => collection.isDefault,
    );
    if (defaultCollection) {
      await deleteFilmFromCollection(
        Number(defaultCollection.id),
        Number(movieId),
      );
      savedFilms.value = savedFilms.value.filter((film) => film.id !== movieId);
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
    state.value = 'pending';
    const collections = await getCollections();
    const defaultCollection = collections.find(
      (collection) => collection.isDefault,
    );
    if (defaultCollection) {
      savedFilms.value = defaultCollection.movies;
    }
  } catch (error) {
    console.warn('Ошибка загрузки фильмов:', error);
  } finally {
    state.value = 'idle';
  }
});

const handleClick = () => {
  viewStore.changeSearch();
};
</script>
