<script context="module">
	export async function load({ page }) {
		return {
			props: {
				last: page.query.get('last')
			}
		};
	}
</script>

<script>
	import { goto } from '$app/navigation';

	import { onMount } from 'svelte';
	import Highlight from 'svelte-highlight';
	import python from 'svelte-highlight/src/languages/python';
	import github from 'svelte-highlight/src/styles/github';

	let items;
	export let last;

	const fetch_snippets = async () => {
		try {
			let q;
			if (last) q = `/api/snippets?last=${last}`;
			else q = '/api/snippets';
			const res = await fetch(q);
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

<div class="container" style="margin-top: 5%; margin-bottom: 5%;">
	{#if items}
		{#each items as item}
			<div
				class="card"
				style="width: 100%; padding: 3%; margin: 3%; display: flex;
			justify-content: center;
			align-items: center;"
			>
				<div class="card-title">
					{#if item.description}
						<h5 class="card-title">{item.description}</h5>
					{/if}
				</div>
				<div style="width: 100%; ">
					<Highlight language={python} code={item.code} />
				</div>
				<div class="card-body">
					<a href="/p/{item.key}" target="_blank" class="shadow-none btn btn-primary"
						>Open in playground</a
					>
				</div>
			</div>
		{/each}
		<center>
			{#if last}
				<button
					on:click={() => (location.href = `/snippets?last=${last}`)}
					class="btn btn-info shadow-none">Next Page</button
				>
			{:else}
				<button class="btn btn-light" disabled>No More Snippets</button>
			{/if}
		</center>
	{:else}
		<h3>Fetching Snippets...</h3>
	{/if}
</div>
