(function(){
  
var request;
document.addEventListener("DOMContentLoaded", init, false);

function init() {
	console.log("init");
    image = document.querySelector('#wrapper');
	call_try();
}

//to be called in another function with accesstoken as the parameter
function call_try() {
	var currentlocation = window.location;
	console.log(currentlocation);
	console.log(currentlocation.search);
    console.log("call_try");
    var url = "try.py" + currentlocation.search;
    console.log(url);
    request = new XMLHttpRequest();
    request.addEventListener('readystatechange', handle_response1, false);
    request.open('GET', url, true);
    request.send(null);
}

//if all's good redirect to try.py
function handle_response1() {
console.log("1");
  if (request.readyState === 4 ) {
        console.log("2");
        console.log("request.status= " + request.status);
        if (request.status === 200 ) {
                console.log("3");
                console.log("response=" + " " + request.responseText.trim());
            if (request.responseText.trim() === 'problem') {
                console.log("ERROR!");
                //something to show user stuff didn't work D:
            } else {
                image.innerHTML = "<div><img src="+"'" + request.responseText.trim() + "'></div>";
				image.style.display = 'block';
				image.style.marginLeft = 'auto';
				image.style.marginRight = 'auto';
            }
        } else {
		console.log("response = " + request.responseText.trim());
		image.innerHTML = "<div style='margin-left: auto; margin-right: auto; height: 40%; width: 40%; padding: 1em;'><p>Sorry we are experiencing problems right now, please try again later!</p><br /><a href='http://143.239.81.202'>Return to the main page</a></div>"
		}
    }
}  

})();
