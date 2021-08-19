<script>
	import { nanoid } from 'nanoid';
	import { onMount } from 'svelte';

	onMount(() => {
		location.href = `/p/${nanoid(8)}`;
	});
</script>
