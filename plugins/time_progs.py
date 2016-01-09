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
            # FIXME displayed clock will be wrong by design (up to 100ms)
            self.wait(0.1)
