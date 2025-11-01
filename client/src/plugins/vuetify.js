import 'vuetify/styles';
import { createVuetify } from 'vuetify';
import { aliases, mdi } from 'vuetify/iconsets/mdi';

// 🌞 Light theme
const myCustomLightTheme = {
	dark: false,
	colors: {
		background: '#fceddbff',
		surface: '#FFFFFF',
		primary: '#1976D2',
		secondary: '#03DAC6',
		error: '#B00020',
		info: '#2196F3',
		success: '#4CAF50',
		warning: '#FB8C00',
		text: '#1E1E1E',
	},
};

// 🌚 Dark theme
const myCustomDarkTheme = {
	dark: true,
	colors: {
		background: '#121212',
		surface: '#1E1E1E',
		primary: '#90CAF9',
		secondary: '#03DAC6',
		error: '#CF6679',
		info: '#2196F3',
		success: '#4CAF50',
		warning: '#FB8C00',
		text: '#FFFFFF',
	},
};

// 🌿 Forest theme
const forestTheme = {
	dark: true,
	colors: {
		background: '#1b2621',
		surface: '#26332d',
		primary: '#81c784',
		secondary: '#a5d6a7',
		text: '#e8f5e9',
	},
};

// 🌸 Sakura theme
const sakuraTheme = {
	dark: false,
	colors: {
		background: '#ffeef2',
		surface: '#ffffff',
		primary: '#e91e63',
		secondary: '#f8bbd0',
		text: '#4a148c',
	},
};

export const vuetify = createVuetify({
	icons: {
		defaultSet: 'mdi',
		aliases,
		sets: { mdi },
	},
	theme: {
		defaultTheme: 'myCustomLightTheme',
		themes: {
			myCustomLightTheme,
			myCustomDarkTheme,
			forestTheme,
			sakuraTheme,
		},
	},
});

export default vuetify;
