import webcolors as wc
from signs import digit_signs, separator_types, pref_char_rep
from settings import digit_leds, leds_digit, separator_leds, leds_separator, led_count
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
        b = colorsys.rgb_to_hls(*map(lambda x: float(x) / 255, a))
        b = (b[0], min(1, b[1] * lightness), b[2])
        a = map(lambda x: int(round(x * 255)), colorsys.hls_to_rgb(*b))

    if output_format == "byte":
        return bytearray(chr(a[2]) + chr(a[1]) + chr(a[0]))
    elif output_format == "hex":
        return "#%02X%02X%02X" % (a[0], a[1], a[2])
    else:
        raise Exception("Format " + str(output_format) + " not implemented")


def _get_leds(ascii, position, prefered_signs=True, strict=False):
    if prefered_signs and ascii.lower() in pref_char_rep:
        ascii = pref_char_rep[ascii.lower()]
    if ascii in digit_signs:
        return [digit_leds[position][l] for l in digit_signs[ascii]]
    else:
        if strict:
            raise Exception("Sign '" + unicode(ascii) + "' is not implemented")
        else:
            return [digit_leds[position][l] for l in digit_signs["_"]]


def get_message(string="", separator="NONE", color="white", off_color="black", seperator_color=None, seperator_off_color=None, prefered_signs=True, strict=False):
    if len(string) > 4:
        raise Exception("Only 4 signs allowed, got '" + string[:8] + "' (max 8 signs shown)")

    leds = [t for i, char in enumerate(string) for t in _get_leds(char, i, prefered_signs=prefered_signs, strict=strict)]
    leds += [separator_leds[i] for i in separator_types[separator]]

    return _colorize_message(leds, color=color, off_color=off_color, seperator_color=seperator_color, seperator_off_color=seperator_off_color)


def _colorize_message(leds, color="white", off_color="black", seperator_color=None, seperator_off_color=None):
    if not isinstance(color, list):
        color_bytes = [_get_color(color)]*4
    else:
        color_bytes = [_get_color(c) for c in color ]

    if not isinstance(off_color, list):
        off_color_bytes = [_get_color(off_color)]*4
    else:
        off_color_bytes = [_get_color(c) for c in off_color ]

    if seperator_color is None:
        seperator_color_bytes = color_bytes
    if seperator_off_color is None:
        seperator_off_color_bytes = off_color_bytes

    message = ''
    for i in range(led_count):
        if i in leds:
            if i in leds_digit:
                message += color_bytes[leds_digit[i]]
            else:
                message += seperator_color_bytes[leds_separator[i]]
        else:
            if i in leds_digit:
                message += off_color_bytes[leds_digit[i]]
            else:
                message += seperator_off_color_bytes[leds_separator[i]]

    return message


def modify_separator(message, separator="NONE", color="white", off_color="black", lightness=0.2):
    leds = [separator_leds[i] for i in separator_types[separator]]

    color_bytes = _get_color(color, lightness=lightness)
    off_color_bytes = _get_color(off_color)

    for i in separator_leds:
        if i in leds:
            message = message[:i * 3] + color_bytes + message[(i + 1) * 3:]
        else:
            message = message[:i * 3] + off_color_bytes + message[(i + 1) * 3:]

    return message
