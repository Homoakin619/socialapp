const chatGround = document.querySelector('#chat-ground');
const closeBtn = document.querySelector('#close');
const user = JSON.parse(document.querySelector('#current_user').textContent)  ;
const chatOutput = document.querySelector('#chat-body');
const user_space = document.querySelector('#user_space');
friendId = JSON.parse(document.querySelector('#friendId').textContent) ;
const submitBtn = document.querySelector('#send-message');
const messageInput = document.querySelector('#message-input');
let messages = document.getElementsByClassName('message');

let chat_url = `${window.location.protocol}//${window.location.host}/chat_user/`;

class DateFormatter {
    date;
    constructor(date) {
        this.date = date;
    }

    convertDate() {
        let date_object = new Date(this.date);
        return date_object;
    }

    formatDate() {
        let obj = this.convertDate();
        let year = obj.getFullYear();
        let month = obj.getMonth()+1;
        let day = obj.getDate();
        const result = `${year}-${month}-${day}`;

        return result;
    }

    formatTime() {
        let obj = this.convertDate()
        let hourInstance = obj.getHours();
        let minute = obj.getMinutes();
        let hour;
        if (hourInstance > 12){
            hour = hourInstance % 12;
        } else {
            hour = hourInstance;
        }
        
        let period;
        if (hour > 0) {
            period = 'pm';
        }else if(hour == 0){
            period = 'am';
        }else{
            period = 'am';
        }
        let timeResult = `${hour}:${minute} ${period}`
        return timeResult
    }
}


//  Messages  Page Logic
if(friendId) { //User is on profile page of a friend

    runSocket(friendId);
} else {
    console.log('Not Available');
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
                    let dates = JSON.parse(data.chat_date)
                    let id = data.id;
                    let chats = displayChats(chat_messages,dates,user);
                    chatOutput.innerHTML += chats;
                    chatGround.style.display = 'flex'; 
                    runSocket(id);
                })
        }
    
    for (message of messages) {
            message.addEventListener('click',makeRequest)
        }
};


function runSocket(id) {
    console.log('this is it ' +id);
    const socket = new WebSocket(
        'wss://' + window.location.host + '/ws/' + id + '/'
    )
    
    socket.onopen = function(e) {
        console.log('CONNECTION ESTABLISHED');
        let chats_history = displayChats(chatHistory,chatDates,user);
        chatOutput.innerHTML += chats_history;
    }
    
    socket.onmessage = function(e) {
        const result = JSON.parse(e.data)
        refreshMessage();
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
        messageInput.value = '';
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



function displayChats(messages,dates,user) {
    // console.log(dates)
    let output = '';
    const formatter = new DateFormatter()
    const dateFormatter = new DateFormatter()
    for (let date of dates) {
        let dateIns;

        dateFormatter.date = date['fields']['timestamp'];
        dateIns = dateFormatter.formatDate()
    
        output += `<h5 class="divider line one-line" >${dateIns} </h5>`;

        for(let message of messages) {
            let timeInstance = message['fields']['timestamp'];
            formatter.date = timeInstance;
            let messageDate = formatter.formatDate();
    
            // console.log(`ChatDate is => ${dateIns} : MessageDate is => ${messageDate}`)
            if (dateIns == messageDate) {
                
                if (message['fields']['sender'] == user) {
                    output += `
                        <div class="message end">
                            <div class="right">
                            <span>${ message['fields']['message'] }</span>
                            <small>${ formatter.formatTime() }</small>
                            </div>
                        </div>`;
                } else {
                    output += `
                        <div class="message ">
                            <div class="left">
                            <span>${ message['fields']['message'] }</span>
                            <small>${ formatter.formatTime() }</small>
                            </div>
                        </div>`;
                }
                  
            }
        }
    }

    return output;
}
