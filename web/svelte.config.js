import adapter from "@sveltejs/adapter-static"

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		// hydrate the <div id="svelte"> element in src/app.html
		target: '#svelte',
		adapter: adapter({
			pages: 'build',
			assets: 'build',
			fallback: 'index.html'
		}),
		ssr: false,
		vite: {
			optimizeDeps: {
				include: ["highlight.js/lib/core"]
			}
		}
	}
};

export default config;
