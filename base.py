import webcolors as wc
from signs import digit_signs, separator_types, pref_char_rep
from settings import digit_leds, separator_leds, led_count
import colorsys

def _get_color(color, output_format="byte", lightness=1):
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

    if lightness != 1:
        b = colorsys.rgb_to_hls(*map(lambda x: float(x)/255, a))
        b = (b[0], min(1, b[1] * lightness), b[2])
        a = map(lambda x: int(round(x*255)), colorsys.hls_to_rgb(*b)) 


    if output_format == "byte":
        return bytearray(chr(a[2]) + chr(a[1]) + chr(a[0]))
    elif output_format == "hex":
        return "#%02X%02X%02X" % (a[0], a[1], a[2])
    else:
        raise Exception("Format " + str(output_format) + " not implemented")


def _get_leds(ascii, position, prefered_signs = True, strict = False):
    if prefered_signs and ascii.lower() in pref_char_rep:
        ascii = pref_char_rep[ascii.lower()]
    if ascii in digit_signs:
        return [digit_leds[position][l] for l in digit_signs[ascii]]
    else:
        if strict:
            raise Exception("Sign '" + unicode(ascii) + "' is not implemented")
        else:
            return [digit_leds[position][l] for l in digit_signs["_"]]


def get_message(string = "", separator="NONE", color="white", off_color="black", prefered_signs = True, strict = False):
    if len(string) > 4:
        raise Exception("Only 4 signs allowed, got '" + string[:8] + "' (max 8 signs shown)")

    leds = [t for i, c in enumerate(string) for t in _get_leds(c, i, prefered_signs = prefered_signs, strict = strict)]
    leds += [separator_leds[i] for i in separator_types[separator]]

    color_bytes = _get_color(color)
    off_color_bytes = _get_color(off_color)

    message = ''
    for i in range(led_count):
        if i in leds:
            message += color_bytes
        else:
            message += off_color_bytes

    return message


def modify_separator(oldMessage, separator="NONE", color="white", off_color="black", lightness=0.2):
    leds = [separator_leds[i] for i in separator_types[separator]]

    color_bytes = _get_color(color, lightness=lightness)
    off_color_bytes = _get_color(off_color)

    for i in separator_leds:
        if i in leds:
            oldMessage = oldMessage[:i*3] + color_bytes + oldMessage[(i+1)*3:]
        else:
            oldMessage = oldMessage[:i*3] + off_color_bytes + oldMessage[(i+1)*3:]

    return oldMessage