<script context="module">
	export async function load({ page }) {
		return {
			props: {
				host: page.host,
				slug: page.params.slug
			}
		};
	}
</script>

<script>
	import { onDestroy, onMount } from 'svelte';
	import { pyodide } from '$lib/store';
	let editor;
	let editorTextarea;
	let output = '',
		code = '# Please wait while we check for any code associated with this id';
	let cloudIcon;
	let isNavOpen = false;
	export let slug, host;

	let id, description;

	const setup_pyodide = () => {
		let setup_code = `
import sys, io, traceback
namespace = {}  # use separate namespace to hide run_code, modules, etc.
def run_code(code):
	"""run specified code and return stdout and stderr"""
	out = io.StringIO()
	oldout = sys.stdout
	olderr = sys.stderr
	sys.stdout = sys.stderr = out
	try:
		# change next line to exec(code, {}) if you want to clear vars each time
		exec(code, namespace)
	except:
		traceback.print_exc()

	sys.stdout = oldout
	sys.stderr = olderr
	return out.getvalue()`;
		$pyodide.runPython(setup_code);
	};

	const copyToClipboard = () => {
		document.getElementById('ctc').innerHTML = '<i class="fas fa-clipboard-check"></i>';
		navigator.clipboard.writeText(`https://${host}/p/${id}`);
		setTimeout(() => {
			document.getElementById('ctc').innerHTML = '<i class="fas fa-clipboard"></i>';
		}, 2000);
	};

	const getCodeByID = async () => {
		try {
			const res = await fetch(`/api/code/${id}`);
			const data = await res.json();
			if (data) {
				editor.setValue(data.code);
				description = data.description;
			} else {
				editor.setValue(
					'# looks like a fresh template\n# write some code\n# run some code\n# add description\n# save to cloud\n\nimport this'
				);

				description = 'The Zen of Python';
			}
		} catch (err) {
			console.error(err);
		}
	};

	const uploadCode = async () => {
		editor.save();
		let code = editorTextarea.value;
		cloudIcon.innerHTML = '<i class="fas fa-cloud-upload-alt"></i>';
		try {
			const res = await fetch('/api/save', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ id, code, description })
			});
			const data = await res.json();
			if (res.ok) {
				if (id != data.key) {
					history.replaceState('data to be passed', 'Title of the page', `/p/${data.key}`);
				}
				id = data.key;
			} else {
				console.error('please try again later');
			}
		} catch (err) {
			console.error(err);
		}
		cloudIcon.innerHTML = '<i class="fas fa-cloud"></i>';
	};

	const setupEnvironment = async () => {
		try {
			$pyodide = await loadPyodide({
				indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.18.0/full/'
			});
		} catch (err) {
			console.error(err);
		}
		console.log('python environment is ready');
	};

	const runCode = async () => {
		editor.save();
		$pyodide.globals.set('code_to_run', editorTextarea.value);
		try {
			output = 'Output:\n' + (await $pyodide.runPython('run_code(code_to_run)'));
		} catch (err) {
			console.error(err);
		}
	};

	onMount(async () => {
		id = slug;
		editor = CodeMirror.fromTextArea(editorTextarea, {
			lineNumbers: true,
			language: 'python',
			matchBrackets: true,
			autoCloseBrackets: true,
			theme: 'ayu-dark'
		});
		editor.setSize('100%', '100%');
		await setupEnvironment();
		await setup_pyodide();
		await getCodeByID();
	});

	onDestroy(() => {
		editor = editor.toTextArea();
	});
</script>

<svelte:head>
	<style>
		body {
			overflow-y: hidden; /* Hide vertical scrollbar */
			overflow-x: hidden; /* Hide horizontal scrollbar */
		}
	</style>
</svelte:head>

<!--Navbar start-->
<nav class="navbar navbar-expand-lg" style="background-color: #0A0E14;">
	<div class="container-fluid">
		<a class="navbar-brand" href="/">PyPlay</a>
		<button
			class="navbar-toggler"
			style="color: #0A0E14;"
			type="button"
			on:click={() => (isNavOpen = !isNavOpen)}
			data-bs-toggle="collapse"
			data-bs-target="#navbarSupportedContent"
			aria-controls="navbarSupportedContent"
			aria-expanded="false"
			aria-label="Toggle navigation"
		>
			<span class="navbar-toggler-icon">
				<i class="fas fa-hamburger" style="color:#18BC9C; font-size:28px;" />
			</span>
		</button>
		<div class="collapse navbar-collapse" class:show={isNavOpen} id="navbarSupportedContent">
			{#if $pyodide}
				<form class="d-flex">
					<a href="/" class="shadow-none btn btn-outline-success" type="button"> Home </a>&nbsp;
					<input
						id="snippet-id"
						style="background-color: #0A0E14; border-color: #18BC9C; color: #18BC9C;"
						class="shadow-none form-control me-2"
						type="search"
						placeholder="Snippet ID"
						aria-label="Search"
						readonly
						bind:value={id}
					/>
					<button
						on:click={copyToClipboard}
						id="ctc"
						class="shadow-none btn btn-outline-success"
						type="button"
					>
						<i class="fas fa-clipboard" />
					</button>
					&nbsp;
					<button
						bind:this={cloudIcon}
						id="save"
						class="shadow-none btn btn-outline-success"
						type="button"
						on:click={uploadCode}
					>
						<i class="fas fa-cloud" />
					</button>
					&nbsp;
					<button
						class="btn shadow-none btn-outline-success"
						style="width: 125px; height: 40px;"
						type="button"
						id="run"
						on:click={runCode}
						><i class="fab fa-python" />
						Run</button
					>
				</form>
			{:else}
				<p style="color: #18BC9C;">Loading Environment</p>
			{/if}
		</div>
	</div>
</nav>
<!--Navbar end-->

<div style="display: flex; height: 94%;">
	<textarea class="form-control" id="editor" bind:this={editorTextarea} style="min-height: 100%;"
		>{code}</textarea
	>
	<div class="form-control" style="background-color: #0d121a;">
		<textarea
			placeholder="Add a short description to explain the snippet (max 50 chars)"
			bind:value={description}
			style="height: 20%;border: none;outline: none;color: #18BC9C;width: 100%;background-color: #0d121a;resize:none;"
		/>
		<textarea
			class="form-control"
			id="result"
			style="min-height: 100%; background-color: #0d121a; color: wheat; border-top: none; border-right: none; border-left: #18BC9C;"
			disabled>{output}</textarea
		>
	</div>
</div>

<style>
	#editor {
		resize: none;
	}
</style>
