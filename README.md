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

It makes sense to ‘aptitude install screen’ and place this line in
/etc/rc.local:

    sudo -iu pi /usr/bin/screen -dmS angezeige bash -c 'cd /home/pi/angezeige/; python main.py'

Run something like this to attach to the screen session if your hands are
already in pain of clapping:

    ssh pi@angezeige.local
    screen -x angezeige

Exit screen (aka detach) without closing angezeige and the screen session:

    CTRL + A,  D

Simulation:

    PYTHONPATH=simple-websocket-server ./web_socket.py

Then open ./angezeige/simulation/index.html in your web browser.
