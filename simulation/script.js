function doColoring(data) {
    var a = data.match(/.{1,7}/g);
    console.log(a.length)
    for (i = 0; i < a.length; ++i) {
        var id = "#n" + i
        //console.log(id)
        $(id).css({ boxShadow: '1px 3px 6px ' + a[i],
                    background: a[i] })
    }
}

function onMessage(evt) {
    doColoring(evt.data)
}

var sendTrigger = ""

function onOpen(evt) {
    console.log("Connected!")
    sendTrigger = setInterval(send, 20)
}

function onClose(evt) {
    console.log("Disonnected!")
    clearInterval(sendTrigger)
}

function send() {
    websocket.send("a")
}

$(document).ready(function() {
    console.log("Connecting ...")
    websocket = new WebSocket("ws://localhost:8000/")
    websocket.onopen = onOpen
    websocket.onclose = onClose
    websocket.onmessage = onMessage
});

