from _00_cogs.architecture.channels_class import Channel
from _02_global_dicts import theJar
from _00_cogs.architecture.kits.faction_kits import *


class Faction():
    def __init__(self, faction_name, guild):
        self.title = faction_name
        self.guild = guild
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
        self.players = []

    async def init(self):
        self.channel = await Channel(self.guild, self.title.replace(' ', '-').lower(), category_name='factions').init()

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


async def init_factions(factions_kit, guild):
    f_list = []
    for faction in factions_kit.keys():
        if faction not in theJar['factions']:
            f = Faction(faction, guild)
            await f.init()
            f_list.append(f)
    for faction in f_list:
        for rep in factions_kit[faction.title].keys():
            faction.addRep(rep,factions_kit[faction.title][rep])
    #print(theJar['factions'])
    #for faction in f_list:
        #print(faction.report())

