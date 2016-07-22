function doColoring(data) {
    var a = new Uint8Array(data)
    for (i = 0; i < a.length/3; ++i) {
        var id = "#n" + i
        var color = 'rgb(' + a.slice(i*3, i*3 + 3).reverse().join() + ')'
        $(id).css({ boxShadow: '1px 3px 6px ' + color,
                    background: color })
    }
}

function onMessage(evt) {
    doColoring(evt.data)
}

var sendTrigger = ""

function onOpen(evt) {
    console.log("Connected!")
    sendTrigger = setInterval(sendAlive, 20)
}

function onClose(evt) {
    console.log("Disonnected!")
    clearInterval(sendTrigger)
}

function sendAlive() {
    websocket.send("a")
}

$(document).ready(function() {
    console.log("Connecting ...")
    websocket = new WebSocket("ws://localhost:8000/")
    websocket.binaryType = 'arraybuffer';
    websocket.onopen = onOpen
    websocket.onclose = onClose
    websocket.onmessage = onMessage
});
