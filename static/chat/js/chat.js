const user =  JSON.parse(document.querySelector('#current_user').textContent);
const friendId = JSON.parse(document.querySelector('#friend').textContent);
const submitBtn = document.querySelector('#send-message');
const messageInput = document.querySelector('#message-input');
const chatOutput = document.querySelector('#chat-body');

const socket = new WebSocket(
    'wss://' + window.location.host + '/ws/' + friendId + '/'
)

socket.onopen = function(e) {
    console.log('CONNECTION ESTABLISHED')
}

socket.onmessage = function(e) {
    const result = JSON.parse(e.data)
    console.log(result)
    if (result.username == user) {
        chatOutput.innerHTML += `
            <div class="message end">
                <div class="right">
                    <span>${result.message}</span>
                    
                </div>
            </div>
                `
    }else{
        chatOutput.innerHTML += `
            <div class="message ">
                <div class="left">
                    <span>${result.message}</span>
                    
                </div>
            </div>`
    }
}

socket.onerror = function(e) {
    console.log('ERROR IN CONNECTON')
    console.log(e)
}

messageInput.onkeyup = function(e) {
    if(e.keyCode === 13) {
        submitBtn.click();
    }
}

submitBtn.onclick = function(e) {
    let message = messageInput.value;
    socket.send(
        JSON.stringify({
            'username':user,
            'message':message
        })
    );
    messageInput.value = ''
}