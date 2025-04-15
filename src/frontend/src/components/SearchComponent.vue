<template>
  <div class="container" @click="dismissKeyboard">
    <div class="flex items-center py-2">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-6 w-6 text-white"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        @click="viewStore.changeSearch()"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M15 19l-7-7 7-7"
        />
      </svg>
      <h1 class="text-xl font-bold text-white mx-4">Поиск по всем фильмам</h1>
    </div>
    <input
      ref="searchInput"
      v-model="searchInputContent"
      placeholder="Search"
      class="w-full mb-3 outline-none border-none rounded-2xl p-2 bg-[#3A3F47] text-white border"
      @input="handleSearchInput"
      @click.stop
    />
    <div class="flex justify-center mb-6">
      <button
        class="generate-button flex items-center justify-center gap-2 px-5 py-1.5 rounded-full text-white font-medium shadow-lg transition-all hover:scale-103"
        @click="showAIModal = true"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-4 w-4"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <polygon
            points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"
          ></polygon>
        </svg>
        <span>Забыли название?</span>
      </button>
    </div>
    <div v-if="searchResults.length > 0" class="flex flex-col gap-4 pb-5">
      <div
        v-if="totalPages > 1"
        class="flex justify-center items-center mb-2 gap-2"
      >
        <button
          :disabled="currentPage === 1 || isLoading"
          class="px-3 py-1 rounded-md bg-gray-700 text-white disabled:opacity-50 disabled:cursor-not-allowed"
          :class="{ 'hover:bg-gray-600': currentPage !== 1 && !isLoading }"
          @click="changePage(currentPage - 1)"
        >
          <svg
            class="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M15 19l-7-7 7-7"
            ></path>
          </svg>
        </button>

        <div class="flex gap-1">
          <button
            v-if="currentPage > 3"
            :disabled="isLoading"
            class="px-3 py-1 rounded-md bg-gray-700 hover:bg-gray-600 text-white disabled:opacity-50 disabled:cursor-not-allowed"
            @click="changePage(1)"
          >
            1
          </button>

          <span v-if="currentPage > 4" class="px-2 py-1 text-white">...</span>

          <button
            v-for="page in [
              ...(currentPage > 2 ? [currentPage - 2] : []),
              ...(currentPage > 1 ? [currentPage - 1] : []),
              currentPage,
              ...(currentPage < totalPages ? [currentPage + 1] : []),
              ...(currentPage < totalPages - 1 ? [currentPage + 2] : []),
            ].filter((p) => p > 0 && p <= totalPages)"
            :key="page"
            :disabled="isLoading"
            class="px-3 py-1 rounded-md text-white disabled:opacity-50 disabled:cursor-not-allowed"
            :class="
              page === currentPage
                ? 'bg-blue-600'
                : 'bg-gray-700 hover:bg-gray-600'
            "
            @click="changePage(page)"
          >
            {{ page }}
          </button>

          <span v-if="currentPage < totalPages - 3" class="px-2 py-1 text-white"
            >...</span
          >

          <button
            v-if="currentPage < totalPages - 2"
            :disabled="isLoading"
            class="px-3 py-1 rounded-md bg-gray-700 hover:bg-gray-600 text-white disabled:opacity-50 disabled:cursor-not-allowed"
            @click="changePage(totalPages)"
          >
            {{ totalPages }}
          </button>
        </div>

        <button
          :disabled="currentPage === totalPages || isLoading"
          class="px-3 py-1 rounded-md bg-gray-700 text-white disabled:opacity-50 disabled:cursor-not-allowed"
          :class="{
            'hover:bg-gray-600': currentPage !== totalPages && !isLoading,
          }"
          @click="changePage(currentPage + 1)"
        >
          <svg
            class="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 5l7 7-7 7"
            ></path>
          </svg>
        </button>
      </div>

      <div
        v-if="isLoading"
        class="flex justify-center items-center py-8 flex-col"
      >
        <div class="spinner"></div>
        <div class="text-white mt-2">Загрузка</div>
      </div>

      <div v-else class="flex flex-col gap-4 overflow-y-scroll" style="height: calc(100svh - 64px - 44px - 52px - 60px - 40px - 18px - 45px);">
        <div
          v-for="movie in searchResults"
          :key="movie.id"
          class="flex text-white items-center gap-4 p-4 rounded-xl transition-all duration-300 shadow-lg bg-gray-800 hover:bg-gray-700 border border-gray-700 hover:border-gray-500 hover:shadow-xl group"
        >
          <div
            class="w-16 h-24 flex-shrink-0 overflow-hidden rounded-md shadow-md cursor-pointer"
            @click="openMovieDetails(movie)"
          >
            <img
              :src="movie.image_base64 || movie.image_url || '/movielogo.png'"
              :alt="movie.title"
              class="w-full h-full object-cover"
            />
          </div>
          <div
            class="flex-1 min-w-0 cursor-pointer"
            @click="openMovieDetails(movie)"
          >
            <h3 class="font-bold text-lg line-clamp-1 mb-2 text-white">
              {{ movie.title }}
            </h3>
            <div class="flex items-center gap-4">
              <span
                class="px-2 py-0.5 bg-gradient-to-r from-yellow-500 to-amber-600 rounded-full text-xs font-semibold shadow-inner"
              >
                {{ movie.rating }}/10
              </span>
              <span class="text-sm text-gray-300">{{ movie.year }}</span>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <button
              class="p-2 rounded-full text-gray-300 hover:text-white hover:bg-gray-700 transition-all"
              title="Подробнее"
              @click="openMovieDetails(movie)"
            >
              <svg
                class="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                ></path>
              </svg>
            </button>
            <button
              class="p-2 bg-indigo-600 hover:bg-indigo-700 rounded-full text-white transition-all flex items-center justify-center"
              title="Добавить фильм"
              @click="openCollectionSelector(movie.id)"
            >
              <svg
                class="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 4v16m8-8H4"
                ></path>
              </svg>
            </button>
          </div>
        </div>
      </div>

      <div
        v-if="totalPages > 1"
        class="flex justify-center items-center mt-2 gap-2"
      >
        <button
          :disabled="currentPage === 1 || isLoading"
          class="px-3 py-1 rounded-md bg-gray-700 text-white disabled:opacity-50 disabled:cursor-not-allowed"
          :class="{ 'hover:bg-gray-600': currentPage !== 1 && !isLoading }"
          @click="changePage(currentPage - 1)"
        >
          <svg
            class="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M15 19l-7-7 7-7"
            ></path>
          </svg>
        </button>

        <div class="flex gap-1">
          <button
            v-if="currentPage > 3"
            :disabled="isLoading"
            class="px-3 py-1 rounded-md bg-gray-700 hover:bg-gray-600 text-white disabled:opacity-50 disabled:cursor-not-allowed"
            @click="changePage(1)"
          >
            1
          </button>

          <span v-if="currentPage > 4" class="px-2 py-1 text-white">...</span>

          <button
            v-for="page in [
              ...(currentPage > 2 ? [currentPage - 2] : []),
              ...(currentPage > 1 ? [currentPage - 1] : []),
              currentPage,
              ...(currentPage < totalPages ? [currentPage + 1] : []),
              ...(currentPage < totalPages - 1 ? [currentPage + 2] : []),
            ].filter((p) => p > 0 && p <= totalPages)"
            :key="page"
            :disabled="isLoading"
            class="px-3 py-1 rounded-md text-white disabled:opacity-50 disabled:cursor-not-allowed"
            :class="
              page === currentPage
                ? 'bg-blue-600'
                : 'bg-gray-700 hover:bg-gray-600'
            "
            @click="changePage(page)"
          >
            {{ page }}
          </button>

          <span v-if="currentPage < totalPages - 3" class="px-2 py-1 text-white"
            >...</span
          >

          <button
            v-if="currentPage < totalPages - 2"
            :disabled="isLoading"
            class="px-3 py-1 rounded-md bg-gray-700 hover:bg-gray-600 text-white disabled:opacity-50 disabled:cursor-not-allowed"
            @click="changePage(totalPages)"
          >
            {{ totalPages }}
          </button>
        </div>

        <button
          :disabled="currentPage === totalPages || isLoading"
          class="px-3 py-1 rounded-md bg-gray-700 text-white disabled:opacity-50 disabled:cursor-not-allowed"
          :class="{
            'hover:bg-gray-600': currentPage !== totalPages && !isLoading,
          }"
          @click="changePage(currentPage + 1)"
        >
          <svg
            class="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 5l7 7-7 7"
            ></path>
          </svg>
        </button>
      </div>
    </div>
    <div
      v-else-if="searchInputContent && !isLoading"
      class="flex flex-col items-center mt-8 pb-20"
    >
      <h1 class="text-3xl text-white mb-4">Фильм не найден</h1>
    </div>
    <div class="flex flex-col items-center pb-20">
      <RouterLink to="/create">
        <button
          class="px-4 py-2 center bg-blue-600 hover:bg-blue-700 text-white rounded-md"
        >
          Добавьте свой
        </button>
      </RouterLink>
    </div>
    <div
      v-if="isLoading && !searchResults.length"
      class="flex justify-center items-center py-8 flex-col"
    >
      <div class="spinner"></div>
      <div class="text-white mt-2">Загрузка</div>
    </div>

    <MovieInfoModal
      :movie="selectedMovie"
      :is-keyboard-open="isKeyboardOpen"
      :is-loading="isLoading"
      :is-search-context="false"
      @close="selectedMovie = null"
      @add-to-collection="openCollectionSelector"
    />

    <transition name="fade-scale">
      <div
        v-if="showCollectionSelector"
        class="fixed inset-0 bg-black bg-opacity-50 z-50"
        @click="showCollectionSelector = false"
      ></div>
    </transition>
    <transition name="modal-fade">
      <div
        v-if="showCollectionSelector"
        class="fixed inset-0 flex items-center justify-center p-4 z-50"
        :class="{ 'pb-keyboard': isKeyboardOpen }"
        @click="showCollectionSelector = false"
      >
        <div
          class="bg-gray-800 rounded-xl w-full max-w-md p-6 border border-gray-700 shadow-2xl modal-content"
          @click.stop
        >
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-bold text-white">Выберите коллекцию</h2>
            <button
              class="text-gray-400 hover:text-white"
              @click="showCollectionSelector = false"
            >
              <svg
                class="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M6 18L18 6M6 6l12 12"
                ></path>
              </svg>
            </button>
          </div>

          <div
            v-if="isLoadingCollections"
            class="flex justify-center items-center py-4 flex-col"
          >
            <div class="spinner"></div>
            <div class="text-white mt-2">Загрузка</div>
          </div>

          <div
            v-else-if="collections.length === 0"
            class="text-center text-white py-4"
          >
            У вас нет коллекций. Создайте новую коллекцию.
          </div>

          <div v-else class="max-h-60 overflow-y-auto scrollbar-hide">
            <div
              v-for="collection in collections"
              :key="collection.id"
              class="p-3 mb-2 rounded-lg bg-gray-700 transition-colors relative"
              :class="{
                'opacity-50 cursor-not-allowed': addingToCollection,
                'hover:bg-gray-600 cursor-pointer': !addingToCollection,
              }"
              @click="
                !addingToCollection &&
                addMovieToCollection(selectedMovieId, Number(collection.id))
              "
            >
              <div class="flex items-center justify-between">
                <div>
                  <h3 class="font-medium text-white">{{ collection.name }}</h3>
                  <p class="text-sm text-gray-300 truncate">
                    {{ collection.description }}
                  </p>
                </div>
                <div
                  v-if="
                    addingToCollection &&
                    selectedCollectionId === Number(collection.id)
                  "
                  class="spinner-small"
                ></div>
              </div>
            </div>
          </div>

          <div class="mt-4 flex justify-end">
            <button
              class="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-md mr-2"
              @click="showCollectionSelector = false"
            >
              Отмена
            </button>
            <button
              class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-md"
              @click="showCreateCollectionModal = true; showCollectionSelector = false;"
            >
              Создать коллекцию
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- New Collection Creation Modal -->
    <transition name="fade-scale">
      <div
        v-if="showCreateCollectionModal"
        class="fixed inset-0 bg-black bg-opacity-50 z-50"
        @click="showCreateCollectionModal = false"
      ></div>
    </transition>
    <transition name="modal-fade">
      <div
        v-if="showCreateCollectionModal"
        class="fixed inset-0 flex items-center justify-center p-4 z-50"
        :class="{ 'pb-keyboard': isKeyboardOpen }"
        @click="showCreateCollectionModal = false"
      >
        <div
          class="bg-gray-800 rounded-xl w-full max-w-md p-6 border border-gray-700 shadow-2xl modal-content"
          @click.stop
        >
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-bold text-white">Создать коллекцию</h2>
            <button
              class="text-gray-400 hover:text-white"
              @click="showCreateCollectionModal = false"
            >
              <svg
                class="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M6 18L18 6M6 6l12 12"
                ></path>
              </svg>
            </button>
          </div>

          <div class="mt-4">
            <div class="mb-4">
              <label for="collectionName" class="block text-sm font-medium text-gray-300 mb-1">Название коллекции</label>
              <input
                id="collectionName"
                v-model="newCollection.name"
                type="text"
                class="w-full p-2 bg-gray-700 text-white rounded-lg border border-gray-600 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none"
                placeholder="Введите название коллекции"
              />
            </div>
            <div class="mb-4">
              <label for="collectionDescription" class="block text-sm font-medium text-gray-300 mb-1">Описание (необязательно)</label>
              <textarea
                id="collectionDescription"
                v-model="newCollection.description"
                class="w-full p-2 bg-gray-700 text-white rounded-lg border border-gray-600 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none resize-none h-24"
                placeholder="Введите описание коллекции"
              ></textarea>
            </div>
          </div>

          <div class="mt-4 flex justify-end">
            <button
              class="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-md mr-2"
              @click="showCreateCollectionModal = false"
            >
              Отмена
            </button>
            <button
              :disabled="isCreatingCollection || !newCollection.name"
              class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-md disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              @click="createCollectionAndAddMovie"
            >
              <div
                v-if="isCreatingCollection"
                class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"
              ></div>
              <span>{{ isCreatingCollection ? 'Создание...' : 'Создать' }}</span>
            </button>
          </div>
        </div>
      </div>
    </transition>

    <transition name="fade-scale">
      <div
        v-if="showAIModal"
        class="fixed inset-0 bg-black opacity-50 z-40"
        @click="showAIModal = false"
      ></div>
    </transition>
    <transition name="modal-fade">
      <div
        v-if="showAIModal"
        class="fixed inset-0 bg-opacity-60 backdrop-blur-sm z-50 flex items-center justify-center p-4"
        :class="{ 'pb-keyboard': isKeyboardOpen }"
        @click="showAIModal = false"
      >
        <div
          class="ai-modal w-full max-w-lg p-6 shadow-2xl transform transition-all modal-content"
          @click.stop
        >
          <div class="flex justify-between items-start mb-4">
            <div>
              <h2 class="text-2xl font-bold text-white mb-2">
                Поиск с помощью нейросети
              </h2>
              <p class="text-gray-300 text-sm">
                Опишите фильм своими словами, если не помните точное название.
                Например:
              </p>
              <ul class="text-gray-400 text-sm mt-2">
                <li>"Фильм про космонавта, застрявшего на Марсе"</li>
              </ul>
            </div>
            <button
              class="text-gray-400 hover:text-white transition-colors"
              @click="showAIModal = false"
            >
              <svg
                class="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M6 18L18 6M6 6l12 12"
                ></path>
              </svg>
            </button>
          </div>

          <div class="mt-4">
            <textarea
              v-model="aiSearchQuery"
              class="w-full h-24 p-3 bg-gray-700/50 text-white rounded-lg border border-gray-600/30 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none resize-none backdrop-blur-sm"
              placeholder="Опишите фильм, который ищете..."
              @keydown.enter.prevent="handleAISearch"
            ></textarea>
          </div>

          <div class="mt-4 flex justify-end gap-3">
            <button
              class="px-4 py-2 bg-gray-700/50 hover:bg-gray-600/50 text-white rounded-md backdrop-blur-sm transition-all"
              @click="showAIModal = false"
            >
              Отмена
            </button>
            <button
              :disabled="isLoading"
              class="ai-search-button px-4 py-2 text-white rounded-md flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
              @click="handleAISearch"
            >
              <div
                v-if="isLoading"
                class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"
              ></div>
              <span>{{ isLoading ? 'Поиск...' : 'Найти фильм' }}</span>
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';

import { search, searchAI } from '@/api/search';
import {
  getCollections,
  addFilmToCollection,
  createFilm,
  getAllMovies,
  createCollection,
} from '@/api/collections';
import { Collection, Movie } from '@/api/types';
import { Axios } from '@/api';

import { useViewStore } from '@/services/stores';

import MovieInfoModal from '@/components/MovieInfoModal.vue';

declare global {
  interface Window {
    initialWindowHeight?: number;
  }
}

interface SearchMovie extends Partial<Movie> {
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

interface SearchResponse {
  results: SearchMovie[];
  total_pages: number;
  total_results: number;
}

const router = useRouter();
const viewStore = useViewStore();
const searchInput = ref<HTMLInputElement | null>(null);
const searchInputContent = ref<string>('');
const searchTimeout = ref<number | null>(null);
const searchData = ref<SearchResponse | null>(null);
const isLoading = ref<boolean>(false);
const selectedMovie = ref<SearchMovie | null>(null);
const currentPage = ref<number>(1);
const totalPages = ref<number>(0);

const showCollectionSelector = ref<boolean>(false);
const selectedMovieId = ref<number | null>(null);
const selectedMovieData = ref<SearchMovie | null>(null);
const collections = ref<Collection[]>([]);
const isLoadingCollections = ref<boolean>(false);
const addingToCollection = ref<boolean>(false);
const selectedCollectionId = ref<number | null>(null);

const showAIModal = ref<boolean>(false);
const aiSearchQuery = ref<string>('');

const showCreateCollectionModal = ref<boolean>(false);
const newCollection = ref<{ name: string; description: string }>({
  name: '',
  description: '',
});
const isCreatingCollection = ref<boolean>(false);

const isKeyboardOpen = ref<boolean>(false);

const searchResults = computed<SearchMovie[]>(() => {
  if (!searchData.value || !searchData.value.results) return [];
  return searchData.value.results.map((movie) => ({
    id: movie.id,
    title: movie.title,
    rating: movie.rating,
    year: movie.year,
    image_url: movie.image_url,
    image_base64: movie.image_base64,
    description: movie.description,
    genre: movie.genre || '',
    loaded_from_tmdb: movie.loaded_from_tmdb,
    user_added: movie.user_added,
  }));
});

onMounted(() => {
  if (searchInput.value) {
    searchInput.value.focus();
  }

  window.addEventListener('resize', detectKeyboard);

  window.visualViewport?.addEventListener('resize', handleVisualViewportResize);

  detectKeyboard();
});

onBeforeUnmount(() => {
  window.removeEventListener('resize', detectKeyboard);
  window.visualViewport?.removeEventListener(
    'resize',
    handleVisualViewportResize,
  );
});

const handleVisualViewportResize = () => {
  if (window.visualViewport) {
    const heightDiff = window.innerHeight - window.visualViewport.height;
    isKeyboardOpen.value = heightDiff > 150;
  }
};

const detectKeyboard = () => {
  const windowHeight = window.innerHeight;

  if (!window.initialWindowHeight) {
    window.initialWindowHeight = windowHeight;
  }

  isKeyboardOpen.value =
    window.initialWindowHeight &&
    window.initialWindowHeight - windowHeight > 150;
};

const handleSearchInput = (): void => {
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value);
  }

  searchTimeout.value = window.setTimeout(() => {
    currentPage.value = 1;
    performSearch();
  }, 1000);
};

const performSearch = async (): Promise<void> => {
  if (!searchInputContent.value.trim()) {
    searchData.value = null;
    return;
  }

  isLoading.value = true;
  try {
    const res = await search(searchInputContent.value, currentPage.value);
    searchData.value = res;
    totalPages.value = res.total_pages;
  } catch (error) {
    console.error('Search error:', error);
    searchData.value = null;
  } finally {
    isLoading.value = false;
  }
};

const changePage = (page: number): void => {
  if (page < 1 || page > totalPages.value || page === currentPage.value) return;
  currentPage.value = page;
  performSearch();
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

const openMovieDetails = (movie: SearchMovie): void => {
  selectedMovie.value = movie;
  selectedMovieData.value = movie;
};

const openCollectionSelector = (movieId: number): void => {
  if (selectedMovie.value && selectedMovie.value.id === movieId) {
    selectedMovieId.value = movieId;
    selectedMovieData.value = selectedMovie.value;
    selectedMovie.value = null;
    showCollectionSelector.value = true;
    fetchCollections();
    return;
  }

  const movie = searchResults.value.find((m) => m.id === movieId);
  if (movie) {
    selectedMovieId.value = movieId;
    selectedMovieData.value = movie;
    selectedMovie.value = null;
    showCollectionSelector.value = true;
    fetchCollections();
  }
};

const fetchCollections = async (): Promise<void> => {
  isLoadingCollections.value = true;
  try {
    const collectionsData = await getCollections();
    collections.value = collectionsData;
  } catch (error) {
    console.error('Error fetching collections:', error);
  } finally {
    isLoadingCollections.value = false;
  }
};

const addMovieToCollection = async (
  movieId: number,
  collectionId: number,
): Promise<void> => {
  if (addingToCollection.value) return;

  addingToCollection.value = true;
  selectedCollectionId.value = collectionId;
  try {
    const movie = selectedMovieData.value;
    if (!movie) {
      throw new Error('Movie data not found');
    }

    const allMovies = await getAllMovies();
    const existingMovie = allMovies.find(
      (m) => m.title.toLowerCase() === movie.title.toLowerCase(),
    );

    let finalMovieId = movieId;

    if (existingMovie) {
      console.log(
        'Movie already exists in database, using existing ID:',
        existingMovie.id,
      );
      finalMovieId = existingMovie.id;
    } else if (movie.loaded_from_tmdb || !movie.user_added) {
      const movieData = {
        title: movie.title,
        description: movie.description || '',
        image_url: movie.image_url || '',
        image_base64: movie.image_base64 || '',
        rating: movie.rating || 0,
        genre: movie.genre || '',
        year: movie.year || 0,
        user_added: true,
        loaded_from_tmdb: movie.loaded_from_tmdb || false,
      };

      const addedMovie = await createFilm(movieData);

      if (addedMovie && addedMovie.id) {
        finalMovieId = addedMovie.id;
      }
    }

    await addFilmToCollection(finalMovieId, collectionId);
    showCollectionSelector.value = false;
    viewStore.showNotification('Фильм успешно добавлен в коллекцию', 'success');
  } catch (error) {
    console.error('Error adding movie to collection:', error);
    viewStore.showNotification(
      'Ошибка при добавлении фильма в коллекцию',
      'error',
    );
  } finally {
    addingToCollection.value = false;
    selectedCollectionId.value = null;
  }
};

const handleMovieClick = (id: number): void => {
  selectedMovie.value = null;
  router.push(`/movie/${id}`);
};

const dismissKeyboard = (): void => {
  if (document.activeElement instanceof HTMLElement) {
    document.activeElement.blur();
  }

  if (searchInput.value) {
    searchInput.value.blur();
  }
};

const handleAISearch = async (): Promise<void> => {
  if (!aiSearchQuery.value.trim()) {
    viewStore.showNotification('Введите описание фильма', 'warning');
    return;
  }

  isLoading.value = true;
  try {
    const filmName = await searchAI(aiSearchQuery.value);
    if (filmName) {
      showAIModal.value = false;
      searchInputContent.value = filmName;
      await performSearch();
    } else {
      viewStore.showNotification(
        'Нейросеть не смогла найти подходящий фильм',
        'warning',
      );
    }
  } catch (error) {
    console.error('AI search error:', error);
    viewStore.showNotification(
      'Произошла ошибка при использовании нейросети',
      'error',
    );
  } finally {
    isLoading.value = false;
  }
};

const createCollectionAndAddMovie = async (): Promise<void> => {
  if (!newCollection.value.name || isCreatingCollection.value) return;
  
  isCreatingCollection.value = true;
  try {
    // Create a simple collection object without initialUsers
    const payload = {
      name: newCollection.value.name,
      description: newCollection.value.description || '',
      isDefault: false,
      initialUsers: []
    };

    // Make direct API call to avoid the issue with user ID
    const { data: createdCollection } = await Axios.post('/collections/', payload);
    
    if (createdCollection) {
      // Add movie to the newly created collection
      const movie = selectedMovieData.value;
      if (!movie) {
        throw new Error('Movie data not found');
      }

      const allMovies = await getAllMovies();
      const existingMovie = allMovies.find(
        (m) => m.title.toLowerCase() === movie.title.toLowerCase(),
      );

      let finalMovieId = selectedMovieId.value;

      if (existingMovie) {
        console.log(
          'Movie already exists in database, using existing ID:',
          existingMovie.id,
        );
        finalMovieId = existingMovie.id;
      } else if (movie.loaded_from_tmdb || !movie.user_added) {
        const movieData = {
          title: movie.title,
          description: movie.description || '',
          image_url: movie.image_url || '',
          image_base64: movie.image_base64 || '',
          rating: movie.rating || 0,
          genre: movie.genre || '',
          year: movie.year || 0,
          user_added: true,
          loaded_from_tmdb: movie.loaded_from_tmdb || false,
        };

        const addedMovie = await createFilm(movieData);

        if (addedMovie && addedMovie.id) {
          finalMovieId = addedMovie.id;
        }
      }

      if (createdCollection.id) {
        await addFilmToCollection(finalMovieId, Number(createdCollection.id));
        
        // Reset form and close modal
        newCollection.value = { name: '', description: '' };
        showCreateCollectionModal.value = false;
        
        viewStore.showNotification('Коллекция создана и фильм добавлен', 'success');
      } else {
        // If we don't have the collection ID, try to find it by name
        const collections = await getCollections();
        const newCollectionId = collections.find(c => c.name === newCollection.value.name)?.id;
        
        if (newCollectionId) {
          await addFilmToCollection(finalMovieId, Number(newCollectionId));
          
          // Reset form and close modal
          newCollection.value = { name: '', description: '' };
          showCreateCollectionModal.value = false;
          
          viewStore.showNotification('Коллекция создана и фильм добавлен', 'success');
        } else {
          throw new Error('Не удалось найти созданную коллекцию');
        }
      }
    }
  } catch (error) {
    console.error('Error creating collection and adding movie:', error);
    viewStore.showNotification(
      'Ошибка при создании коллекции',
      'error',
    );
  } finally {
    isCreatingCollection.value = false;
  }
};
</script>

<style>
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}

.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-from .modal-content,
.modal-fade-leave-to .modal-content {
  transform: scale(0.9);
  opacity: 0;
}

.modal-fade-enter-active .modal-content,
.modal-fade-leave-active .modal-content {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.modal-fade-enter-to .modal-content,
.modal-fade-leave-from .modal-content {
  transform: scale(1);
  opacity: 1;
}

.fade-scale-enter-active,
.fade-scale-leave-active {
  transition: opacity 0.25s ease;
}

.fade-scale-enter-from,
.fade-scale-leave-to {
  opacity: 0;
}

.spinner-small {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.1);
  border-top-color: rgba(255, 255, 255, 0.8);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.loading .spinner-small {
  display: block;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.generate-button {
  background: linear-gradient(135deg, #d946ef, #db2777, #f59e0b, #ec4899);
  box-shadow: 0 0 15px rgba(219, 39, 119, 0.6);
  position: relative;
  overflow: hidden;
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
  transform-origin: center;
  animation: gradient-animation 5s ease infinite;
  background-size: 300% 300%;
  border: none;
  will-change: transform, box-shadow;
}

.generate-button:hover {
  box-shadow: 0 0 20px rgba(219, 39, 119, 0.8);
  transform: scale(1.03);
}

.generate-button:before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  z-index: -1;
  background: linear-gradient(
    135deg,
    #f59e0b,
    #ec4899,
    #d946ef,
    #db2777,
    #f59e0b
  );
  background-size: 400% 400%;
  border-radius: 28px;
  filter: blur(5px);
  opacity: 0.7;
  animation: gradient-animation 8s ease infinite;
  will-change: background-position;
}

@keyframes gradient-animation {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.spinner {
  width: 50px;
  height: 50px;
  position: relative;
  margin: 10px auto;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.spinner:before {
  content: '';
  box-sizing: border-box;
  position: absolute;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 4px solid #2563eb;
  border-right-color: transparent;
  border-bottom-color: transparent;
  transform: rotate(-45deg);
  animation: spinner-rotate 1s linear infinite;
}

@keyframes spinner-rotate {
  0% {
    transform: rotate(-45deg);
  }
  100% {
    transform: rotate(315deg);
  }
}

.ai-modal {
  position: relative;
  background: linear-gradient(
    135deg,
    rgba(31, 41, 55, 0.8),
    rgba(17, 24, 39, 0.9)
  );
  backdrop-filter: blur(12px);
  border: none;
  box-shadow:
    0 0 30px rgba(217, 70, 239, 0.2),
    0 0 60px rgba(219, 39, 119, 0.15),
    0 0 100px rgba(245, 158, 11, 0.1);
  transform-origin: center;
  border-radius: 1rem;
}

.ai-modal:before {
  content: '';
  position: absolute;
  inset: -2px;
  background: linear-gradient(135deg, #d946ef, #db2777, #f59e0b, #ec4899);
  background-size: 400% 400%;
  border-radius: 1rem;
  z-index: -1;
  animation: gradient-animation 8s ease infinite;
  opacity: 0.7;
}

.ai-modal:after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    135deg,
    rgba(31, 41, 55, 0.9),
    rgba(17, 24, 39, 0.95)
  );
  border-radius: 0.95rem;
  z-index: -1;
}

.ai-search-button {
  background: linear-gradient(135deg, #d946ef, #db2777);
  position: relative;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  transform-origin: center;
}

.ai-search-button:hover {
  transform: scale(1.03);
  box-shadow: 0 0 20px rgba(219, 39, 119, 0.3);
  background: linear-gradient(135deg, #e355f7, #e93a86);
}

.ai-search-button:before {
  content: '';
  position: absolute;
  inset: -2px;
  background: linear-gradient(135deg, #e355f7, #e93a86);
  z-index: -1;
  filter: blur(8px);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.ai-search-button:hover:before {
  opacity: 0.5;
}

.pb-keyboard {
  padding-bottom: 40vh !important;
  justify-content: flex-start !important;
  padding-top: 10vh !important;
}
</style>
