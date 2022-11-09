import sys
import cfbd
from Tree import *
from Team import *

ConfDict = {
    "B1G": "Big Ten",
    "SEC": "SEC",
    "ACC": "ACC",
    "B12": "Big 12",
    "PAC": "Pac-12",
    "MWC": "Mountain West"
}

class Calculator:
    def __init__(self, yr, cf):
        teamAndLogo = self.getMasterTeamsAndLogos(yr, cf)
        self.allTeams = teamAndLogo[0]
        self.allLogos = teamAndLogo[1]
        self.urlDict = {self.allTeams[i].name: self.allLogos[i] for i in range(len(self.allTeams))}
        self.allTrees = []
        for i in self.allTeams:
            self.allTrees.append(Tree(i, self.allTeams.__len__()))

    def findMaxCircs(self):
        allCircs = []
        maxLen = -1
        for i in self.allTrees:
            for j in i.getCleanedLeavesMax():
                allCircs.append(j)
                if j.__len__() > maxLen:
                    maxLen = j.__len__()

        for i in range(len(allCircs) - 1, -1, -1):
            alphFirst = min(x for x in allCircs[i] if isinstance(x, str))
            if allCircs[i].__len__() != maxLen:
                del allCircs[i]
            else:
                while allCircs[i][0] != alphFirst:
                    allCircs[i].insert(0, allCircs[i].pop())

        # removes duplicates, left with all possible max circles of suck
        tups = [tuple(x) for x in allCircs]
        dct = list(dict.fromkeys(tups))
        sansDups = [list(x) for x in dct]

        return sansDups


    def findMinCircs(self):
        allCircs = []
        minLen = 9999
        for i in self.allTrees:
            for j in i.getCleanedLeavesMin():
                allCircs.append(j)
                if j.__len__() < minLen:
                    minLen = j.__len__()

        for i in range(len(allCircs) - 1, -1, -1):
            alphFirst = min(x for x in allCircs[i] if isinstance(x, str))
            if allCircs[i].__len__() != minLen:
                del allCircs[i]
            else:
                while allCircs[i][0] != alphFirst:
                    allCircs[i].insert(0, allCircs[i].pop())

        # removes duplicates, left with all possible max circles of suck
        tups = [tuple(x) for x in allCircs]
        dct = list(dict.fromkeys(tups))
        sansDups = [list(x) for x in dct]

        return sansDups

    def getMasterTeamsAndLogos(self, year, conf):
        masterTeams = []
        masterLogos = []
        perfList = []

        configuration = cfbd.Configuration()
        configuration.api_key['Authorization'] = sys.argv[1]
        configuration.api_key_prefix['Authorization'] = 'Bearer'

        team_api_instance = cfbd.TeamsApi(cfbd.ApiClient(configuration))
        teams = team_api_instance.get_fbs_teams(year=year)
        #teams = teams + team_api_instance.get_teams(conference="SEC")

        for i in teams:
            # for each conference team found in the database,
            if i.conference == ConfDict[conf]:
                masterTeams.append(Team(i.school))
                masterLogos.append(i.logos[0])
        # append new Team objects with their names to a master team list

        for i in masterTeams:
            game_api_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))
            games = game_api_instance.get_games(year=year, conference=conf, team=i.name, season_type="regular")
            #games = games + game_api_instance.get_games(year=yr, conference="SEC", team=i.name, season_type="regular")
            for j in games:
                if j.home_points is not None:  # filter out games that haven't happened yet
                    if j.home_team == i.name:
                        # if the team is the home team
                        if j.home_points > j.away_points:

                            for k in masterTeams:
                                if k.name == j.away_team:
                                    i.addDef(k)

                        else:
                            for k in masterTeams:
                                if k.name == j.away_team:
                                    i.addLos(k)
                    else:
                        if j.home_points > j.away_points:
                            for k in masterTeams:
                                if k.name == j.home_team:
                                    i.addLos(k)
                        else:
                            for k in masterTeams:
                                if k.name == j.home_team:
                                    i.addDef(k)

            if i.lostTo.__len__() == 0 or i.defeated.__len__() == 0:
                perfList.append(i)

        # filter out undefeated and win-proof teams


        while perfList.__len__() != 0:
            perfAtBat = []
            for i in range(len(masterTeams) - 1, -1, -1):
                if masterTeams[i] in perfList:
                    del masterTeams[i]
                    del masterLogos[i]
                else:
                    for j in range(len(masterTeams[i].lostTo) - 1, -1, -1):
                        if masterTeams[i].lostTo[j] in perfList:
                            del masterTeams[i].lostTo[j]

                    for j in range(len(masterTeams[i].defeated) - 1, -1, -1):
                        if masterTeams[i].defeated[j] in perfList:
                            del masterTeams[i].defeated[j]

                    if masterTeams[i].lostTo.__len__() == 0 or masterTeams[i].defeated.__len__() == 0:
                        perfAtBat.append(masterTeams[i])

            perfList = perfAtBat

        return [masterTeams, masterLogos]
