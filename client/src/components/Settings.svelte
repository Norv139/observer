<script>
    import { DateTime } from 'luxon'
    import { postCreateBot } from '../utils';
    export let reloadFn;
    export let closeFn;

    let showInfo = false;
    let inputName = null;
    let inputToken = null;
    let inputIdGuild = null;
    let toggleType = 'target';

    $: listGuilds = [];
    $: listTarget = listGuilds.filter(item => item.type == "target");
    $: listIgnore = listGuilds.filter(item => item.type == "ignore");
    $: incrimentId = listGuilds.length !== 0 ? listGuilds[listGuilds.length-1].id + 1 : 1;
    $: formVisibility = 'normal'; // 'normal' | "ok" | "error"

    function addGuildFn() {
        if(inputIdGuild !== null){
            listGuilds = [
            ...listGuilds, { 
                id: incrimentId, 
                type: toggleType, 
                idGuild: listGuilds.length !== 0 
                    ? listGuilds[listGuilds.length-1].id + 1 
                    : 1
            } ]
        }
    }
    function deleteFn(delItem) {
        // console.log(delItem, listGuilds)
        listGuilds = listGuilds.filter(item => item.id != delItem.id)
    }
    const clearFormFn = () => {
        inputName = null;
        inputToken = null;
        toggleType = 'target';
        listGuilds = [];
        // listTarget = [];
        // listIgnore = [];
    }
    const submitFn = ()=>{
        if (inputToken == null){
            alert("no token");
            return 
        }
        postCreateBot({
            token: inputToken, 
            name: inputName == null ? `bot_${DateTime.now().toFormat("yyMMddHHmmss")}` : inputName, 
            target: listTarget, 
            ignore: listIgnore
        })
        .then(()=>{
            formVisibility = 'ok';
            clearFormFn()
            reloadFn()
            setTimeout(closeFn, 1000)
        })
        .catch(()=>{formVisibility = 'error'; setTimeout(()=>{formVisibility='ok'}, 5000)})
    }
    
</script>

<div class="settings" style="--show-info:{showInfo ? "blok":"none"}">
    <button class="close" on:click={closeFn}>x</button>
    <div style="
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
    ">
        <h1>settings</h1> <button on:click={()=>{showInfo=!showInfo}}>!</button>
    </div>

    {#if formVisibility == 'normal'}
    <div class="form">
    <div  class="form-line">
        <div class="info">
            <div>
                <h3>name</h3>
                <p>token discord аккаунта</p>
            </div>
        </div>
        <p>name:</p> 
        <input id="name" bind:value={inputName}>
        
    </div>

    <div  class="form-line">
        <div class="info">
            <div>
                <h3>token</h3>
                <p> token discord аккаунта</p>
            </div>
        </div>
        <p>token:</p> 
        <input id="token" bind:value={inputToken}>
    </div>
    <div class="list">
        <p style="color: #676767;">сервер не может адекватно обработать ignore & trget</p>
    </div>
<!--    
    <div class="form-line">
        <div class="info">
            <div>
                <h3>ig guild</h3>
                <p>id дискорд сервера</p>
                <p>target - записывать действия только с этих серверов</p>
                <p>ignore - записывать все кроме этого сервера</p>
                <p>если есть список target, то лист ignore не используеться</p>
            </div>
        </div>
        <p>id guild:</p>
        <input type="number" bind:value={inputIdGuild}>
        <button on:click={()=>{toggleType = toggleType == 'ignore' ? 'target' : 'ignore'}}>
            {toggleType}
        </button >
        <button on:click={()=>{
            // alert(`${toggleType} ${listGuilds}`)
            addGuildFn()
        }}>
            +
        </button>
    </div>
    <div class="form-list">
        <p class="form-list_tetle">target:</p>
        <ul class="list">
            {#each listTarget as itemTarget}
                <ol class="list-item">
                    <button on:click={()=>{
                        // console.log(itemTarget)
                        deleteFn(itemTarget)
                    }}>
                        -
                    </button>
                    <p class="list-item_text">
                        id Guild: {itemTarget.idGuild}
                    </p>
                </ol>
            {/each}
        </ul>
    </div>
    <div class="form-list">
        <div> 
            <div style="display: flex; text-align: center; gap:5px;">
                
                {#if listTarget.length > 0 && listIgnore.length > 0}
                    <div class="info">
                        <div>
                            <h3>!</h3>
                            <p>все эти сервера не будут учитываться в обработке </p>
                        </div>
                    </div>
                {/if} 
                <p class="form-list_tetle">ignore:</p>

            </div>
        </div>

        <ul class="list">
            {#each listIgnore as itemIgnore}
                <ol class="list-item">
                    <button on:click={()=>{
                        console.log(itemIgnore)
                        deleteFn(itemIgnore)
                    }}>
                        -
                    </button>
                    <p class="list-item_text">
                        id Guild: {itemIgnore.idGuild}
                    </p>
                </ol>
            {/each}
        </ul>
    </div> -->
        
    <button class="submit-btn" on:click={submitFn}>submit</button>

    </div>
        {:else if formVisibility == 'ok'}
            <h1>OK</h1>
        {:else}
            <h1>ERROR</h1>
    {/if}

</div>

<style>
    .submit-btn{
        margin-top: 10px;
        color: black;
        background-color: white;
    }
    .info{
        position: relative;
        background-color: rgb(255, 231, 76);
        color: rgb(0, 0, 0);
        width: 24px;
        height: 24px;
        border-radius: 20px;
        text-align: center !important;
        gap: 5px;
        display: var(--show-info);
    }
    .info::after{
        content: "!";
    }
    .info div{
        display: none;
    }
    .info div *{
        margin: 0;
    }
    .info div h1, h2, h3, h4, h5, h6{
        text-align: center;
    }
    .info:hover div{
        position: absolute;
        z-index: 11;

        box-sizing: border-box;

        word-wrap: inherit;
        text-wrap: inherit;
        left: 24px;
        top: 10px;
        

        min-width: 30vw;
        max-width: 55vw;
        padding: 10px;

        border-radius:  0 20px 20px 20px;

        text-align: start;
        align-items: start;

        display: block;
        color: rgb(0, 0, 0);

        background-color: rgb(255, 255, 255);
    }

    

    .list{
        margin-top: 5px !important;
        max-height: 100px;
        overflow-y: scroll;
        border: 2px solid #4b4b4b;
        text-align: start;
        padding: 0;
        align-items: center;
        text-align: center;
        color: white;
    }
    .list-item{
        display: flex;
        align-items: start;
        padding: 0;
        margin: 0;
        align-items: center;
        text-align: center;
        gap: 10px;

    }
    /* 
    border-top: 2px solid #4b4b4b;
    border-bottom: 2px solid #4b4b4b;
     */
    .list-item{
        border-top: none;
        border-bottom: none;
    }
    .list-item:last-child{
        border-bottom: 2px solid #4b4b4b;
    }

    .list-item:not(:first-child){
        border-top: 2px solid #4b4b4b;
    }

    .list-item:nth-child(n+3){
        border-top: 2px solid #4b4b4b;
        border-bottom: none;
    }

    .list-item *{
        color: white;
        padding: 0;
    }
    .list-item button{
        height: 30px;
        width: 30px;
        text-align: center;
        margin-left: 10px;
    }

    .close{
        position: absolute;
        top: 10px;
        left: 10px;
        background-color: inherit;
    }

    .form{
        display: flex;
        flex-direction: column;
        /* height: 60%;
        overflow-x: scroll; */
        overflow-y: visible;
        padding: 5px;
        gap: 10px;
    }
    

    .form-list{
        display: flex;
        flex-direction: column;
    }
    .form-list *{
        margin: 0;
        padding: 0;
        text-align: start;
    }
    .form-list_tetle{
        color: #57e641;
    }

    .form-line{
        display: flex;
        align-items: center;
        justify-content: start;
        gap: 5px;
        flex-wrap: wrap;

    }
    

    .form-line button{
        padding: 5px;
        height: 30px;
        min-width: 30px;
        align-items: center;
        text-align: center;
    }

    .settings{
        top: 0;
        left: 0;
        box-sizing: border-box;
        position: relative;
        width: 80vw;
        min-height: 20%;
        max-height: 80%;
        overflow: auto;
        border-radius: 20px;
        padding: 10px 10%;
        background-color: #242424;
        margin: 0 auto;
    }
    .settings h1{
        padding: 0;
        margin: 20px 0;
    }

    .list-item_text{
        padding: 10px;
        color: white;
        /* border-right: 2px solid #4b4b4b; */
        border-left: 2px solid #4b4b4b;
    }

</style>