websocket = null
programs = {}

function updateConnectionStatus() {
    var status = -1
    if (websocket) 
        status = websocket.readyState
    var connected = false
    switch(status) {
        case -1:
            statusText = "Uninitialized"
        break
        case 0:
            statusText = "Connecting"
        break
        case 1:
            statusText = "Open"
            connected = true
        break
        case 2:
            statusText = "Closing"
        break
        case 3:
            statusText = "Closed"
        break
        
    }

    $("#statusConnection").html(statusText);

    $("#serverName").attr('disabled', connected);
    if (connected) { 
        $("#connectButton").addClass("hidden")
        $("#disconnectButton").removeClass("hidden")
        $("#controlPanel").removeClass("hidden")
    } else {
        $("#disconnectButton").addClass("hidden")
        $("#connectButton").removeClass("hidden")
        $("#controlPanel").addClass("hidden")
    }
}


function getBaseInfo() {
    sendCommand({"name": "get_programs"}, function(data) {
        programs = data
    })
    sendCommand({"name": "get_environment"}, function(data) {
        //environment = data
        $('.envPanel').remove()
        $.each(data, function(proxyName, text) {
            var panel = $('#envPanels .envPanelTemplate').clone()
            panel.removeClass('hidden envPanelTemplate')
            panel.addClass('envPanel')
            panel.find('.panel-title').html(proxyName)

            if(Object.keys(data[proxyName]).length > 0) {
                panel.find('.panel-body').empty()    
                $.each(data[proxyName], function(val, props) {
                    //console.log(props)
                    var checkbox = $('#envPanels .envPanelTemplate .checkbox').clone()
                    checkbox.removeClass('hidden')
                    checkbox.find('label span').html(props['name'])
                    checkbox.find('input').prop('checked', props['enabled']);
                    checkbox.find('input').change(function (evt) {
                        sendCommand({
                                'name': 'set_environment', 
                                'params': {
                                    'proxy': proxyName,
                                    'name': props['name'],
                                    'state': this.checked
                                }})
                    })
                    panel.find('.panel-body').append(checkbox)
                });
            }
            // line.find('input').attr('name', 'p_' + val)
            // line.find('input').val(text)
            // line.find('label').attr('for', 'p_' + val)
            // line.find('label').html(val.replace(/_/g , " ") + ":")
            $('#envPanels').append(panel)
        });
    })
}

function onOpen(evt) {
    updateConnectionStatus()
    getBaseInfo()
}

function onClose(evt) {
    updateConnectionStatus()
}

function onMessage(evt, success, error) {
    //console.log(evt.data)
    console.log(JSON.parse(evt.data))
}

function onMessage2(message) {
    if (message)
        console.log(message)
}

function connect(websocketAddress) {
    websocket = new WebSocket(websocketAddress)
    websocket.binaryType = "blob";
    websocket.onopen = onOpen
    websocket.onclose = onClose
    websocket.onmessage = onMessage
}

function sendCommand(command, success, error) {
    console.log(command)
    success = typeof success !== 'undefined' ? success : onMessage2;
    error = typeof error !== 'undefined' ? error : onMessage2;
    var commandWS = new WebSocket(websocket.url)
    commandWS.onmessage = function(evt) {
        var data = JSON.parse(evt.data)
        console.log(data)
        if (data['valid']) {
            var p = null 
            if ('info' in data)
                p = data['info']
            success(p)
        } else {
            error(data['error'])
        }
        commandWS.close()
    }
    commandWS.onopen = function() {
        commandWS.send(JSON.stringify(command))
    }
}

$(document).ready(function() {
    $("#serverName").val(config.manager.addresses[0])
    $("#connectButton").click(function() {
        connect($("#serverName").val())
    })
    $("#disconnectButton").click(function() {
        websocket.close()
    })
    $("#nextButton").click(function() {
        sendCommand({"name": "switch"})
    })

    $('#startProgramModal').on('show.bs.modal', function (e) {
        $('#startProgramModal #programName').empty()
        $.each(programs, function(val, text) {
                $('#startProgramModal #programName').append(
                    $('<option></option>').val(val).html(val)
                );
        });
        $('#startProgramModal #programName').change()
    })

    $('#startProgramModal #programName').change(function (e) {
        $('#startProgramModal .paramsPanel').addClass('hidden')
        var activeProgram = $('#startProgramModal #programName').val()
        $('#startProgramModal form.params .paramsLine').remove()
        $.each(programs[activeProgram], function(val, text) {
            var line = $('#startProgramModal form.params .paramsLineTemplate').clone()
            line.removeClass('hidden paramsLineTemplate')
            line.addClass('paramsLine')
            line.find('input').attr('id', 'p_' + val)
            line.find('input').attr('name', 'p_' + val)
            line.find('input').val(text)
            line.find('label').attr('for', 'p_' + val)
            line.find('label').html(val.replace(/_/g , " ") + ":")
            $('#startProgramModal form.params').append(line)
        });
        if ($('#startProgramModal form.params .paramsLine').length > 0)
            $('#startProgramModal .paramsPanel').removeClass('hidden')
    })

    $('#startProgramModal #startProgramButton').click(function () {
        var name = $('#startProgramModal #programName').val()
        var params = {}
        $.each(programs[name], function(val, text) {
            params[val] = $('#p_' + val).val()
        })
        sendCommand(
            {   
                "name": "start_program",
                "params": {
                    "name": name,
                    "params": params
                }
            })

        $('#startProgramModal').modal('hide')
    })

    updateConnectionStatus()
    if (config.manager.connect)
        connect($("#serverName").val())
});
