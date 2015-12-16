#!/usr/bin/env python2
import webcolors as wc
from signs import digit_signs, separator_types
from settings import digit_leds, separator_leds
import time

spidev = None
spidev_file = "/dev/spidev0.0"
#spidev_file = "/tmp/spidev0.0"


def _get_color(color, output_format="byte"):
    if isinstance(color, basestring):
        if color.startswith("#"):
            if len(color) == 4:
                a = (int(color[1] * 2, 16), int(color[2] * 2, 16), int(color[3] * 2, 16))
            elif len(color) == 7:
                a = (int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16))
            else:
                raise Exception("Format not implemented")
        else:
            a = wc.name_to_rgb(color)

    if output_format == "byte":
        return bytearray(chr(a[2]) + chr(a[1]) + chr(a[0]))
    elif output_format == "hex":
        return "#%02X%02X%02X" % (a[0], a[1], a[2])
    else:
        raise Exception("Format " + str(output_format) + " not implemented")


def _get_leds(ascii, position):
    if ascii in digit_signs:
        return [digit_leds[position][l] for l in digit_signs[ascii]]
    else:
        raise Exception("Sign " + str(ascii) + " not implemented")


def get_message(string, separator="NONE", color="white", off_color="black"):
    leds = [t for i, c in enumerate(string) for t in _get_leds(c, i)]
    leds += [separator_leds[i] for i in separator_types[separator]]

    color_bytes = _get_color(color)
    off_color_bytes = _get_color(off_color)

    message = ''
    for i in range(30):
        if i in leds:
            message += color_bytes
        else:
            message += off_color_bytes

    return message


def write_spidev(message):
    spidev.write(message)
    spidev.flush()


# STARTING POINT
def run(write):
    i = 0
    separators = ["NONE"]
    # = ["8888", "", "1", "2", " 3"]
    messages = ["8888", "", "1", "2", " 3"]
    while True:
        #print(str(i) + " "  + messages[i%len(messages)] + " " + separators[i%len(separators)])
        temp = "%1d" % (i%10)
        message = get_message(temp, separator=separators[i%len(separators)], color="blue")
        write(message)
        time.sleep(2)
        i += 1

def main():
    global spidev
    spidev = open(spidev_file,"wb")
    run(write_spidev)

if __name__ == "__main__":
    main()

