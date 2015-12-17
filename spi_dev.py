spidev_file = "/dev/spidev0.0"
#spidev_file = "/tmp/spidev0.0"

def init():
    global spidev
    spidev = open(spidev_file,"wb")

def write(message):
    spidev.write(message)
    spidev.flush()