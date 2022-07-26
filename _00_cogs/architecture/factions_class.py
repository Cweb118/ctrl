from _02_global_dicts import theJar
from _00_cogs.architecture.kits.faction_kits import *


class Faction():
    def __init__(self, faction_name):
        self.title = faction_name

        #faction_title:rep_int
        self.reps = {}

        self.rep_cypher = {
            3:'Allied',
            2:'Cooperative',
            1:'Friendly',
            0:'Neutral',
            -1:'Unfriendly',
            -2:'Hostile',
            -3:'Enemy'
        }

        theJar['factions'][self.title] = self

    def addRep(self, other_faction_title, rep_change):
        rep_change = int(rep_change)
        try:
            self.reps[other_faction_title] += rep_change
        except:
            self.reps[other_faction_title] = 0
            self.reps[other_faction_title] += rep_change
        if self.reps[other_faction_title] > 3:
            self.reps[other_faction_title] = 3
        if self.reps[other_faction_title] > -3:
            self.reps[other_faction_title] = -3

    def repCheck(self, other_faction_title):
        rep = self.reps[other_faction_title]
        return rep

    def report(self):
        reps = self.reps
        report = self.title+" Standings:\n"
        for rep in reps.keys():
            report += rep+': '+self.rep_cypher[reps[rep]]+'\n'
        return report


def init_factions(factions_kit):
    f_list = []
    for faction in factions_kit.keys():
        f = Faction(faction)
        f_list.append(f)
    for faction in f_list:
        for rep in factions_kit[faction.title].keys():
            faction.addRep(rep,factions_kit[faction.title][rep])
    print(theJar['factions'])
    for faction in f_list:
        print(faction.report())

#init_factions(g0)
