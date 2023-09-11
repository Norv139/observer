<script>
    export let name;
    export let discription;
    export let start;
    export let code;
    export let status;

    export let process;
    export let id;
    export let token;
</script>

<section>
    <h2>{name}</h2>
    <p> {code} {status} {discription}</p>
    <p>{start}</p>
    <button>stop</button>
</section>

<style>
    section{
        color: #131313;
        background-color: #d3d3d3;
        border: 2px solid #131313;
        border-radius: 15px;
        padding: 10px;
        min-width: 200px;
        text-align: start;
    }
    section *{
        margin: 5px;
    }
</style>