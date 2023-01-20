let messagesCount = document.querySelector('#msgcount');
let msgCount = document.querySelector('#msgs');
let notificationsCount = document.querySelector('#notificationcount');
let ntfCount = document.querySelector('#ntfs');
let loggedId = document.querySelector('#loggedId');
let Id = loggedId.value;


window.onload = refreshMessage();

function refreshMessage()    {  
    const refreshSocket = new WebSocket('ws://'+window.location.host +'/ws/refresh/'+Id+'/');

    refreshSocket.onopen = function(e) {
        console.log('REFRESH CONNECTION ESTABLISHED');
        refreshSocket.send(JSON.stringify({'status':'refresh messages'}))
    }
    

    refreshSocket.onmessage = function(e) {
        let returns = JSON.parse(e.data);
        let messageCount = returns.count
        messagesCount.innerHTML = messageCount;
        msgCount.innerHTML = messageCount;
    }

    refreshSocket.onclose = function(e) {
        console.log('REFRESH CONNECTION CLOSED')
    }

    refreshSocket.onerror = function(e) {
        console.log('AN ERROR OCCURED');
        console.log(e);
    }
}

    



// window.onload = 

    // fetch(url,{
    //         method: 'GET',
    //         mode: 'no-cors',
    //         headers: {
    //             'Content-Type': 'application/json',
    //         }
    //         })
    //         .then((response) => response.json() )
    //         .then((data) => {
    //             console.log(data)
    //             messagesCount.innerHTML = data.message_count;
    //             msgCount.innerHTML = data.message_count;
    //             notificationsCount.innerHTML = data.notification_count;
    //             ntfCount.innerHTML = data.notification_count;
    //         });