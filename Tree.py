from anytree import AnyNode, RenderTree

class Tree:
    def __init__(self, team, TEAM_AMT):
        self.team = team
        self.TEAM_NAME = team.name
        self.TEAM_AMT = TEAM_AMT

        self.root = AnyNode(id=self.TEAM_NAME)
        self.createTree(self.root, team)

    def getCleanedLeavesMax(self):
        maxNum = -1
        pile = []
        out = []
        for i in self.root.leaves:
            if i.id == self.TEAM_NAME:
                pile.append(i)
                if i.depth > maxNum:
                    maxNum = i.depth

        for i in pile:
            if i.depth == maxNum:
                out.append([getattr(o, 'id') for o in i.path])
                out[-1].pop()
        return out

    def getCleanedLeavesMin(self):
        minNum = 999
        pile = []
        out = []
        for i in self.root.leaves:
            if i.id == self.TEAM_NAME:
                pile.append(i)
                if i.depth < minNum:
                    minNum = i.depth

        for i in pile:
            if i.depth == minNum:
                out.append([getattr(o, 'id') for o in i.path])
                out[-1].pop()
        return out

    def printData(self):
        print("Team: " + self.TEAM_NAME)
        print("Record: " + str(self.team.defeated.__len__()) + " - " + str(self.team.lostTo.__len__()))
        allLeaves = self.getCleanedLeaves()
        print("Circs: " + str(allLeaves.__len__()))
        histBarebone = [getattr(i, 'depth') for i in allLeaves]

        print("01:", end='')
        for i in range(0, histBarebone.count(1)):
            print("|", end='')
        print("")
        print("02:", end='')
        for i in range(0, histBarebone.count(2)):
            print("|", end='')
        print("")
        print("03:", end='')
        for i in range(0, histBarebone.count(3)):
            print("|", end='')
        print("")
        print("04:", end='')
        for i in range(0, histBarebone.count(4)):
            print("|", end='')
        print("")
        print("05:", end='')
        for i in range(0, histBarebone.count(5)):
            print("|", end='')
        print("")
        print("06:", end='')
        for i in range(0, histBarebone.count(6)):
            print("|", end='')
        print("")
        print("07:", end='')
        for i in range(0, histBarebone.count(7)):
            print("|", end='')
        print("")
        print("08:", end='')
        for i in range(0, histBarebone.count(8)):
            print("|", end='')
        print("")
        print("09:", end='')
        for i in range(0, histBarebone.count(9)):
            print("|", end='')
        print("")
        print("10:", end='')
        for i in range(0, histBarebone.count(10)):
            print("|", end='')
        print("")
        print("11:", end='')
        for i in range(0, histBarebone.count(11)):
            print("|", end='')
        print("")
        print("12:", end='')
        for i in range(0, histBarebone.count(12)):
            print("|", end='')
        print("")
        print("13:", end='')
        for i in range(0, histBarebone.count(13)):
            print("|", end='')
        print("")
        print("14:", end='')
        for i in range(0, histBarebone.count(14)):
            print("|", end='')
        print("")
        print("")

    def printTree(self):
        print(RenderTree(self.root))

    def createTree(self, n, t):
        for i in t.defeated:
            node = AnyNode(id=i.name, parent=n)

            if i.name != self.TEAM_NAME and node.depth < self.TEAM_AMT:
                withDups = []
                for j in node.path:
                    withDups.append(j.id)
                sansDups = set(withDups)
                if withDups.__len__() == sansDups.__len__():
                    self.createTree(node, i)
