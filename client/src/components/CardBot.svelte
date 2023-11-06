<script>
    export let obj = null ;
</script>

<section>
    {#if obj != null}
        <h2>{obj.name}</h2>
        <p> {obj.code} {obj.status} {obj.discription}</p>
        <p> {obj.start} </p>
        <button>stop</button>
        {:else}
        <h2>Loading...</h2>
    {/if}
    
</section>

<style>
    section{
        color: #131313;
        background-color: #d3d3d3;
        border: 2px solid #131313;
        border-radius: 15px;
        padding: 10px;
        min-width: 200px;
        height: 155px;
        text-align: start;
        overflow: hidden;
    }
    section *{
        margin: 5px;
    }
</style>