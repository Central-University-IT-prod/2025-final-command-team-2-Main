<script setup lang="ts">
import { onMounted, ref } from 'vue';

import LoadingSpinner from '@/components/LoadingSpinner.vue';

import { deleteCollection, getCollections } from '@/api/collections.js';
import { Collection } from '@/api/types';

import router from '@/services/router';
import { useViewStore } from '@/services/stores';

const collections = ref<Collection[]>([]);
const loadingCollectionId = ref<string | null>(null);
const viewStore = useViewStore();

onMounted(async () => {
	await loadCollections();
});

const loadCollections = async () => {
	const data = await getCollections();
	collections.value = data;
	console.log('Collections:', collections.value);
};

const handleDelete = async (collectionId: string) => {
	loadingCollectionId.value = collectionId;
	try {
		await deleteCollection(collectionId);
		await loadCollections();
		viewStore.showNotification('Коллекция успешно удалена', 'success');
	} catch (error) {
		console.error('Error deleting collection:', error);
		viewStore.showNotification('Ошибка при удалении коллекции', 'error');
	} finally {
		loadingCollectionId.value = null;
	}
};

const handleClick = (event: MouseEvent) => {
	if ((event.target as HTMLElement).tagName !== 'BUTTON') {
		router.push(`/collections/${(event.currentTarget as HTMLElement).id}`);
	}
	console.log();
};
</script>

<template>
	<div class="m-4 relative min-h-screen">
		<h1 class="mb-5 text-3xl text-white">Коллекции</h1>

		<div
			v-if="collections.length === 0"
			class="w-full min-h-[4rem] flex items-center justify-center text-xl text-white bg-[#3A3F47] p-4 rounded-lg"
		>
			Нет коллекций
		</div>

		<div
			v-for="collection in collections"
			v-else
			:id="collection.id"
			:key="collection.id"
			class="w-full min-h-[4rem] flex items-center justify-between text-xl text-white bg-[#3A3F47] p-4 rounded-lg hover:bg-[#43454A] transition-colors duration-300 mb-2"
			@click="handleClick"
		>
			<h2>{{ collection.name }}</h2>

			<button
				v-if="!collection.isDefault"
				class="hover:text-red-400 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
				:disabled="loadingCollectionId === collection.id"
				@click="handleDelete(collection.id)"
			>
				<LoadingSpinner v-if="loadingCollectionId === collection.id" />
				<span v-else>×</span>
			</button>
		</div>

		<!-- Плавающая кнопка -->
		<button
			class="fixed bottom-16 right-8 w-14 h-14 rounded-2xl text-white text-4xl flex items-center justify-center shadow-lg"
			@click=""
		>
			<svg
				xmlns="http://www.w3.org/2000/svg"
				x="0px"
				y="0px"
				width="30"
				height="30"
				viewBox="0 0 24 24"
			>
				<path
					fill="white"
					fill-rule="evenodd"
					d="M 11 2 L 11 11 L 2 11 L 2 13 L 11 13 L 11 22 L 13 22 L 13 13 L 22 13 L 22 11 L 13 11 L 13 2 Z"
				></path>
			</svg>
		</button>
	</div>
	<div>
		<!-- Плавающая кнопка -->
		<RouterLink to="/collections/create">
			<button
				class="fixed bottom-16 right-8 w-14 h-14 rounded-2xl text-white text-4xl flex items-center justify-center shadow-lg"
				@click=""
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					x="0px"
					y="0px"
					width="30"
					height="30"
					viewBox="0 0 24 24"
				>
					<path
						fill="white"
						fill-rule="evenodd"
						d="M 11 2 L 11 11 L 2 11 L 2 13 L 11 13 L 11 22 L 13 22 L 13 13 L 22 13 L 22 11 L 13 11 L 13 2 Z"
					></path>
				</svg>
			</button>
		</RouterLink>
	</div>
</template>

<style scoped>
/* Дополнительные стили при необходимости */
</style>
