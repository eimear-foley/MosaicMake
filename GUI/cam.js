(function(){

window.addEventListener("DOMContentLoaded", init, false); 
var dataURL;
var request;

function init(){
// Grab elements, create settings, etc.
var video = document.getElementById('video');
var save_button = document.querySelector("#save");
save_button.disbaled = "true";

// Get access to the camera!
if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    // Not adding `{ audio: true }` since we only want video now
    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
        video.src = window.URL.createObjectURL(stream);
        video.play();
    });
}

/* Legacy code below: getUserMedia 
else if(navigator.getUserMedia) { // Standard
    navigator.getUserMedia({ video: true }, function(stream) {
        video.src = stream;
        video.play();
    }, errBack);
} else if(navigator.webkitGetUserMedia) { // WebKit-prefixed
    navigator.webkitGetUserMedia({ video: true }, function(stream){
        video.src = window.webkitURL.createObjectURL(stream);
        video.play();
    }, errBack);
} else if(navigator.mozGetUserMedia) { // Mozilla-prefixed
    navigator.mozGetUserMedia({ video: true }, function(stream){
        video.src = window.URL.createObjectURL(stream);
        video.play();
    }, errBack);
}
*/
// Elements for taking the snapshot
var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');
var video = document.getElementById('video');

// Trigger photo take
document.getElementById("snap").addEventListener("click", function() {
        context.drawImage(video, 0, 0, 640, 480);
         dataURL = canvas.toDataURL('image/png');
    var hidden_input = document.querySelector("#image");
    hidden_input.value = dataURL;   
    var save_button = document.querySelector("#save");
    save_button.disabled = false;
    //save_button.addEventListener("click", save_image(), false);    

});
}

/*function save_image(){
var url = "cgi-bin/cam.py";
console.log(url);
var param = "image=" + dataURL;
request = new XMLHttpRequest();
request.addEventListener('readystatechange', handle_response, false);
request.open('POST', url, true);
request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
request.send(param);
}*/



/*function handle_response(){
console.log("handle_response");
console.log(request.readyState);
if (request.readyState === 4){
        console.log("ready state 4");
        console.log("request.status =" + request.status );
        if (request.status === 200){
                console.log("200");
                console.log(request.responseText.trim());
                if (request.responseText.trim() === "good"){
                        window.location = "cgi-bin/resize.py";
                        }
                } else {
                        console.log(request.responseText.trim());
                        }
        }
}*/


})();
