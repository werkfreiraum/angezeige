####################################
# LED NUMERATION | SEVEN SEGMENT
####################################
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

digit_signs = {}
##################
# DIGITS
##################
digit_signs["0"] = [0,1,2,3,4,5]
digit_signs["1"] = [1,2]
digit_signs["2"] = [0,1,3,4,6]
digit_signs["3"] = [0,1,2,3,6]
digit_signs["4"] = [1,2,5,6]
digit_signs["5"] = [0,2,3,5,6]
digit_signs["6"] = [2,3,4,5,6]
digit_signs["7"] = [0,1,2]
digit_signs["8"] = range(7)
digit_signs["9"] = [0,1,2,3,5,6]

##################
# LETTERS
##################
digit_signs["A"] = [0,1,2,4,5,6]
digit_signs["B"] = range(7)
digit_signs["b"] = [2,3,4,5,6]
digit_signs["C"] = [0,3,4,5]
digit_signs["c"] = [3,4,6]
digit_signs["d"] = [1,2,3,4,6]
digit_signs["E"] = [0,3,4,5,6]
digit_signs["F"] = [0,4,5,6]
digit_signs["G"] = [0,2,3,4,5]
digit_signs["H"] = [1,2,4,5,6]
digit_signs["h"] = [2,4,5,6]
digit_signs["I"] = digit_signs["1"]
digit_signs["J"] = [0,1,2,3,4]
# digit_signs["K"]
digit_signs["L"] = [3,4,5]
# digit_signs["M"]
# digit_signs["N"]
digit_signs["O"] = digit_signs["0"]
digit_signs["o"] = [2,3,4,6]
digit_signs["P"] = [0,1,4,5,6]
# digit_signs["Q"]
# digit_signs["R"]
digit_signs["S"] = digit_signs["5"]
# digit_signs["T"]
digit_signs["U"] = [1,2,3,4,5,6]
#digit_signs["V"]
#digit_signs["W"]
#digit_signs["X"]
digit_signs["Y"] = [1,2,3,5,6]
digit_signs["Z"] = digit_signs["2"]

##################
# SPECIAL CHARS
##################
digit_signs["_"] = [3]
digit_signs["-"] = [6]



##################
# POINTS (all combinations)
##################
separator_types = {}
separator_types['NONE']    = []
separator_types['LOWER']  = [0]
separator_types['UPPER']  = [1]
separator_types['BOTH']   = [0,1]



