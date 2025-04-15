import { createRouter, createWebHistory } from 'vue-router';

import Home from '../views/HomeView.vue';
import NotFound from '../views/NotFound.vue';

import CreateFilmView from '@/views/CreateFilmView.vue';
import SavedView from '@/views/SavedView.vue';

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{ path: '/', component: Home, name: 'Home' },
		{
			path: '/create',
			component: () => import('../views/CreateFilmView.vue'),
			name: 'Create',
		},
		{ path: '/saved', component: SavedView, name: 'Saved' },
		{
			path: '/collections',
			component: () => import('../views/CollectionsView.vue'),
			name: 'Collections',
		},
		{
			path: '/details/:id',
			component: () => import('../views/DetailsView.vue'),
			name: 'Details',
		},
		{
			path: '/collections/:id',
			component: () => import('../views/CollectionView.vue'),
			name: 'Details',
		},
		{ path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound },
		{
			path: '/collections/create',
			component: () => import('../views/CreateCollectionView.vue'),
			name: 'CreateCollection',
		},
	],
});

router.beforeEach((to, from, next) => {
	if (!to.query.ref) {
		const query = { ...to.query, ref: from.path };
		next({ ...to, query });
	} else {
		next();
	}
});

export default router;
