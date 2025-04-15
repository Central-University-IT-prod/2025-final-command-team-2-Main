<template>
	<HomeComponent v-if="!useViewStore().isSearch" />
	<SearchComponent v-else />
</template>
<script setup lang="ts">
import HomeComponent from '@/components/HomeComponent.vue';
import SearchComponent from '@/components/SearchComponent.vue';

import { useViewStore } from '@/services/stores.js';

useViewStore().hideSearch();

console.log(useViewStore().data);
useViewStore().updateData([
	{
		id: 1,
		title: 'The Shawshank Redemption',
		description:
			'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
		rating: '9.3',
		genre: 'Drama',
		date: '1994-09-23',
		duration: '2h 22min',
		imgUrl:
			'https://m.media-amazon.com/images/M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFmNTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg',
		watchLink: 'https://www.imdb.com/title/tt0111161/',
	},
]);
console.log(useViewStore().data);
</script>
