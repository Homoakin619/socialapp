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
    type;
    constructor(type) {
        this.type = type
    }

    makeconnection() {
        
        this.Socket = new WebSocket('ws://'+window.location.host +'/ws/refresh/'+Id+'/');

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
                
                socket.send(JSON.stringify({'type':'refresh','friend_id':friendId}));

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
                
                socket.send(JSON.stringify({'type':'refresh','friend_id':0}));

                socket.onmessage = function(e) {
                    
                    let returned_data = JSON.parse(e.data);
                    
                    let messageCount = returned_data.message_count;
                    let NotificationCount = returned_data.notification_count;
                    
                    messagesCount.innerHTML = messageCount;
                    msgCount.innerHTML = messageCount;
            
                    notificationsCount.innerHTML = NotificationCount;
                    notifCount.innerHTML = NotificationCount;
            
                    } // inner socket.onmessage ends here

                } // If/Else Clause ends here
            } // socket.onopen ends here

        } // makeconnection() ends here
        

    refreshData(id=null) {
                
        if(friendId) {
            this.Socket.send(JSON.stringify({'type':'refresh','friend_id':friendId}))

            this.Socket.onmessage = function(e) {
                let returned_data = JSON.parse(e.data);
                chatHistory = returned_data.chat_history;
                chatDates = returned_data.chat_dates;
                friendUsername = returned_data.friend_username;
                let chats_history = displayChats(chatHistory,chatDates,user);
                chatOutput.innerHTML += chats_history;
                let messageCount = returned_data.message_count;
                let NotificationCount = returned_data.notification_count;
                
                messagesCount.innerHTML = messageCount;
                msgCount.innerHTML = messageCount;
        
                notificationsCount.innerHTML = NotificationCount;
                notifCount.innerHTML = NotificationCount;
        
                if(user_space){
                    user_space.innerHTML = friendUsername;
                    }
                }  
        }
        else if(id){
            this.Socket.send(JSON.stringify({'type':'refresh','friend_id':id}));

            this.Socket.onmessage = function(e) {
                let returned_data = JSON.parse(e.data);
                chatHistory = returned_data.chat_history;
                chatDates = returned_data.chat_dates;
                friendUsername = returned_data.friend_username;
                let chats_history = displayChats(chatHistory,chatDates,user);
                chatOutput.innerHTML += chats_history;
                
                let messageCount = returned_data.message_count;
                let NotificationCount = returned_data.notification_count;
                
                messagesCount.innerHTML = messageCount;
                msgCount.innerHTML = messageCount;
        
                notificationsCount.innerHTML = NotificationCount;
                notifCount.innerHTML = NotificationCount;
                
        
                if(user_space){
                    user_space.innerHTML = friendUsername;
                    }
                }  
        }else{
            this.Socket.send(JSON.stringify({'type':'refresh','friend_id':0}));

            this.Socket.onmessage = function(e) {
                let returned_data = JSON.parse(e.data);
                let messageCount = returned_data.message_count;
                let NotificationCount = returned_data.notification_count;
             
                messagesCount.innerHTML = messageCount;
                msgCount.innerHTML = messageCount;
        
                notificationsCount.innerHTML = NotificationCount;
                notifCount.innerHTML = NotificationCount;
                }
        }
    
        }   // refreshData ends here..

    subscribeNotification(profile_id=null,action=null) {
        this.Socket.send(JSON.stringify({
            'type':'subscription',
            'action':action,
            'id':profile_id
        }));

        this.Socket.onmessage = function(e) {
            let returned_data = JSON.parse(e.data);
            
            let response = returned_data.response;
            console.log(response)
            }
    }

    readMessage(friend_name=null) {
        let $this = this;
        let socket = this.Socket
        socket.send(JSON.stringify({
            'type':'read',
            'username':friend_name
        }));
        
        socket.onmessage = function(e) {
            let response = JSON.parse(e.data);
    
            if(response['response'] == 'success') {
                runSocket(response['user_id']);
                $this.refreshData(response['user_id'])

            }else {
                console.log('Else running!')
                console.log(response['response'])
                console.log(this)
            }

            }
        } //read messaged ends here..

    } 
    
const generalSocket = new RefreshSocketObject('refresh');
window.onload = generalSocket.makeconnection()