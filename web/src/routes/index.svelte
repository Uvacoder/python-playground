<script>
	import { nanoid } from 'nanoid';
</script>

<div class="container col-xxl-8 px-4 py-5">
	<div class="row flex-lg-row-reverse align-items-center g-5 py-5" style="margin-top: 5%;">
		<div class="col-10 col-sm-8 col-lg-6">
			<img
				src="/_app/python.svg"
				class="d-block mx-lg-auto img-fluid"
				alt="Bootstrap Themes"
				width="500"
				height="300"
				loading="lazy"
			/>
		</div>
		<div class="col-lg-6">
			<h1 class="display-5 fw-bold lh-1 mb-3">PyPlay - The Python Playground</h1>
			<p class="lead">Create, Run, Save and Share Python Code Snippets</p>
			<div class="d-grid gap-2 d-md-flex justify-content-md-start">
				<button
					on:click={() => {
						location.href = `/p/${nanoid(8)}`;
					}}
					type="button"
					class="btn shadow-none btn-primary btn-lg px-4 me-md-2">Playground</button
				>
				<a
					sveltekit:prefetch
					href="/snippets"
					type="button"
					class="btn btn-outline-secondary shadow-none btn-lg px-4">My Snippets</a
				>
			</div>
		</div>
	</div>
</div>
