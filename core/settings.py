####################################
# LED NUMERATION | SEVEN SEGMENT
####################################
#
#     0000
#    5    1   00
#    5    1   11
#     6666
#    4    2   22
#    4    2   33
#     3333
#
##################

##################
# LED NUMERATION
##################
digit_leds = {}

digit_leds[3] = [1, 0, 5, 4, 3, 2, 6]
digit_leds[2] = [8, 7, 12, 11, 10, 9, 13]
digit_leds[1] = [19, 18, 23, 22, 21, 20, 24]
digit_leds[0] = [26, 25, 30, 29, 28, 27, 31]

separator_leds = [14, 15, 16, 17]

led_count = 32

leds_digit = {}
for d, la in digit_leds.items():
    for l in la:
        leds_digit[l] = d

leds_separator = {}
for i, s in enumerate(separator_leds):
    leds_separator[s] = i