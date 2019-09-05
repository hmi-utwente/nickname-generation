var ready = false;

var startButton = document.getElementById("start-button");

var outputText = document.getElementById("text");
var submitButton;

var stalls = ["Hmmm alright let me put that down.....", "Storing that in my memory banks.....", "Let me just save that information....."];

document.getElementById("input").addEventListener("keydown", function(e) {
    if (!e) { var e = window.event; }
    
    // Enter is pressed
    if (e.keyCode == 13) { 
    	e.preventDefault();
    	console.log("clicking now the start button");
    	submitButton.click(); 
    }
}, false);


startButton.addEventListener("click", function (){
    console.log("sending 'Ready'");
    eel.py_send("ready");
    document.getElementById("input").innerHTML = '<input type="text" id="input-text" style="display:none;"> <button id="submit">Submit</button>';
    
    submitButton = document.getElementById("submit");
    var inputText = document.getElementById("input-text");
    
    submitButton.addEventListener("click", function(){
        eel.py_send(inputText.value);
        inputText.value = "";
        var index = Math.floor(Math.random() * stalls.length);
        outputText.innerHTML = stalls[index];
        submitButton.disabled = true;
    });
});


eel.expose(send);
function send(n){
    return n;
}

eel.expose(removeHTML);
function removeHTML(){
    document.getElementById("input").innerHTML = "";
}

eel.expose(changeHTML);
function changeHTML(text){
    console.log("changed the HTML");
    outputText.innerText = text;
    submitButton.disabled = false;
    console.log(document.getElementById("input-text"));
    document.getElementById("input-text").style.display="";
}
