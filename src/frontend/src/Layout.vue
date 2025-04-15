<script setup>

import { onMounted } from 'vue';
import { useHapticFeedback } from 'vue-tg';

import BookmarkIcon from './components/icons/BookmarkIcon.vue';

import FolderIcon from './components/icons/FolderIcon.vue';

import HomeIcon from './components/icons/HomeIcon.vue';

import router from './services/router';

import { useViewStore } from '@/services/stores.js';



const viewStore = useViewStore();

const hapticFeedback = useHapticFeedback();



const handleClick = () => {

	viewStore.hideSearch();

};



router.beforeEach((to, from) => {

	if (to.path !== from.path) {

		try {

			hapticFeedback.impactOccurred('medium');

		} catch (error) {

			console.warn(error);

		}

	}

});



onMounted(() => {

	handleClick();

	document.body.style.position = 'fixed';

	document.body.style.width = '100%';

	document.body.style.height = '100%';

});

</script>



<template>

	<div class="app-container">

		<main class="main-content">

			<slot />

		</main>

		<footer

			class="bg-[#242A32] h-16 flex justify-around items-center px-10 py-4 w-full shadow-lg fixed bottom-0 left-0 z-30"

		>

			<RouterLink

				v-slot="{ isActive }"

				to="/"

				class="transition-colors duration-200"

				@click="handleClick"

			>

				<HomeIcon :isActive="isActive" />

			</RouterLink>



			<RouterLink

				v-slot="{ isActive }"

				to="/saved"

				class="transition-colors duration-200"

				@click="handleClick"

			>

				<BookmarkIcon :isActive="isActive" />

			</RouterLink>



			<RouterLink

				v-slot="{ isActive }"

				to="/collections"

				class="transition-colors duration-200"

				@click="handleClick"

			>

				<FolderIcon :isActive="isActive" />

			</RouterLink>

		</footer>

	</div>

</template>



<style scoped>

.app-container {

	position: relative;

	height: 100vh;

	height: 100svh;

}



.main-content {

}

</style>

