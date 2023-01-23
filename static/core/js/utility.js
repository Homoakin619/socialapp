let mybutton = document.getElementsByClassName("to-top")[0];

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
} else {
        mybutton.style.display = "none";
        }
    }

function goTop() {
    document.documentElement.scrollTop = 0;
}

let comments = document.getElementsByClassName("commentForms");
let commentBtns = document.getElementsByClassName("comment");
let showCommentsBtns = document.getElementsByClassName('showcomment');
let commentSpaces = document.getElementsByClassName('comment-space');
let hideCommentBtns = document.getElementsByClassName('hide-comment');

for (const comment in Object.keys(comments)) {
    comments[comment].setAttribute('id',String(comment));
}

for (const btn in Object.keys(commentBtns)) {
    commentBtns[btn].setAttribute('id',String(btn));
}

for (const btn in Object.keys(commentBtns)) {
    commentBtns[btn].onclick = makeComment;
}

// Functionality for show comment and hide comment

for (const btn in Object.keys(showCommentsBtns)) {
    showCommentsBtns[btn].setAttribute('id',String(btn));
    showCommentsBtns[btn].onclick = showComments;
}

for (const space in Object.keys(commentSpaces)) {
    commentSpaces[space].setAttribute('id',String(space));
}

for (const hide in Object.keys(hideCommentBtns)) {
    hideCommentBtns[hide].setAttribute('id',String(hide));
    hideCommentBtns[hide].onclick = hideComments;
}



function hideComments(something) {
    let spaceID = Number(this.id)
    for (const space in Object.keys(commentSpaces)) {
        var ispace = commentSpaces[space].getAttribute('id');
        if (Number(ispace) == spaceID) {
            let targ = commentSpaces[space];
            targ.style.display = "none";
            try {
                single_comment = document.getElementsByClassName('commentspace')[0]
                single_comment.style.display = "block"
            } catch (error) {
                console.log(error)
            }
        }
    }
}

function showComments(something) {
    let spaceID = Number(this.id)
    for (const space in Object.keys(commentSpaces)) {
        var ispace = commentSpaces[space].getAttribute('id');
        if (Number(ispace) == spaceID) {
            let targ = commentSpaces[space];
            targ.style.display = "block";
            try {
                single_comment = document.getElementsByClassName('commentspace')[0]
                single_comment.style.display = "none"
            } catch (error) {
                console.log(error)
            }
        }
    }
}

function makeComment(btnid) {
    let bId = Number(this.id)
    for (const comment in Object.keys(comments)) {
        var mid = comments[comment].getAttribute('id');
        if (Number(mid) == bId) {
            let pos = comments[comment]
            pos.style.display = "block";
            window.onmouseup = function(event) {
                if (!pos.contains(event.target) ) {
                    pos.style.display = "none";
                }
            }
            
        }
    }
 
}    