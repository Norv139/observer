<script>
  import CardBot from './components/CardBot.svelte';
  import Settings from './components/Settings.svelte';

  import {getStatus} from './utils';

  $: isDisplayOpen = false

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

  let overflow = 'scroll'

  const changeDisplayOpen= () => {
    isDisplayOpen = !isDisplayOpen;
    overflow == 'scroll' 
    ?  (()=>{overflow = 'hidden'; window.document.body.classList.toggle('off-scroll')})()
    : (()=>{overflow = 'scroll'; window.document.body.classList.toggle('off-scroll')})()
  }

  $:promisStatus = getStatus() 
</script>

<main style="--main-overflow:{overflow}" id="main">
  {#await promisStatus }
      <CardBot />
      {:then result } 

      {#each result as unitBot, index}
       <CardBot obj={unitBot } />
      {/each}

      <section class="add-bot">
        <button on:click={changeDisplayOpen}>+</button>
      </section> 

      {:catch error}
      <section class="add-bot">
        error {error}
      </section>
  {/await}

  

  {#if isDisplayOpen}
    <div class="display">
      <Settings reloadFn={()=>{promisStatus = getStatus() }} closeFn={changeDisplayOpen}/>
    </div>
  {/if}
</main>

<style>
  :global(body.off-scroll){
    overflow-x: hidden;
    overflow-y: hidden;
  }
  
  main{
    padding: 0 10px;
    display: flex;
    gap: 10px;
    /* overflow-x: var(--main-overflow); */
  }

  .add-bot button:hover{

    box-shadow: 0 5px  5px #131313;

  }
  .add-bot button{
    width: 80px;
    height: 50px;
  }
  .add-bot{
      position: relative;
      min-width: 200px;
      height: 155px;
      display: flex;
      justify-content: center;
      text-align: center;
      align-items: center;

      border: 2px solid #131313;
      border-radius: 15px;
      padding: 10px;

      color: #131313;
      background-color: #d3d3d3;
    }
  
  .display{
    position: absolute;
    top: 0;
    left: 0;
    

    width: 100vw;
    height: 100vh;

    background-color: #888888a4;

    display: flex;
    justify-content: center;
    align-items: center;
  }


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
