<script>
	import { onMount } from 'svelte';
	import Highlight from 'svelte-highlight';
	import python from 'svelte-highlight/src/languages/python';
	import github from 'svelte-highlight/src/styles/github-dark';

	let items, last;

	const fetch_snippets = async () => {
		try {
			const res = await fetch('/api/snippets');
			const data = await res.json();
			if (res.ok) {
				items = data.items;
				last = data.last;
			} else {
				console.log('error occured');
			}
		} catch (err) {
			console.error(err);
		}
	};

	onMount(async () => {
		await fetch_snippets();
	});
</script>

<svelte:head>
	{@html github}
	<style>
		pre {
			padding: 5%;
			background-color: #0a0e14;
			font-size: medium;
			font-family: 'Fira Code', monospace;
		}
	</style>
</svelte:head>

<nav class="navbar navbar-expand-lg navbar-dark bg-dark" style="background-color: #0A0E14;">
	<div class="container-fluid">
		<a class="navbar-brand" href="/">Home</a>
		<a class="navbar-brand" href="/p">Playground</a>
	</div>
</nav>

<div class="container">
	{#if items}
		{#each items as item}
			<div
				class="card"
				style="width: 100%; padding: 3%;  display: flex;
			justify-content: center;
			align-items: center;"
			>
				<div style="width: 40%; ">
					<Highlight language={python} code={item.code} />
				</div>
				<div class="card-body">
					{#if item.description}
						<h5 class="card-title">{item.description}</h5>
					{/if}
					<a href="/p/{item.key}" target="_blank" class="shadow-none btn btn-primary"
						>Open in playground</a
					>
				</div>
			</div>
			<hr />
		{/each}
	{:else}
		<h3>Fetching Snippets...</h3>
	{/if}
</div>
