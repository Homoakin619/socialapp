const chatGround = document.querySelector('#chat-ground');
const closeBtn = document.querySelector('#close');
let messages = document.getElementsByClassName('message');
const user = JSON.parse(document.querySelector('#current_user').textContent);
const chatOutput = document.querySelector('#chat-body');
const user_space = document.querySelector('#user_space');
const friendId = JSON.parse(document.querySelector('#friend').textContent);
const submitBtn = document.querySelector('#send-message');
const messageInput = document.querySelector('#message-input');


let chat_url = `${window.location.protocol}//${window.location.host}/chat_user/`;

function get_time(value) {
    date = new Date(value);
    let x = date.getHours();
    let minute = date.getMinutes();
    let hour;
    if (x>12){
        hour = x % 12;
    }else{
        hour = x;
    }
    
    let period;
    if (hour > 0) {
        period = 'pm';
    }else if(hour == 0){
        period = 'am';
    }else{
        period = 'am';
    }
    let result = `${hour}:${minute} ${period}`
    return result
}



if(friendId) {
    runSocket(friendId);
} else {
    function makeRequest() {
        const userId = this.id
        data = {name:userId}
            fetch(chat_url,{
                method: 'POST',
                mode: 'no-cors',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
                })
                .then((response) => response.json())
                .then((data) => {
                    user_space.innerHTML = `${data.friend}`;
                    let chat_messages = JSON.parse(data.messages);
                    let id = data.id;
                    console.log(Object.keys(data));
                    runSocket(id);
                    // console.log();
                    for (let message of chat_messages) {
                        var time = message['fields']['timestamp']
                    
                        if(message['fields']['sender'] == user){
                            chatOutput.innerHTML += `
                                <div class="message end">
                                    <div class="right">
                                    <span>${ message['fields']['message'] }</span>
                                    <small>${ get_time(time) }</small>
                                    </div>
                                </div>`
                        }else {
                            chatOutput.innerHTML += `
                                <div class="message ">
                                    <div class="left">
                                    <span>${ message['fields']['message'] }</span>
                                    <small>${ get_time(time) }</small>
                                    </div>
                                </div>`
                        }
                        
                    }
                    chatGround.style.display = 'flex'; 
                })
                // .then((next) => runProcess(userId))
        }
    
    for (message of messages) {
            message.addEventListener('click',makeRequest)
        }
    
}


function runSocket(id) {
    const socket = new WebSocket(
        'wss://' + window.location.host + '/ws/' + id + '/'
    )
    
    socket.onopen = function(e) {
        console.log('CONNECTION ESTABLISHED')
    }
    
    socket.onmessage = function(e) {
        const result = JSON.parse(e.data)
        var date = new Date()
    
        let get_Hour = (date) => {
            let x = date.getHours()
            let result1 = x % 12
            let period = null
            if (result1 > 0) {
                period = 'pm'
            }else if(result1 == 0){
                period = 'am'
            }else{
                period = 'am'
            }
            return {'time':result1,'period':period}
        }
    
        if (result.username == user) {
            chatOutput.innerHTML += `
                <div class="message end">
                    <div class="right">
                        <span>${result.message}</span>
                        <small>${get_Hour(date).time}:${date.getMinutes()} ${get_Hour(date).period}</small>
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
}

messageInput.onkeyup = function(e) {
    if(e.keyCode === 13) {
        submitBtn.click();
    }
}

function runProcess(senderId) {
    let sender = senderId
    let read_url = `${window.location.protocol}//${window.location.host}/messages/${sender}/`
    let data = {value:sender}
    
    fetch(read_url, {
        method: 'POST',
        mode: 'no-cors',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
        })
        .then((response) => response.json() )
        .then((data) => {
            
            console.log('Status:',  data.status);
            window.location.href = `${window.location.protocol}//${window.location.host}/messages/`
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

