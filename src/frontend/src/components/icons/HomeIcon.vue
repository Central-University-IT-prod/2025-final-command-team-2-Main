<template>
	<svg
		width="20"
		height="22"
		viewBox="0 0 20 22"
		fill="none"
		xmlns="http://www.w3.org/2000/svg"
	>
		<path
			:stroke="isActive ? '#FFFFFF' : '#67686D'"
			d="M15.5245 21H13.7817H6.3487H4.6059C2.86855 21 1.46014 19.4607 1.46014 17.5618V8.84736C1.46683 8.09967 1.78828 7.39702 2.33154 6.94256L8.26578 1.6853C9.30997 0.771566 10.7943 0.771566 11.8385 1.6853L17.7989 6.93303C18.3401 7.38935 18.661 8.09083 18.6703 8.83784V17.5618C18.6703 19.4607 17.2619 21 15.5245 21Z"
			stroke-width="2"
			stroke-linecap="round"
			stroke-linejoin="round"
		/>
	</svg>
</template>
<script>
export default {
	name: 'HomeOutlined',
	props: {
		isActive: {
			type: Boolean,
			default: false,
		},
	},
};
</script>
