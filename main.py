#!/bin/python2
import webcolors as wc
from signs import digit_signs, separator_types
from settings import digit_leds, separator_leds

spidevBuffer = "/dev/spidev0.0"

#spidev = open(spidevBuffer,"wb")

def _get_color(color):
    if isinstance(color, basestring):
        if color.startswith("#"):
            if len(color) == 4:
                a = (int(color[1]*2, 16), int(color[2]*2, 16), int(color[3]*2, 16))
            elif len(color) == 7:
                a = (int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16))
        else:
            a = wc.name_to_rgb(color)
            
    return bytearray(chr(a[2]) + chr(a[1]) + chr(a[0]))

def write_time(time, color):
    pass

def get_leds(ascii, position):
    if ascii in digit_signs:
        ret = []
        #ret = [digitLeds[position][l] for l in sign[ascii]]
        for l in digit_signs[ascii]:
            ret.append(digit_leds[position][l])
        return ret
    else:
        raise Exception("Sign not implemented")

def write(string, separator="OFF", color = "white", off_color = "black"):
    leds = []
    for i, c in enumerate(string):
        leds += get_leds(c, i)
    for i in separator_types[separator]:
        leds += separator_leds[i]

    color_bytes = _get_color(color)
    off_color_bytes = _get_color(off_color)

    message_bytes = ''
    for i in range(30):
        if i in leds:
            message_bytes += color_bytes
        else:
            message_bytes += off_color_bytes

    #spidev.write(writeString)
    #spidev.flush()


print(_get_color("white"))
print(_get_color("#fff"))
print(_get_color("#ffffff"))

write('0000')