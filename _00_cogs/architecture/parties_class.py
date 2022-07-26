from _00_cogs.architecture.channels_class import Channel
from _00_cogs.architecture.factions_class import Faction
from _02_global_dicts import theJar

class Party(Faction):
    def __init__(self, faction_name):
        super().__init__(faction_name)
        self.players = []
        #self.channel = Channel()
        theJar['parties'][self.title] = self


    def addPlayer(self, player_obj):
        #TODO: Add addRep to the player class
        player_obj.addRep(self.title, 6)
        player_obj.faction = self.title
        self.players.append(player_obj.name)
        #self.channel.addPlayer(player_obj)

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
