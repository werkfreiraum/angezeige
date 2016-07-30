from time import localtime
from time import strftime
from programs import Program


class ShowTime(Program):
    name = "TIME"
    def do(self):
        separator = ["INNER", "NONE"]
        oldSec = -1
        while True:
            signs = strftime("%H%M", localtime())
            sec = int(strftime("%S", localtime()))
            if oldSec != sec:
                self.write(signs, separator=separator[sec % len(separator)])
            oldSec = sec
            # FIXME displayed clock will be wrong by design (up to 100ms)
            self.wait(0.05)
