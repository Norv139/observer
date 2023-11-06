async function getStatus() {
    const response = await fetch('http://127.0.0.1:3000/status');
    return await response.json();
    
}

async function postCreateBot(data){
    const url = 'http://127.0.0.1:3000/create'
    const response = await fetch(url, {
            method: 'POST',
            headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
    return await response.json()
}
export { getStatus, postCreateBot};
