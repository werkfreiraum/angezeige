from programs import Program, promoteProgram
from time import gmtime, strftime

################################################################
# Shows current time
################################################################
@promoteProgram
class ShowTime(Program):
    def do(self):
        separator = ["INNER", "NONE"]
        while True:
            signs = strftime("%H%M", gmtime())
            sec = int(strftime("%S", gmtime()))
            self.write(signs, separator = separator[sec%len(separator)])
            self.wait(0.1)