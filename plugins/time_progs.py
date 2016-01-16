from programs import Program, promoteProgram
from time import localtime, strftime

################################################################
# Shows current time
################################################################
@promoteProgram
class ShowTime(Program):
    def do(self):
        separator = ["INNER", "NONE"]
        while True:
            signs = strftime("%H%M", localtime())
            sec = int(strftime("%S", localtime()))
            self.write(signs, separator = separator[sec%len(separator)])
            # FIXME displayed clock will be wrong by design (up to 100ms)
            self.wait(0.1)
