
class proposition:
    def __init__(self, filename):
        self.filename = filename
        self.propo = None
        self.file = None

    def  get_new_proposition(self):
        self.propo = []
        self.file = open(self.filename, "r")
        for line in self.file:
            self.propo.append(line[:len(line)-1])

        self.file.close()
        return self.propo


print(proposition("proposition.txt").get_new_proposition())