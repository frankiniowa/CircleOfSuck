class Team:
    def __init__(self, name):
        self.defeated = []
        self.lostTo = []
        self.name = name
        # print(name)

    def addDef(self, t):
        self.defeated.append(t)

    def addURL(self, u):
        self.logo_url = u

    def addLos(self, t):
        self.lostTo.append(t)

    def delDef(self, t):
        toDel = Team("-")
        for i in self.defeated:
            if i.name == t.name:
                toDel = i
        self.defeated.pop(toDel)

    def delLos(self, t):
        toDel = Team("-")
        for i in self.lostTo:
            if i.name == t.name:
                toDel = i
        self.lostTo.pop(toDel)

    def clrAll(self):
        self.defeated.clear()
        self.lostTo.clear()