#!/bin/python2
import webcolors as wc

spidevBuffer = "/dev/spidev0.0"
off = bytearray(b'\x00\x00\x00')

##################
# LED NUMERATION 
##################
digit = {} 

digit[0] = [ 0, 1, 2, 3, 4, 5, 6]
digit[1] = [ 7, 8, 9,10,11,12,13]
digit[2] = [16,17,18,19,20,21,22]
digit[3] = [23,24,25,26,27,28,29]

point    = [14,15]




##################
# LED NUMERATION | SEVEN SEGMENT
##################
#
#     0000
#    5    1   00
#    5    1   00
#     6666 
#    4    2   11
#    4    2   11
#     3333 
#
##################

sign = {}
##################
# DIGITS
##################
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

##################
# LETTERS
##################
sign["A"] = [0,1,2,4,5,6]
sign["B"] = range(7)
sign["b"] = [2,3,4,5,6]
sign["C"] = [0,3,4,5]
sign["c"] = [3,4,6]
sign["d"] = [1,2,3,4,6]
sign["E"] = [0,3,4,5,6]
sign["F"] = [0,4,5,6]
sign["G"] = [0,2,3,4,5]
sign["H"] = [1,2,4,5,6]
sign["h"] = [2,4,5,6]
sign["I"] = sign["1"]
sign["J"] = [0,1,2,3,4]
# sign["K"]
sign["L"] = [3,4,5]
# sign["M"]
# sign["N"]
sign["O"] = sign["0"]
sign["o"] = [2,3,4,6]
sign["P"] = [0,1,4,5,6]
# sign["Q"]
# sign["R"]
sign["S"] = sign["5"]
# sign["T"]
sign["U"] = [1,2,3,4,5,6]
#sign["V"]
#sign["W"]
#sign["X"]
sign["Y"] = [1,2,3,5,6]
sign["Z"] = sign["2"]

##################
# SPECIAL CHARS
##################
sign["_"] = [3]
sign["-"] = [6]




##################
# POINTS (all combinations)
##################
points = {}
points[0] = []
points[1] = [0]
points[2] = [1]
points[3] = [0,1]




spidev = open(spidevBuffer,"wb")


def _get_color(color):
    if isinstance(color, basestring):
        if color.startswith("#"):
            if len(color) == 4:
                a = (int(color[1]*2, 16), int(color[2]*2, 16), int(color[3]*2, 16))
            elif en(color) == 7:
                a = (int(color[1:2], 16), int(color[3:4]*2, 16), int(color[5:6]*2, 16))
        else:
            a = name_to_rgb(color)
    
    return bytearray(chr(a[2]) + chr(a[1]) + chr(a[0]))

def write_time(time, color):
    pass

def get_leds(ascii, position):
    if ascii in sign:
        ret = []
        #ret = [digit[position][l] for l in sign[ascii]]
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

    byte_color = _get_color(color)

    writeString = ''
    for i in range(30):
        if i in temp:
            writeString += byte_color
        else:
            writeString += off
    spidev.write(writeString)
    spidev.flush()


