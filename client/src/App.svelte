<script>
  import svelteLogo from './assets/svelte.svg'
  import viteLogo from '/vite.svg'
  import Counter from './lib/Counter.svelte'
  import CardBot from './components/CardBot.svelte';

  let obj =   {
    "id": 1,
    "name": "test_1",
    "token": "hide",
    "code": 1,
    "status": "stoped",
    "discription": "null",
    "start": "2023-09-11 15:24:41",
    "process": null
  }

</script>

<main>
  <CardBot 
    {...obj}
  />
</main>

<style>
  .logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
    transition: filter 300ms;
  }
  .logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
  }
  .logo.svelte:hover {
    filter: drop-shadow(0 0 2em #ff3e00aa);
  }
  .read-the-docs {
    color: #888;
  }
</style>
