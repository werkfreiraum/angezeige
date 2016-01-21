# -*- coding: utf-8 -*-
####################################
# LED NUMERATION | SEVEN SEGMENT
####################################
#
#     0000
#    5    1   33
#    5    1   22
#     6666
#    4    2   11
#    4    2   00
#     3333
#
##################

up = {}
up[0] = None
up[1] = None
up[2] = 1
up[3] = 6
up[4] = 5
up[5] = None
up[6] = 0

down = {}
up[0] = 6
up[1] = 2
up[2] = None
up[3] = None
up[4] = None
up[5] = 4
up[6] = 3


digit_signs = {}
digit_signs[" "] = []
##################
# DIGITS
##################
digit_signs["0"] = [0, 1, 2, 3, 4, 5]
digit_signs["1"] = [1, 2]
digit_signs["2"] = [0, 1, 3, 4, 6]
digit_signs["3"] = [0, 1, 2, 3, 6]
digit_signs["4"] = [1, 2, 5, 6]
digit_signs["5"] = [0, 2, 3, 5, 6]
digit_signs["6"] = [0, 2, 3, 4, 5, 6]
digit_signs["7"] = [0, 1, 2]
digit_signs["8"] = range(7)
digit_signs["9"] = [0, 1, 2, 3, 5, 6]

##################
# LETTERS
##################
digit_signs["A"] = [0, 1, 2, 4, 5, 6]
digit_signs["B"] = range(7)
digit_signs["b"] = [2, 3, 4, 5, 6]
digit_signs["C"] = [0, 3, 4, 5]
digit_signs["c"] = [3, 4, 6]
digit_signs["d"] = [1, 2, 3, 4, 6]
digit_signs["E"] = [0, 3, 4, 5, 6]
digit_signs["F"] = [0, 4, 5, 6]
digit_signs["G"] = [0, 2, 3, 4, 5]
digit_signs["H"] = [1, 2, 4, 5, 6]
digit_signs["h"] = [2, 4, 5, 6]
digit_signs["I"] = [5, 4]
digit_signs["i"] = [2]
digit_signs["j"] = [2, 3]
digit_signs["J"] = [1, 2, 3, 4]
digit_signs["K"] = [1, 2, 4, 5, 6]
digit_signs["L"] = [3, 4, 5]
digit_signs["l"] = [1, 2]
# digit_signs["M"]
# digit_signs["N"]
digit_signs["n"] = [4, 6, 2]
digit_signs["O"] = [0, 1, 2, 3, 4, 5]
digit_signs["o"] = [2, 3, 4, 6]
digit_signs["P"] = [0, 1, 4, 5, 6]
# digit_signs["Q"]
digit_signs["q"] = [0, 1, 2, 5, 6]
digit_signs["R"] = [0, 1, 2, 4, 5, 6]
digit_signs["r"] = [4, 6]
digit_signs["S"] = [0, 2, 3, 5, 6]
# digit_signs["T"]
digit_signs["t"] = [3, 4, 5, 6]
digit_signs["U"] = [1, 2, 3, 4, 5]
digit_signs["u"] = [2, 3, 4]
digit_signs["V"] = [5, 6, 1, 4]
# digit_signs["W"]
digit_signs["X"] = [1, 2, 4, 5, 6]
digit_signs["Y"] = [1, 2, 3, 5, 6]
digit_signs["Z"] = [0, 1, 3, 4, 6]

##################
# SPECIAL CHARS
##################
digit_signs[u'ö'] = [0, 2, 3, 4, 6]
digit_signs[u'ü'] = [0, 2, 3, 4]
digit_signs[u'ß'] = [0, 1, 2, 4, 5]
digit_signs["_"] = [3]
digit_signs["-"] = [6]
digit_signs[u"°"] = [5, 0, 1, 6]
digit_signs["\n"] = []
digit_signs["?"] = [0, 1, 4, 6]
digit_signs["!"] = []
digit_signs["."] = [3]
digit_signs[","] = [4]
digit_signs["'"] = [1]
digit_signs["\""] = [1, 5]


pref_char_rep = {}
pref_char_rep['a'] = 'A'
pref_char_rep['b'] = 'b'
pref_char_rep['c'] = 'c'
pref_char_rep['d'] = 'd'
pref_char_rep['e'] = 'E'
pref_char_rep['f'] = 'F'
pref_char_rep['g'] = 'G'
pref_char_rep['h'] = 'h'
pref_char_rep['i'] = 'i'
pref_char_rep['j'] = 'J'
pref_char_rep['k'] = 'K'
pref_char_rep['l'] = 'L'
pref_char_rep['m'] = '-'
pref_char_rep['n'] = 'n'
pref_char_rep['o'] = 'o'
pref_char_rep['p'] = 'P'
pref_char_rep['q'] = 'q'
pref_char_rep['r'] = 'r'
pref_char_rep['s'] = 'S'
pref_char_rep['t'] = 't'
pref_char_rep['u'] = 'u'
pref_char_rep['v'] = 'V'
pref_char_rep['w'] = '-'
pref_char_rep['x'] = 'X'
pref_char_rep['y'] = 'Y'
pref_char_rep['z'] = 'Z'

pref_char_rep[u'ä'] = u'ö'
pref_char_rep[u'ö'] = u'ö'
pref_char_rep[u'ü'] = u'ü'
pref_char_rep[u'ß'] = u'ß'


##################
# POINTS (all combinations)
##################
separator_types = {}
separator_types['NONE'] = []
separator_types['LOWER'] = [0, 1]
separator_types['UPPER'] = [2, 3]
separator_types['BOTH'] = [0, 1, 2, 3]
separator_types['INNER'] = [1, 2]
separator_types[0] = [0]
separator_types[1] = [1]
separator_types[2] = [2]
separator_types[3] = [3]
separator_types[4] = [4]
separator_types[('P', 0)] = []
separator_types[('P', 1)] = [0]
separator_types[('P', 2)] = [0, 1]
separator_types[('P', 3)] = [0, 1, 2]
separator_types[('P', 4)] = [0, 1, 2, 3]
