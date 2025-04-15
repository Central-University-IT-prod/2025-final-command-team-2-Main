<template>
	<div class="text-white p-4">
		<div class="flex items-center justify-between py-2">
			<RouterLink to="/">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					class="h-6 w-6 text-white"
					fill="none"
					viewBox="0 0 24 24"
					stroke="currentColor"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M15 19l-7-7 7-7"
					/>
				</svg>
			</RouterLink>
			<button>
				<svg
					width="22"
					height="24"
					viewBox="0 0 22 24"
					fill="white"
					xmlns="http://www.w3.org/2000/svg"
				>
					<path
						fill-rule="evenodd"
						clip-rule="evenodd"
						d="M10.6963 18.6316L5.32373 21.881C4.89477 22.1271 4.3663 21.9529 4.12982 21.4874V21.4874C4.0614 21.3432 4.02449 21.1834 4.02203 21.0206V6.62244C4.02203 3.87644 5.7217 2.77805 8.16756 2.77805H13.9133C16.2845 2.77805 18.0588 3.80322 18.0588 6.43937V21.0206C18.0588 21.2804 17.9653 21.5295 17.7989 21.7132C17.6326 21.8968 17.4069 22 17.1716 22C17.0216 21.9974 16.874 21.9567 16.7405 21.881L11.3347 18.6316C11.1355 18.5128 10.8955 18.5128 10.6963 18.6316Z"
						stroke="white"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
					/>
				</svg>
			</button>
		</div>

		<div
			v-if="movie"
			class="flex flex-col gap-6 mt-6"
		>
			<div class="flex items-start gap-6">
				<img
					:src="movie.imageSrc || '/movielogo.png'"
					alt="poster"
					class="w-48 h-72 object-cover rounded-xl"
				/>
				<div class="flex-1">
					<h1 class="text-3xl font-bold text-white mb-4">{{ movie.title }}</h1>
					<div class="flex items-center gap-4 text-[#92929D] mb-6">
						<div class="flex items-center gap-2">
							<svg
								class="w-5 h-5"
								fill="none"
								viewBox="0 0 16 17"
								stroke="currentColor"
							>
								<path
									d="M13 2.81712H3C2.72386 2.81712 2.5 3.04098 2.5 3.31712V13.3171C2.5 13.5933 2.72386 13.8171 3 13.8171H13C13.2761 13.8171 13.5 13.5933 13.5 13.3171V3.31712C13.5 3.04098 13.2761 2.81712 13 2.81712Z"
									stroke-linecap="round"
									stroke-linejoin="round"
								/>
								<path
									d="M11 1.81712V3.81712"
									stroke-linecap="round"
									stroke-linejoin="round"
								/>
								<path
									d="M5 1.81712V3.81712"
									stroke-linecap="round"
									stroke-linejoin="round"
								/>
								<path
									d="M2.5 5.81712H13.5"
									stroke-linecap="round"
									stroke-linejoin="round"
								/>
							</svg>
							<span>{{ movie.duration }} мин</span>
						</div>
						<div class="w-px h-6 bg-[#92929D]/50"></div>
						<div class="flex items-center gap-2">
							<svg
								class="w-5 h-5"
								fill="none"
								viewBox="0 0 16 17"
								stroke="currentColor"
							>
								<path
									d="M6 4.21737V13.2174"
									stroke-linecap="round"
									stroke-linejoin="round"
								/>
								<path
									d="M1.5 11.1668C1.49998 11.0516 1.53979 10.9399 1.61268 10.8507C1.68557 10.7615 1.78706 10.7003 1.89995 10.6774C2.35166 10.5851 2.75763 10.3396 3.04919 9.98246C3.34075 9.62531 3.5 9.17842 3.5 8.71737C3.5 8.25633 3.34075 7.80943 3.04919 7.45229C2.75763 7.09514 2.35166 6.84966 1.89995 6.75737C1.78706 6.73445 1.68557 6.67321 1.61268 6.58402C1.53979 6.49483 1.49998 6.38317 1.5 6.26798V4.71737C1.5 4.58476 1.55268 4.45759 1.64645 4.36382C1.74021 4.27005 1.86739 4.21737 2 4.21737H14C14.1326 4.21737 14.2598 4.27005 14.3536 4.36382C14.4473 4.45759 14.5 4.58476 14.5 4.71737V6.26798C14.5 6.38317 14.4602 6.49483 14.3873 6.58402C14.3144 6.67321 14.2129 6.73446 14.1001 6.75737C13.6483 6.84966 13.2424 7.09514 12.9508 7.45229C12.6592 7.80944 12.5 8.25633 12.5 8.71738C12.5 9.17842 12.6592 9.62531 12.9508 9.98246C13.2424 10.3396 13.6483 10.5851 14.1001 10.6774C14.2129 10.7003 14.3144 10.7615 14.3873 10.8507C14.4602 10.9399 14.5 11.0516 14.5 11.1668V12.7174C14.5 12.85 14.4473 12.9772 14.3536 13.0709C14.2598 13.1647 14.1326 13.2174 14 13.2174H2C1.86739 13.2174 1.74021 13.1647 1.64645 13.0709C1.55268 12.9772 1.5 12.85 1.5 12.7174V11.1668Z"
									stroke-linecap="round"
									stroke-linejoin="round"
								/>
							</svg>
							<span>{{ movie.genre }}</span>
						</div>
					</div>
					<div class="flex items-center gap-4 mb-8">
						<div
							:class="{
								'bg-gradient-to-r from-yellow-500 to-orange-500':
									movie.rating >= 8,
								'bg-gradient-to-r from-gray-500 to-gray-700':
									movie.rating >= 5 && movie.rating < 8,
								'bg-gradient-to-r from-red-500 to-red-700': movie.rating < 5,
							}"
							class="px-4 py-1 rounded-full text-white font-medium"
						>
							{{ movie.rating }}/10
						</div>
						<span class="text-white/80 text-lg">{{ movie.year }}</span>
					</div>
				</div>
			</div>

			<div class="space-y-6">
				<div>
					<h2 class="text-xl font-semibold text-white mb-3">Описание</h2>
					<p class="text-white/80 leading-relaxed">{{ movie.description }}</p>
				</div>

				<div class="grid grid-cols-2 gap-6">
					<div>
						<h3 class="text-white/70 mb-2">Страна</h3>
						<p class="text-white">{{ movie.country || '—' }}</p>
					</div>
					<div>
						<h3 class="text-white/70 mb-2">Режиссёр</h3>
						<p class="text-white">{{ movie.director || '—' }}</p>
					</div>
				</div>
			</div>
		</div>

		<div
			v-else
			class="text-center py-20 text-white/50"
		>
			Фильм не найден
		</div>
	</div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

import { useViewStore } from '@/services/stores.js';

const route = useRoute();
const viewStore = useViewStore();
const isLoading = ref(true);

const movie = computed(() =>
	viewStore.data.find(item => item.id === Number(route.params.id)),
);

onMounted(async () => {
	try {
		if (viewStore.data.length === 0) {
			await viewStore.fetchData();
		}
	} catch (error) {
		console.error('Ошибка загрузки данных:', error);
	} finally {
		isLoading.value = false;
	}
});
</script>
