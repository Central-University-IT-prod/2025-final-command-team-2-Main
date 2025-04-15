<template>
	<transition name="fade-scale">
		<div
			v-if="movie"
			class="fixed inset-0 bg-black opacity-50 z-40"
			@click="$emit('close')"
		></div>
	</transition>
	<transition name="modal-fade">
		<div
			v-if="movie"
			class="fixed inset-0 bg-opacity-60 backdrop-blur-sm flex items-center justify-center z-50 p-4"
			:class="{ 'pb-keyboard': isKeyboardOpen }"
			@click="$emit('close')"
		>
			<div
				class="bg-gray-800 rounded-xl max-w-sm w-full max-h-[80vh] overflow-y-auto p-6 border border-gray-700 shadow-2xl scrollbar-hide modal-content"
				@click.stop
			>
				<div class="flex justify-between items-start mb-4">
					<h2 class="text-2xl font-bold text-white">{{ movie.title }}</h2>
					<button
						class="text-gray-400 hover:text-white"
						@click="$emit('close')"
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

				<div class="flex flex-col sm:flex-row gap-4 mb-4">
					<img
						:src="
							movie.loaded_from_tmdb
								? movie.image_base64
								: movie.image_url && movie.image_url !== 'null'
									? movie.image_url
									: '/movielogo.png'
						"
						:alt="movie.title"
						class="w-full h-auto object-cover rounded-lg shadow-md"
					/>
					<div class="flex flex-col gap-3">
						<div class="flex items-center gap-2">
							<span
								v-if="movie.rating >= 0"
								class="px-2 py-1 bg-gradient-to-r from-yellow-500 to-amber-600 rounded-full text-sm font-semibold shadow-inner text-white"
							>
								{{ movie.rating }}/10
							</span>
							<span
								v-if="movie.year >= 0"
								class="text-gray-300"
								>{{ movie.year }}</span
							>
						</div>
						<p
							v-if="movie.description !== 'null'"
							class="text-gray-300 text-sm line-clamp-4"
						>
							{{ movie.description }}
						</p>
						<p
							v-else
							class="text-gray-400 text-sm italic"
						>
							Описание отсутствует
						</p>
					</div>
				</div>

				<button
					v-if="isSearchContext"
					class="w-full py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-md transition-colors flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
					:disabled="isLoading"
					@click="$emit('add-to-collection', movie.id)"
				>
					<LoadingSpinner v-if="isLoading" />
					<span>{{ isLoading ? 'Добавление...' : 'Добавить фильм' }}</span>
				</button>
			</div>
		</div>
	</transition>
</template>

<script setup lang="ts">
import { defineEmits, defineProps } from 'vue';

import type { SearchMovie } from '@/api/types';

import LoadingSpinner from './LoadingSpinner.vue';

defineProps<{
	movie: SearchMovie | null;
	isKeyboardOpen: boolean;
	isLoading: boolean;
	isSearchContext?: boolean;
}>();

defineEmits<{
	(e: 'close'): void;
	(e: 'add-to-collection', id: number): void;
}>();
</script>

<style scoped>
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

.scrollbar-hide::-webkit-scrollbar {
	display: none;
}

.scrollbar-hide {
	-ms-overflow-style: none;
	scrollbar-width: none;
}
</style>
