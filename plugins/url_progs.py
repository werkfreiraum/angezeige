from programs import Program, promoteProgram
import urllib

################################################################
# Shows text from URL
################################################################
@promoteProgram
class UrlReader(Program):
    def __init__(self, writer=None, color=None, url=None, duration=None):
        Program.__init__(self, writer, color=color)
        self.url = self.getParams()["url"] if url is None else url
        self.duration = float(self.getParams()["duration"] if duration is None else duration)

    @staticmethod
    def getParams():
        params = Program.getParams()
        params['url'] = "http://angezeige.abteil.org/nr.html"
        params['duration'] = "2"
        return params

    def run(self):
        separator = ["INNER", "NONE"]
        while True:
            f = urllib.urlopen(self.url)
            self.write(f.read(4))
            f.close()
            self.wait(self.duration)
