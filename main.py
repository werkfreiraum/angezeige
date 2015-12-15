#!/bin/python2
import webcolors as wc

spidevBuffer = "/dev/spidev0.0"

#  00
# 5  1
#  66 
# 4  2
#  33 
sign = {}
# DIGITS
sign["0"] = [0,1,2,3,4,5]
sign["1"] = [1,2]
sign["2"] = [0,1,3,4,6]
sign["3"] = [0,1,2,3,6]
sign["4"] = [1,2,5,6]
sign["5"] = [0,2,3,5,6]
sign["6"] = [2,3,4,5,6]
sign["7"] = [0,1,2]
sign["8"] = range(7)
sign["9"] = [0,1,2,3,5,6]
# ELSE
sign["U"] = [1,2,3,4,5,6]
sign["E"] = [0,3,4,5,6]
sign["o"] = [2,3,4,6]
sign["h"] = [2,4,5,6]
sign["S"] = sign["5"]

points = {}
points[0] = []
points[1] = [0]
points[2] = [1]
points[3] = [0,1]

spidev = open(spidevBuffer,"wb")

digit = {} 
digit[0] = [ 0, 1, 2, 3, 4, 5, 6]
digit[1] = [ 7, 8, 9,10,11,12,13]
point    = [14,15]
digit[2] = [16,17,18,19,20,21,22]
digit[3] = [23,24,25,26,27,28,29]





def write_time(time, color):
    pass

def get_leds(ascii, position):
    if ascii in sign:
        ret = []
        for l in sign[ascii]:
            ret.append(digit[position][l])
        return ret
    else:
        raise Exception("Sign not implemented")

def write(string, delimiter=0, color = "white"):
    temp = []
    for i, c in enumerate(string):
        temp += get_leds(c, i)
    for i in points[delimiter]:
        temp += point[i]

    if color isinstance(o, basestring):
        a = name_to_rgb(color)
        color = "".join(["/x%02x" % c for c in a])

    off = bytearray(b'\x00\x00\x00')
    writeString = ''
    for i in range(30):
        if i in temp:
            writeString += color
        else:
            writeString += off
    spidev.write(writeString)
    spidev.flush()


