Control the awesome RGB led 7-segment display.

Requirements
------------
Ubuntu:

    sudo apt install python-urwid python-webcolors
    git clone https://github.com/dpallot/simple-websocket-server.git


How to run
----------
Main program for real display:

    ./main.py


Simulation:

    PYTHONPATH=simple-websocket-server ./web_socket.py

Then open ./angezeige/simulation/index.html in your web browser.
