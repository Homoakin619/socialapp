// const user =  JSON.parse(document.querySelector('#current_user').textContent);
const friendId = JSON.parse(document.querySelector('#friend').textContent);
const submitBtn = document.querySelector('#send-message');
const messageInput = document.querySelector('#message-input');
// const chatOutput = document.querySelector('#chat-body');
if(friendId){
    runSocket(friendId)
}
// const socket = new WebSocket(
//     'ws://' + window.location.host + '/ws/' + id + '/'
// )

// socket.onopen = function(e) {
//     console.log('CONNECTION ESTABLISHED')
// }

// socket.onmessage = function(e) {
//     const result = JSON.parse(e.data)
//     var date = new Date()

//     let get_Hour = (date) => {
//         let x = date.getHours()
//         let result1 = x % 12
//         let period = null
//         if (result1 > 0) {
//             period = 'pm'
//         }else if(result1 == 0){
//             period = 'am'
//         }else{
//             period = 'am'
//         }
//         return {'time':result1,'period':period}
//     }

//     if (result.username == user) {
//         chatOutput.innerHTML += `
//             <div class="message end">
//                 <div class="right">
//                     <span>${result.message}</span>
//                     <small>${get_Hour(date).time}:${date.getMinutes()} ${get_Hour(date).period}</small>
//                 </div>
//             </div>
//                 `
//     }else{
//         chatOutput.innerHTML += `
//             <div class="message ">
//                 <div class="left">
//                     <span>${result.message}</span>
                    
//                 </div>
//             </div>`
//     }
// }

// socket.onerror = function(e) {
//     console.log('ERROR IN CONNECTON')
//     console.log(e)
// }

messageInput.onkeyup = function(e) {
    if(e.keyCode === 13) {
        submitBtn.click();
    }
}

// submitBtn.onclick = function(e) {
//     let message = messageInput.value;
//     socket.send(
//         JSON.stringify({
//             'username':user,
//             'message':message
//         })
//     );
//     messageInput.value = ''
// }