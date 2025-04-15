<script setup>
import { computed, defineProps } from 'vue';

// Определяем props с валидацией и значениями по умолчанию
const props = defineProps({
	title: {
		type: String,
		default: 'Безымянный фильм',
		required: true,
	},
	rating: {
		type: Number,
		default: 0,
	},
	year: {
		type: Number,
		default: 0,
	},
	imageSrc: {
		type: String,
		default: '/ImageCross.png',
	},
});

// Динамическая цветовая схема для рейтинга
const ratingColor = computed(() => {
	if (props.rating >= 8)
		return 'bg-gradient-to-r from-yellow-500 to-orange-500';
	if (props.rating >= 5) return 'bg-gradient-to-r from-gray-500 to-gray-700';
	return 'bg-gradient-to-r from-red-500 to-red-700';
});
</script>

<template>
	<article
		class="w-30 h-50 movie-card relative rounded-xl overflow-hidden group transition-all duration-500 ease-out aspect-[2/3] bg-gradient-to-b from-gray-900 to-black"
		role="article"
		aria-labelledby="movie-title"
		tabindex="0"
	>
		<!-- Image Container -->
		<div class="relative h-full w-full overflow-hidden">
			<img
				:src="props.imageSrc"
				class="object-cover w-full h-full transition-transform duration-700 ease-out group-hover:scale-110"
				:alt="`Обложка фильма ${props.title}`"
				loading="lazy"
				decoding="async"
			/>

			<!-- Dynamic Overlay with Subtle Noise -->
			<div
				class="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent mix-blend-overlay pointer-events-none"
			></div>
			<div
				class="absolute inset-0 opacity-10 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My ...')] transition-opacity duration-500 group-hover:opacity-20"
			></div>

			<!-- Glow Effect -->
			<div
				class="absolute inset-0 bg-gradient-to-t from-transparent to-white/10 blur-md transition-all duration-500 group-hover:blur-lg"
			></div>
		</div>

		<!-- Content Container -->
		<div
			class="absolute inset-x-0 bottom-0 p-5 space-y-3 transition-all duration-500 ease-out transform translate-y-4 group-hover:translate-y-0"
		>
			<!-- Title -->
			<h2
				id="movie-title"
				class="text-xl text-white font-semibold leading-tight tracking-tight line-clamp-2 drop-shadow-md"
			>
				{{ props.title }}
			</h2>

			<!-- Meta Info -->
			<div
				class="flex items-center gap-3 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
			>
				<span
					:class="ratingColor"
					class="px-2 py-0.5 text-xs font-medium text-white rounded-full shadow-md"
				>
					{{ props.rating }}/10
				</span>
				<span class="text-sm text-gray-300 font-medium">{{ props.year }}</span>
			</div>
		</div>

		<!-- Action Buttons -->
		<div
			class="absolute top-3 right-3 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300"
		>
			<button
				class="p-2 bg-white/90 rounded-full shadow-lg hover:bg-white transition-colors duration-200"
				aria-label="Добавить в избранное"
			>
				<svg
					class="w-5 h-5 text-gray-800"
					fill="none"
					stroke="currentColor"
					viewBox="0 0 24 24"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M12 4v16m8-8H4"
					/>
				</svg>
			</button>
			<button
				class="p-2 bg-white/90 rounded-full shadow-lg hover:bg-white transition-colors duration-200"
				aria-label="Подробнее"
			>
				<svg
					class="w-5 h-5 text-gray-800"
					fill="none"
					stroke="currentColor"
					viewBox="0 0 24 24"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M9 5l7 7-7 7"
					/>
				</svg>
			</button>
		</div>
	</article>
</template>

<style scoped>
.movie-card {
	box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
	transition: box-shadow 0.3s ease-out;
}

.movie-card:hover {
	box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
}

/* Accessibility */
.movie-card:focus-within {
	outline: 2px solid #3b82f6;
	outline-offset: 2px;
}

/* Smooth Transitions */
img,
.movie-card {
	transition-timing-function: cubic-bezier(0.23, 1, 0.32, 1);
}

/* Subtle Grain Effect */
.movie-card::before {
	content: '';
	position: absolute;
	inset: 0;
	pointer-events: none;
	z-index: 10;
}
</style>
