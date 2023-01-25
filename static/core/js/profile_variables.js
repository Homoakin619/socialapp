let postModal = document.getElementById("post_form_modal");
let openPostModalBtn= document.getElementById("open_post");
let closePostModal = document.getElementsByClassName("close")[1];
let modal = document.getElementById("modal");
let open_modal = document.getElementById("modal1");
let closeModal = document.getElementsByClassName("close")[0];
let allPosts = document.getElementById('all-posts');
let engagedPosts = document.getElementById('engagement-posts');
let myPosts = document.getElementById('my-posts')
let Btn1 ,Btn2 ,Btn3;
let inp = document.getElementsByName('image')[0];
let imageSubmitBtn = document.getElementById('img_btn');

const profileId = JSON.parse(document.querySelector('#profile_id').textContent);
const chatBtn = document.querySelector('#chat_user');
const chatArea = document.querySelector('#chat-ground');
const notificationBtn = document.querySelector('#toggle-notification');


var state = JSON.parse(document.querySelector('#status').textContent);



// Image upload Style Functionality

if (imageSubmitBtn){
        imageSubmitBtn.style.display = "none";
    inp.addEventListener('change',function() {
        if (this.value) {
            imageSubmitBtn.style.display = "block";  
        } 
    } );
}


//  Post Creation Functionality
open_modal.onclick = function() {
    modal.style.display = "block";
}

openPostModalBtn.onclick = function() {
    postModal.style.display = "block";
}

closePostModal.onclick = function () {
    postModal.style.display = "none";
}

closeModal.onclick = function () {
    modal.style.display = "none";
}

window.onclick = function(event)  {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}


//  Toggle between Posts Functionality
Btn1 = document.getElementById('all')
Btn2 = document.getElementById('mine')
Btn3 = document.getElementById('engagements')

const btnArray = [Btn1,Btn2,Btn3];
function showAllPosts() {
    btnArray.forEach(element => {
        element.className = null;
    });
    btnArray[0].className = 'active'
    allPosts.style.display = 'block';
    engagedPosts.style.display = 'none';
    myPosts.style.display = 'none';
}

function showEngagedPosts() {
    btnArray.forEach(element => {
        element.className = null;
    });
    btnArray[2].className = 'active'
    allPosts.style.display = 'none';
    engagedPosts.style.display = 'block';
    myPosts.style.display = 'none';
}

function showMyPosts() {
    btnArray.forEach(element => {
        element.className = null;
    });
    btnArray[1].className = 'active'
    allPosts.style.display = 'none';
    engagedPosts.style.display = 'none';
    myPosts.style.display = 'block';
}


let subscription = new RefreshSocketObject('subscription');

const getState = () => {
    if(state == true) {
        return true;
    }else{
        return false
    }
}

if (chatBtn && closeBtn && notificationBtn) {
    chatBtn.onclick = function() {
        chatArea.style.display = 'flex';
        chatOutput.scrollTop = chatOutput.scrollHeight;
    };
    closeBtn.onclick = function() {
        chatArea.style.display = 'none'
    }

// Toggle Noticication Subscription
    notificationBtn.onclick = function(e) {
        myState = getState()
        if(!myState){
            this.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bell-slash" viewBox="0 0 16 16">
                    <path d="M5.164 14H15c-.299-.199-.557-.553-.78-1-.9-1.8-1.22-5.12-1.22-6 0-.264-.02-.523-.06-.776l-.938.938c.02.708.157 2.154.457 3.58.161.767.377 1.566.663 2.258H6.164l-1 1zm5.581-9.91a3.986 3.986 0 0 0-1.948-1.01L8 2.917l-.797.161A4.002 4.002 0 0 0 4 7c0 .628-.134 2.197-.459 3.742-.05.238-.105.479-.166.718l-1.653 1.653c.02-.037.04-.074.059-.113C2.679 11.2 3 7.88 3 7c0-2.42 1.72-4.44 4.005-4.901a1 1 0 1 1 1.99 0c.942.19 1.788.645 2.457 1.284l-.707.707zM10 15a2 2 0 1 1-4 0h4zm-9.375.625a.53.53 0 0 0 .75.75l14.75-14.75a.53.53 0 0 0-.75-.75L.625 15.625z"/>
                </svg>`
            state = true;
            generalSocket.subscribeNotification(profileId,'subscribe')

        }else{
            this.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bell-fill" viewBox="0 0 16 16">
                    <path d="M8 16a2 2 0 0 0 2-2H6a2 2 0 0 0 2 2zm.995-14.901a1 1 0 1 0-1.99 0A5.002 5.002 0 0 0 3 6c0 1.098-.5 6-2 7h14c-1.5-1-2-5.902-2-7 0-2.42-1.72-4.44-4.005-4.901z"/>
                </svg>
            `
            state = false;
            generalSocket.subscribeNotification(profileId,'unsubscribe')

        }

    }
}