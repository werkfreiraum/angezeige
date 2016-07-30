//websocketAddress = "ws://foosball.local:5005/"
//websocketAddress = 
connected = false

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
    for (var bytes = [], c = 0; c < evt.data.length; c += 2)
        bytes.push(parseInt(evt.data.substr(c, 2), 16));
    doColoring(bytes)
}

var sendTrigger;

function onOpen(evt) {
    console.log("Connected!")
    connected = true
    $("#status").html("Connected!");
    sendTrigger = setInterval(sendAlive, 1000)
}

function onClose(evt) {
    console.log("Disconnected!")
    $("#status").html("Disconnected!");
    connected = false
    clearInterval(sendTrigger)
}

function sendAlive() {
    websocket.send("a")
}

function connect(websocketAddress) {
    if (connected) {
        console.log("Disconnecting ...")
        websocket.close()
    }

    console.log("Connecting ...")
    websocket = new WebSocket(websocketAddress)
    //websocket.binaryType = 'arraybuffer';
    //websocket.binaryType = 'blob';
    websocket.onopen = onOpen
    websocket.onclose = onClose
    websocket.onmessage = onMessage
}

$(document).ready(function() {
    $("#serverName").val("ws://localhost:8000/")
    $("#connectButton").click(function() {
        connect($("#serverName").val())
    })
});