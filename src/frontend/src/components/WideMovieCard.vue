<!-- MovieCard.vue -->
<script setup>
import LoadingSpinner from './LoadingSpinner.vue';

const props = defineProps({
  title: {
    type: String,
    default: '',
  },
  rating: {
    type: Number,
    default: -1,
  },
  genre: {
    type: String,
    default: '',
  },
  date: {
    type: Number,
    default: -1,
  },
  duration: {
    type: Number,
    default: -1,
  },
  imgUrl: {
    type: String,
    default: '',
  },
  showDelete: {
    type: Boolean,
    default: false,
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['click', 'delete']);

const handleDelete = (e) => {
  e.stopPropagation();
  emit('delete');
};
</script>

<template>
  <div
    class="group relative flex items-center gap-6 p-4 bg-gradient-to-tl from-gray-900 to-gray-800 rounded-2xl shadow-[0_0_10px_rgba(0,0,0,0.3)] hover:shadow-xl transition-all duration-300 cursor-pointer"
    @click="$emit('click')"
  >
    <div class="relative shrink-0">
      <img
        :src="props.imgUrl"
        class="w-20 h-28 object-cover rounded-lg shadow-md transform group-hover:scale-105 transition-transform duration-300"
        alt="movie poster"
      />
      <div
        v-if="props.rating >= 0"
        class="absolute -top-2 -right-2 bg-orange-500 rounded-full px-2 py-1 text-xs font-bold shadow-lg"
      >
        {{ props.rating }}
      </div>
    </div>

    <div class="flex-1 min-w-0 pr-12">
      <h2
        class="text-lg font-bold text-white mb-2 truncate group-hover:text-orange-400 transition-colors"
      >
        {{ props.title }}
      </h2>

      <div class="flex flex-wrap gap-4 text-sm">
        <div v-if="props.genre" class="flex items-center gap-2 text-gray-300">
          <svg class="w-4 h-4 shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path
              d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z"
            />
          </svg>
          <span class="truncate">{{ props.genre }}</span>
        </div>

        <div
          v-if="props.date >= 0"
          class="flex items-center gap-2 text-gray-300"
        >
          <svg class="w-4 h-4 shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path
              fill-rule="evenodd"
              d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z"
              clip-rule="evenodd"
            />
          </svg>
          <span class="truncate">{{ props.date }}</span>
        </div>

        <div
          v-if="props.duration >= 0"
          class="flex items-center gap-2 text-gray-300"
        >
          <svg class="w-4 h-4 shrink-0" fill="currentColor" viewBox="0 0 20 20">
            <path
              fill-rule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"
              clip-rule="evenodd"
            />
          </svg>
          <span class="truncate">{{ props.duration }} мин</span>
        </div>
      </div>
    </div>

    <button
      v-if="showDelete"
      :disabled="isLoading"
      class="absolute right-4 top-1/2 -translate-y-1/2 p-2.5 rounded-full bg-red-500/10 hover:bg-red-500 text-red-500 hover:text-white transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
      title="Удалить фильм"
      @click="handleDelete"
    >
      <LoadingSpinner v-if="isLoading" />
      <svg
        v-else
        class="w-5 h-5"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
        />
      </svg>
    </button>
  </div>
</template>

<style scoped>
.line-clamp-1 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
}
</style>
