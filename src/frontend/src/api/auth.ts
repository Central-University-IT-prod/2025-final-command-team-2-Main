import { Axios } from '.';
import { useMiniApp } from 'vue-tg';

import { TGUser } from './types';

export const auth = async (): Promise<TGUser> => {
	const initData = useMiniApp().initData;

	try {
		const user = JSON.parse(new URLSearchParams(initData).get('user'));
		console.log(initData, user);
		if (!Axios.defaults.headers.common['Authorization']) {
			const debugToken = localStorage.getItem('debug');

			if (debugToken) {
				Axios.defaults.headers.common['Authorization'] = `Bearer ${debugToken}`;
			} else {
				const { data } = await Axios.post('/auth/telegram', {
					telegramId: user?.id,
					username: user?.username,
					avatarUrl: user?.photo_url,
				});

				// localStorage.setItem('token', data.token);

				Axios.defaults.headers.common['Authorization'] = `Bearer ${data.token}`;
			}
		}
		return user;
	} catch (error) {
		console.warn('no telegram', error);
	}
};
