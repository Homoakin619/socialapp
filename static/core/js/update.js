let messagesCount = document.querySelector('#msgcount');
let msgCount = document.querySelector('#msgs');
let notificationsCount = document.querySelector('#notificationcount');
let notifCount = document.querySelector('#ntfs');
let loggedId = document.querySelector('#loggedId');
let Id = loggedId.value;
let chatHistory;
let chatDates;
let friendUsername;
var friendId;

class RefreshSocketObject {
    status;
    constructor(status) {
        
        this.status = status
    }

    makeconnection() {
        
        this.Socket = new WebSocket('wss://'+window.location.host +'/ws/refresh/'+Id+'/');

        this.Socket.onclose = function(e) {
            console.log('REFRESH CONNECTION CLOSED')
        }
    
        this.Socket.onerror = function(e) {
            console.log('AN ERROR OCCURED');
            console.log(e);
        }

        let socket = this.Socket

        this.Socket.onopen = function(e) {
            console.log('REFRESH CONNECTION ESTABLISHED');
            
            if(friendId) {
                
                socket.send(JSON.stringify({'status':'refresh','friend_id':friendId}));

                socket.onmessage = function(e) {
                    
                    let returned_data = JSON.parse(e.data);
                    
                    let messageCount = returned_data.message_count;
                    let NotificationCount = returned_data.notification_count;
                    chatHistory = returned_data.chat_history;
                    chatDates = returned_data.chat_dates;
    
                    let chats_history = displayChats(chatHistory,chatDates,user);
                    chatOutput.innerHTML += chats_history;
                    friendUsername = returned_data.friend_username;
                    
                    messagesCount.innerHTML = messageCount;
                    msgCount.innerHTML = messageCount;
            
                    notificationsCount.innerHTML = NotificationCount;
                    notifCount.innerHTML = NotificationCount;
            
            
                    if(user_space){
                        user_space.innerHTML = friendUsername;}
                    }
                
            }else{
                
                socket.send(JSON.stringify({'status':'refresh','friend_id':0}));

                socket.onmessage = function(e) {
                    
                    let returned_data = JSON.parse(e.data);
                    
                    let messageCount = returned_data.message_count;
                    let NotificationCount = returned_data.notification_count;
                    
                    messagesCount.innerHTML = messageCount;
                    msgCount.innerHTML = messageCount;
            
                    notificationsCount.innerHTML = NotificationCount;
                    notifCount.innerHTML = NotificationCount;
            
                    } // inner socket.onmessage ends here

                } // IfElse Clause ends here
            } // socket.onopen ends here


        } // makeconnection() ends here
        

    sendData(profileId=null,value=null,status=null) {
        
        if (status == 'refresh') {
                
                if(friendId) {
                    this.Socket.send(JSON.stringify({'status':status,'friend_id':friendId}))    
                }
                this.Socket.send(JSON.stringify({'status':status,'friend_id':0}))   

                this.Socket.onmessage = function(e) {
                    let returned_data = JSON.parse(e.data);
                    
                    let messageCount = returned_data.message_count;
                    let NotificationCount = returned_data.notification_count;
                    chatHistory = returned_data.chat_history;
                    chatDates = returned_data.chat_dates;
                    friendUsername = returned_data.friend_username;
                    
                    messagesCount.innerHTML = messageCount;
                    msgCount.innerHTML = messageCount;
            
                    notificationsCount.innerHTML = NotificationCount;
                    notifCount.innerHTML = NotificationCount;
            
            
                    if(user_space){
                        user_space.innerHTML = friendUsername;}
                    }

            } else {
                
                this.Socket.send(JSON.stringify({
                    'status':status,
                    'value':value,
                    'id':profileId
                }));


                this.Socket.onmessage = function(e) {
                    let returned_data = JSON.parse(e.data);
                    
                    let response = returned_data.response;

                    }

            }
            
        }   // sendData ends here..

    } // make connection ends here
    
const generalSocket = new RefreshSocketObject('refresh');
window.onload = generalSocket.makeconnection()