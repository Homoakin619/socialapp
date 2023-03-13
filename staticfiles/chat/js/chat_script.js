const chatGround = document.querySelector('#chat-ground');
const closeBtn = document.querySelector('#close');
const user = JSON.parse(document.querySelector('#current_user').textContent)  ;
const chatOutput = document.querySelector('#chat-body');
const user_space = document.querySelector('#user_space');
const submitBtn = document.querySelector('#send-message');
const messageInput = document.querySelector('#message-input');
let messages = document.getElementsByClassName('message');

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
        
        let result;
        let obj = this.convertDate();
        let year = obj.getFullYear();
        let month = obj.getMonth()+1;
        let day = obj.getDate();
        let today = new Date();
        today = today.getDate();

        result = `${year}-${month}-${day}`;
        if ((today - day)== 1) {
            result = 'yesterday';
        }

        return result;
    }

    formatTime() {
        let obj = this.convertDate()
        let hourInstance = obj.getHours();
        let minute = obj.getMinutes();
        if (String(minute).length == 1){
            minute = '0' + String(minute)
        }
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
    for (let message of messages) {
            message.addEventListener('click',function() {
                this.style.background = 'none'
                generalSocket.readMessage(this.id)
                chatGround.style.display = 'flex';         
            });
        }
};


function runSocket(id) {
    const socket = new WebSocket(
        'ws://' + window.location.host + '/ws/' + id + '/'
    )
    
    socket.onopen = function(e) {
        console.log('CONNECTION ESTABLISHED');
        // generalSocket.refreshData()
    }
    
    socket.onmessage = function(e) {
        const result = JSON.parse(e.data)
        generalSocket.refreshData()
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
        chatOutput.scrollTop = chatOutput.scrollHeight;
    }
    
    socket.onerror = function(e) {
        console.log('ERROR IN CONNECTON')
        console.log(e)
        setTimeout(runSocket(id),1000)
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

if (messageInput){
    messageInput.onkeyup = function(e) {
        if(e.keyCode === 13) {
            submitBtn.click();
        }
    }
}


function displayChats(messages,dates,user) {
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
