import operator

from _02_global_dicts import theJar
import nextcord
import time, asyncio
from nextcord.ext import tasks
from _00_cogs.architecture.inventory_class import Inventory
import _00_cogs.frontend.menus.menus as Menus

class Region():
    def __init__(self, name, guild = None, guildID = None, districts = []):
        self.name = name
        theJar['regions'][name] = self
        self.districts = districts
        self.guild = guild
        self.guildID = guildID
        self.channel = None


        if guild:
            self.createChannel.start()
    
    def __reduce__(self):
        districtKeys = []
        for district in self.districts:
            districtKeys.append(district.name)
        return(self.__class__, (self.name, None, self.guild.id))
    
    def reinstate(self, guild):
        self.guild = guild 
        self.createChannel.start()

    def addDistrict(self, district):
        self.districts.append(district)

    def __str__(self):
        return self.name

    def report(self):
        report = "-----"+str(self)+"-----\n\n"
        report += "--Districts:\n"
        for district in self.districts:
            report += "-"+str(district)+"\n"

        return report

    @tasks.loop(seconds=1, count=1)
    async def createChannel(self):
        playerRole = nextcord.utils.get(self.guild.roles, name="player")

        categoryNames = []
        for category in self.guild.categories:
            categoryNames.append(category.name)

        if self.name not in categoryNames:
            category = await self.guild.create_category(self.name)
            self.channel = await category.create_text_channel(self.name)
            await self.channel.set_permissions(self.guild.default_role, read_messages=False)
            await self.channel.set_permissions(playerRole, read_messages = True)
        else:
            print("Channel was found for", self.name, "region.")
            self.channel = nextcord.utils.get(self.guild.channels, name=self.name)

class District():
    def __init__(self, name, region_name, size, paths = None, guild = None, guildID = None, pathsRebuild = [], inventory = None):

        self.name = name
        self.region = region_name
        self.paths = pathsRebuild
        self.players = []
        self.channel = None
        self.interfaceChannel = None
        self.inventory = None
        self.guild = guild
        self.size = size
        self.civics = Civics(self)

        if guild:
            self.guildID = guild.id
        else:
            self.guildID = guildID

        if guild:
            self.createChannel.start()

        sizes = {
            #inv_args: [r_cap=None, r_cont=None, u_cap=None, b_cap=None, u_slotcap=None, b_slotcap=None]
            'tiny': [self, 100, None, 10, 10, 4, 1],
            'small': [self, 100, None, 10, 10, 8, 2],
            'medium': [self, 100, None, 10, 10, 16, 4],
            'large': [self, 100, None, 10, 10, 24, 8],
            'huge': [self, 100, None, 10, 10, 40, 14],
        }
        if inventory:
            self.inventory = inventory
        else:
            self.inventory = Inventory(*sizes[size])


        pathcaps = {
            'tiny': 2,
            'small': 3,
            'medium': 4,
            'large': 6,
            'huge': 9,
        }

        self.pathcap = pathcaps[size]

        if paths:
            for path in paths:
                district = theJar['districts'][path]
                self.setPath(district)

        theJar['regions'][region_name].addDistrict(self)
        theJar['districts'][name] = self

        self.interfaceDirty = False
    
    def __reduce__(self):
        return(self.__class__, (self.name, self.region, self.size, None, None, self.guildID, self.paths, self.inventory))

    def reinstate(self, guild):
        self.guild = guild
        self.createChannel.start()

    @tasks.loop(seconds=1, count=1)
    async def createChannel(self):
        playerRole = nextcord.utils.get(self.guild.roles, name="player")
        
        #Wait a short period incase the region category was just made. Otherwise, it will not be able to find the category.
        await asyncio.sleep(.25)

        for category in self.guild.categories:
            if category.name.lower() == self.region.lower():
                # Ginger: Added interface channel
                interfaceOverwrites = {
                    self.guild.default_role: nextcord.PermissionOverwrite(read_messages=False, send_messages=False),
                    #playerRole: nextcord.PermissionOverwrite(read_messages=True)
                }
                overwrites = {
                    self.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
                    #playerRole: nextcord.PermissionOverwrite(read_messages=True)
                }

                foundInterface = False
                foundChannel = False

                for channel in category.channels:
                    if channel.name.lower() == self.name.replace(' ', '-').lower() + '_interface':
                        print("Interface Channel was found for", self.name, "district.")
                        self.interfaceChannel = channel
                        foundInterface = True
                    elif channel.name.lower() == self.name.replace(' ', '-').lower():
                        print("Channel was found for", self.name, "district.")
                        self.channel = channel
                        foundChannel = True

                if not foundInterface:
                    self.interfaceChannel = await category.create_text_channel(self.name.replace(' ', '-') + '_interface', overwrites=interfaceOverwrites)

                if not foundChannel:
                    self.channel = await category.create_text_channel(self.name.replace(' ', '-'), overwrites=overwrites)

                interfaceMessages = await self.interfaceChannel.history(limit=None, oldest_first=True).flatten()
                self.interfaceMessage = None

                for interfaceMessage in interfaceMessages:
                    if interfaceMessage.author.id == theJar['client']:
                        self.interfaceMessage = interfaceMessage
                        break

                if self.interfaceMessage == None:
                     self.interfaceMessage = await Menus.districtMenu.send(self.interfaceChannel, state={'district': self.name})

                self.interfaceDirty = False
                
                return
        print("Error: Category not found. This may be due to the delay not long enough after the category is created.")

    # Ginger: Updates the interface message
    def updateInterface(self):
        self.interfaceDirty = True

    async def doInterfaceUpdate(self):
        self.interfaceDirty = False

        if hasattr(self, 'interfaceMessage'):
            await Menus.districtMenu.update(self.interfaceMessage, newState={'district': self.name})

    def setPath(self, target):
        can_path = True
        if len(target.paths) >= target.pathcap:
            can_path = False
        if len(self.paths) >= self.pathcap:
            can_path = False
        if can_path:
            if target not in self.paths:
                self.paths.append(target)
            if self not in target.paths:
                target.paths.append(self)

    def moveCheck(self, player):
        can_move = False
        if self in player.location.paths:
            can_move = player.modStat(theJar['resources']['Influence'], -1)
        return can_move

    #TODO: Need a function specifically for granting/removing channel permissions

    def movePlayer(self, player):
        #If player is already in a location, check if they can move. Otherwise, set it to true.
        if player.location:
            can_move = self.moveCheck(player)
            #If player is in location AND can move, remove them from the current location's player list.
            if can_move:
                player.location.players.remove(player)
                player.location.updateInterface()
                player.location.civics.delPlayer(player)
        else:
            can_move = True

        if can_move:
            self._movePlayer.start(player)
            return str(player) + " has moved to " + str(self)
        return "Error: " + str(player) + " is unable to move to " + str(self)
    
    @tasks.loop(seconds=1, count=1)
    async def _movePlayer(self, player):

        #Check if player is already in a location. Player may not be in a region at the start of initialization.
        if player.location:
            #if player is being moved to a different region, remove permissions from old region channel and category.
            if not player.location.region == self.region:
                category = nextcord.utils.get(self.guild.categories, name=player.location.region)
                await category.set_permissions(player.member, read_messages=False)
        
            #remove player from old district channel
            await theJar['regions'][player.location.region].channel.set_permissions(player.member, read_messages=False)
        player.location = self
        self.players.append(player)
        self.updateInterface()
        self.civics.addPlayer(player)
        await self.channel.set_permissions(player.member, read_messages=True)

    def __str__(self):
        return self.name

    def report(self):
        title = "-----"+str(self)+"-----\n"
        report = "*The "+str(self.region)+" Region*\n\n"
        fields = []

        player_rep = {'inline':True}
        player_rep['title'] = "-- Players Present:"
        player_rep['value'] = ''
        for player in self.players:
            player_rep['value'] += "- "+str(player)+"\n"
        player_rep['value'] = player_rep['value'][:-1]
        if len(player_rep['value']) == 0:
            player_rep['value'] = '- ...'
        fields.append(player_rep)

        path_rep = {'inline':True}
        path_rep['title'] = "-- Paths:"
        path_rep['value'] = ''
        for district in self.paths:
            path_rep['value'] += "- "+str(district)+"\n"
        path_rep['value'] = path_rep['value'][:-1]
        fields.append(path_rep)

        inv_report, inv_title, inv_fields = self.inventory.report()

        fields += inv_fields
        return report, title, fields

class Civics():
    def __init__(self, location):
        self.location = location
        self.players = [x for x in location.players]
        self.squad_list = []
        self.squads_ranked = {}
        self.allegiances = []
        self.commanders = []
        self.occupance = None
        self.governors = []
        self.governance = None
        #Stand, Attack, Defend, Retreat [Target Location]
        self.allegiance_stances = {}
        for alleg in theJar['allegiances'].keys():
            self.allegiance_stances[alleg] = {'stance': None}

    def addSquad(self, squad):
        if squad not in self.squad_list:
            self.squad_list.append(squad)
            squad.setPriority(squad.priority)
            #^Runs squad.getRank which runs self.getCommander

    def delSquad(self, squad):
        if squad in self.squad_list:
            self.squad_list.remove(squad)
            self.squads_ranked[squad.allegiance][squad.priority].remove(squad)
            self.getCommander(squad.allegiance)

    def addPlayer(self, player):
        if player not in self.players:
            self.players.append(player)
            self.addAllegiance(player.allegiance)
            self.getCommander(player.allegiance)

    def delPlayer(self, player):
        if player in self.players:
            if player.location != self.location:
                remove = True
                for squad in self.squad_list:
                    if squad.owner==player:
                        remove = False
                self.players.remove(player)
                self.getCommander(player.allegiance)

    def addAllegiance(self, allegiance):
        if allegiance not in self.allegiances:
            self.allegiances.append(allegiance)
            self.allegiance_stances[allegiance] = {'stance':'Stand'}

    def delAllegiance(self, allegiance):
        if allegiance in self.allegiances:
            self.allegiances.remove(allegiance)
            self.allegiance_stances[allegiance] = {'stance':None}

    def getGovernor(self, allegiance):
        candidates = []
        for player in self.players:
            if player.allegiance == allegiance:
                candidates.append(player)
        for building in self.location.inventory.slots['building']:
            if building.owner.allegiance == allegiance:
                if building.owner not in candidates:
                    candidates.append(building.owner)
        metrics = []
        alg_building_count = 0
        for cand in candidates:
            inf = cand._statcaps[theJar['resources']['Influence']]
            buildings = [x for x in cand.inventory.cards['building'] if x.location == self.location]
            metric = {'gov':cand, 'inf': inf, 'buildings': len(buildings)}
            metrics.append(metric)
            alg_building_count += len(buildings)
        metrics.sort(key=operator.itemgetter('inf','buildings'), reverse=True)
        if len(metrics) > 0:
            gov = metrics[0]
            try:
                old_gov = next(x for x in self.governors if x['allegiance']==allegiance)
                self.governors.remove(old_gov)
            except:
                pass
            self.governors.append({"gov":gov['gov'], 'allegiance':allegiance, 'inf':gov['inf'], 'buildings':alg_building_count})
        else:
            self.delAllegiance(allegiance)
        self.setGovernorRankings()

    def setGovernorRankings(self):
        self.governors.sort(key=operator.itemgetter('buildings','inf'))
        self.governance = self.governors[0]['allegiance']

    def getCommander(self, allegiance):
        candidates = []
        for player in self.players:
            if player.allegiance == allegiance:
                candidates.append(player)
        metrics = []
        squad_count = 0
        for cand in candidates:
            inf = cand._statcaps[theJar['resources']['Influence']]
            squads = [x for x in cand.squads if x.location == self.location]
            metric = {'cmd':cand, 'inf': inf, 'squads': len(squads)}
            metrics.append(metric)
            squad_count += len(squads)
        metrics.sort(key=operator.itemgetter('inf','squads'), reverse=True)
        if len(metrics) > 0:
            cmdr = metrics[0]
            try:
                old_cmdr = next(item for item in self.commanders if item['allegiance']==allegiance)
                self.commanders.remove(old_cmdr)
            except:
                pass
            self.commanders.append({"cmdr":cmdr['cmd'], 'allegiance':allegiance, 'inf':cmdr['inf'], 'squads':squad_count})
        else:
            self.delAllegiance(allegiance)
        self.setCommanderRankings()

    def setCommanderRankings(self):
        self.commanders.sort(key=operator.itemgetter('squads','inf'))
        self.occupance = self.commanders[0]['allegiance']

    def setStance(self, player, stance, target=None):
        if not target:
            stance_dict = {'stance': stance}
        else:
            stance_dict = {'stance': stance, 'target': target}
        commanders = [x['cmdr'] for x in self.commanders]
        if player in commanders:
            allegiance = player.allegiance
            self.allegiance_stances[allegiance] = stance_dict
            #if stance == "Attack":
               # self.joinConflict(player.allegiance, target)
        else:
            print('Error: Player is not a commander!')

    def setRetreat(self, allegiance, alt_location):
        if alt_location != self.location:
            self.retreats[allegiance] = alt_location

    def refresh(self):
        self.allegiance_stances = {}
        for alleg in theJar['allegiances'].keys():
            self.allegiance_stances[alleg] = {'stance':None}
        self.conflicts = []
        self.retreats = {}

    def report(self):
        fields = []
        title = "-----"+str(self.location)+" Civics-----"
        report = ''
        info_rep = {'inline':True}
        info_rep['title'] = '-- Info:'
        info_rep['value'] =  "\n- Location: "+str(self.location)+\
                             "\n- Players: "+str([str(x) for x in self.players])+\
                             "\n- Squads: "+str(self.squads_ranked)+\
                             "\n- Allegiances: "+str(self.allegiances)+\
                             "\n- Commanders: "+str([str(x['cmdr']) for x in self.commanders])+\
                             "\n- Occupance: "+str(self.occupance)+\
                             "\n- Governors: "+str([str(x['gov']) for x in self.governors])+\
                             "\n- Governance: "+str(self.governance)+\
                             "\n- Allegiance Stances: "+str(self.allegiance_stances)
        #info_rep['value'] += "\n- Units: "
        #for unit in self.units:
        #    value = unit.title
        #    info_rep['value'] += str(value)+"\n"
        #info_rep['value'] = info_rep['value'][:-2]
        fields.append(info_rep)
        return report, title, fields
