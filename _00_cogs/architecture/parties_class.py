from _00_cogs.architecture.channels_class import Channel
from _00_cogs.architecture.factions_class import Faction
from _02_global_dicts import theJar

#TODO: James must hook up the guild object to be pickle friendly
class Party(Faction):
    def __init__(self, faction_name):
        super().__init__(faction_name)
        self.players = []
        theJar['parties'][self.title] = self

    async def init(self):
        self.channel = await Channel(self.guild, self.title, 'Factions').init()

    async def addPlayer(self, player_obj):
        player_obj.addRep(self.title, 6)
        player_obj.faction = self.title
        self.players.append(player_obj.memberID)
        await self.channel.addPlayer(player_obj.member)

    async def delPlayer(self, player_obj):
        player_obj.addRep(self.title, -6)
        player_obj.faction = None
        self.players.remove(player_obj.memberID)
        await self.channel.removePlayer(player_obj.member)

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
