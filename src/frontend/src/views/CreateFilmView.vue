<template>
	<div
		class="create-film-container flex flex-col h-full"
		@click="dismissKeyboard"
	>
		<div class="flex items-center py-2">
			<h1 class="text-3xl font-bold text-white mx-4">Добавление фильма</h1>
		</div>

		<div class="overflow-y-auto flex-1 pb-20">
			<form
				class="text-white flex flex-col gap-6 pt-4"
				@submit.prevent="onSubmit"
				@click="e => e.stopPropagation()"
			>
				<label for="title">
					<h3 class="mb-2 text-xl text-white">Название фильма</h3>
					<input
						id="title"
						v-model="form.title"
						required
						name="title"
						class="w-full outline-none border-none rounded-2xl p-2 bg-[#3A3F47] text-white placeholder:italic"
						type="text"
						placeholder="Название"
						tabindex="1"
						@keydown.enter="($refs.year as HTMLInputElement).focus()"
					/>
				</label>

				<label for="genre">
					<h3 class="mb-2 text-xl text-white">Жанр</h3>
					<input
						id="genre"
						ref="genre"
						v-model="form.genre"
						required
						name="genre"
						class="w-full outline-none border-none rounded-2xl p-2 bg-[#3A3F47] text-white placeholder:italic"
						type="text"
						placeholder="Жанр"
						tabindex="4"
						@keydown.enter="($refs.description as HTMLInputElement).focus()"
					/>
				</label>

				<h4
					class="text-xl ml-5 cursor-pointer"
					@click="
						e => {
							e.stopPropagation();
							showAdvanced = !showAdvanced;
						}
					"
				>
					<span>{{ showAdvanced ? 'Скрыть' : 'Добавить' }}</span> подробности
				</h4>

				<div
					ref="advancedSection"
					class="flex flex-col gap-6 overflow-hidden transition-all duration-300"
					:style="{ maxHeight: showAdvanced ? advancedHeight + 'px' : '0px' }"
				>
					<label for="year">
						<h3 class="mb-2 text-xl text-white">Год</h3>
						<input
							id="year"
							ref="year"
							v-model.number="form.year"
							name="year"
							class="w-full outline-none border-none rounded-2xl p-2 bg-[#3A3F47] text-white placeholder:italic"
							type="number"
							placeholder="Год"
							tabindex="2"
							@keydown.enter="($refs.image_url as HTMLInputElement).focus()"
						/>
					</label>

					<label for="image_url">
						<h3 class="mb-2 text-xl text-white">Ссылка на постер</h3>
						<input
							id="image_url"
							ref="image_url"
							v-model="form.image_url"
							name="image_url"
							class="w-full outline-none border-none rounded-2xl p-2 bg-[#3A3F47] text-white placeholder:italic"
							type="text"
							placeholder="Оставьте ссылку на постер"
							tabindex="3"
							@keydown.enter="($refs.genre as HTMLInputElement).focus()"
						/>
					</label>

					<label for="description">
						<h3 class="mb-2 text-xl text-white">Описание</h3>
						<input
							id="description"
							ref="description"
							v-model="form.description"
							name="description"
							class="w-full outline-none border-none rounded-2xl p-2 bg-[#3A3F47] text-white h-20 placeholder:italic"
							type="text"
							placeholder="Опишите фильм"
							tabindex="5"
							@keydown.enter="($refs.duration as HTMLInputElement).focus()"
						/>
					</label>

					<label for="duration">
						<h3 class="mb-2 text-xl text-white">Длительность</h3>
						<input
							id="duration"
							ref="duration"
							v-model.number="form.duration"
							name="duration"
							class="w-full outline-none border-none rounded-2xl p-2 bg-[#3A3F47] text-white placeholder:italic"
							type="number"
							placeholder="Длительность"
							tabindex="6"
							@keydown.enter="($refs.rating as HTMLInputElement).focus()"
						/>
					</label>

					<label for="rating">
						<h3 class="mb-2 text-xl text-white">Оценка</h3>
						<input
							id="rating"
							ref="rating"
							v-model.number="form.rating"
							name="rating"
							class="w-full outline-none border-none rounded-2xl p-2 bg-[#3A3F47] text-white placeholder:italic"
							type="number"
							placeholder="Оценка"
							tabindex="7"
						/>
					</label>
				</div>

				<MainButton
					text="Добавить фильм"
					:progress="isLoading"
					class="mt-4 mb-4"
					@click="handleButtonClick"
				/>
			</form>
		</div>
	</div>
</template>

<script setup lang="ts">
import { nextTick, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { MainButton } from 'vue-tg';

import {
	addFilmToCollection,
	createFilm,
	getCollections,
} from '@/api/collections.js';
import { CreateFilmType } from '@/api/types';

import router from '@/services/router';

const showAdvanced = ref(false);

const advancedSection = ref<HTMLElement | null>(null);

const advancedHeight = ref(0);

const isLoading = ref(false);

onMounted(async () => {
	await nextTick();

	if (advancedSection.value) {
		advancedSection.value.style.maxHeight = 'none';

		advancedHeight.value = advancedSection.value.offsetHeight;

		advancedSection.value.style.maxHeight = '0px';
	}
});

const form = ref<CreateFilmType>({
	title: '',
	genre: '',
	year: 0,
	image_url: '',
	description: '',
	duration: 0,
	rating: 0,
});

const dismissKeyboard = () => {
	if (document.activeElement instanceof HTMLElement) {
		document.activeElement.blur();
	}
};

const handleButtonClick = (event?: Event) => {
	if (event && typeof event.stopPropagation === 'function') {
		event.stopPropagation();
	}

	onSubmit();
};

const onSubmit = async () => {
	try {
		isLoading.value = true;

		const formData = { ...form.value };

		for (const key in formData) {
			if (formData[key] === '') {
				formData[key] = 'null';
			} else if (formData[key] === 0) {
				formData[key] = -1;
			}
		}

		const filmId = await createFilm(formData);

		const data = await getCollections();

		const defaultCollection = data.find(collection => collection.isDefault);

		if (defaultCollection) {
			await addFilmToCollection(filmId.id, Number(defaultCollection.id));
		}

		router.push('/');
	} catch (error) {
		console.error('Ошибка:', error);
	} finally {
		isLoading.value = false;
	}
};
</script>

<style scoped>
.create-film-container {
	max-width: 800px;
	margin: 0 auto;
	padding: 20px;
	max-height: 100vh;
	overflow-y: auto;
}

:global(html, body) {
	height: 100%;
	overflow: auto;
}
</style>
