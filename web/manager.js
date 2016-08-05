connected = false

function onOpen(evt) {
    console.log("Connected!")
    connected = true
    $("#status").html("Connected!");
}

function onClose(evt) {
    console.log("Disconnected!")
    $("#status").html("Disconnected!");
    connected = false
}

function onMessage(evt) {
    //console.log(evt.data)
    console.log(JSON.parse(evt.data))
}

function connect(websocketAddress) {
    if (connected) {
        console.log("Disconnecting ...")
        websocket.close()
    }
    console.log("Connecting ...")
    websocket = new WebSocket(websocketAddress)
    websocket.binaryType = "blob";
    websocket.onopen = onOpen
    websocket.onclose = onClose
    websocket.onmessage = onMessage
}

function sendCommand(command) {
    commandWS = new WebSocket(websocket.url)
    commandWS.onmessage = onMessage
    commandWS.onopen = function() {
        commandWS.send(JSON.stringify(command))
    }
}

$(document).ready(function() {
    $("#serverName").val("ws://localhost:8001/")
    $("#connectButton").click(function() {
        connect($("#serverName").val())
    })
    $("#nextButton").click(function() {
        sendCommand({"name": "switch"})
    })
    $("#programsButton").click(function() {
        sendCommand({"name": "get_programs"})
    })
});
