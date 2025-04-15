import { defineStore } from 'pinia';

export const useViewStore = defineStore('view', {
	state: () => {
		return {
			isSearch: false,
			currentPage: 1,

			data: [],
			notification: {
				show: false,
				message: '',
				type: 'success', // 'success', 'error', 'info'
			},
		};
	},
	actions: {
		changeSearch() {
			this.isSearch = !this.isSearch;
			console.log(this.isSearch);
		},
		hideSearch() {
			this.isSearch = false;
		},
		changePage(page) {
			this.currentPage = page;
		},
		updateData(newData) {
			this.data = newData;
			console.log(this.data);
		},
		showNotification(message, type = 'success') {
			this.notification = {
				show: true,
				message,
				type,
			};

			setTimeout(() => {
				this.hideNotification();
			}, 1500);
		},
		hideNotification() {
			this.notification.show = false;
		},
	},
});
