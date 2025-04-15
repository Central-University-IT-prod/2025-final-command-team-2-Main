<template>
	<div class="flex items-center py-2">
		<h1 class="text-3xl font-bold text-white mx-4">Создать коллекцию</h1>
	</div>

	<form
		class="text-white flex flex-col gap-6 pt-4"
		@submit.prevent="onSubmit"
	>
		<label for="title">
			<h3 class="mb-2 text-xl text-white">Название</h3>
			<input
				id="title"
				v-model="form.name"
				required
				name="title"
				class="w-full outline-none border-none rounded-2xl p-2 bg-[#3A3F47] text-white placeholder:italic"
				type="text"
				placeholder="Название"
				tabindex="1"
				@keydown.enter="($refs.year as HTMLInputElement).focus()"
			/>
		</label>

		<label for="description">
			<h3 class="mb-2 text-xl text-white">Описание</h3>
			<input
				id="description"
				ref="description"
				v-model="form.description"
				required
				name="description"
				class="w-full outline-none border-none rounded-2xl p-2 bg-[#3A3F47] text-white placeholder:italic"
				type="text"
				placeholder="описание"
				tabindex="4"
				@keydown.enter="($refs.button as HTMLInputElement).focus()"
			/>
		</label>

		<button
			ref="button"
			type="submit"
			class="px-4 mb-32 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md mx-auto text-xl mt-4"
			tabindex="8"
		>
			Создать
		</button>
	</form>
</template>

<script setup lang="ts">
import { nextTick, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

import {
	addFilmToCollection,
	createCollection,
	createFilm,
	getCollections,
} from '@/api/collections.js';
import { CreateCollectionRequest, CreateFilmType } from '@/api/types';

import router from '@/services/router';

const form = ref({
	name: '',
	description: '',
});

const onSubmit = async () => {
	try {
		const formData = form.value;

		const data = await getCollections();
		await createCollection(formData.name, formData.description);

		router.push('/');
	} catch (error) {
		console.error('Ошибка:', error);
	}
};
</script>
