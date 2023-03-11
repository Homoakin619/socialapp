let imgModals = document.getElementsByClassName('mds');
let imageLinks = document.getElementsByClassName('img_links');

window.onload = function() {
    for (let link in Object.keys(imageLinks)) {
        imageLinks[link].setAttribute('href','#mds'+String(link));
    }

    for (let modal in Object.keys(imgModals)) {
        imgModals[modal].setAttribute('id','mds'+String(modal))
    }
}

