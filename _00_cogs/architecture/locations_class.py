from _02_global_dicts import theJar
import nextcord
import time, asyncio
from nextcord.ext import tasks
from _00_cogs.architecture.inventory_class import Inventory

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
        self.inventory = None
        self.guild = guild
        self.size = size

        if guild:
            self.guildID = guild.id
        else:
            self.guildID = guildID

        if guild:
            self.createChannel.start()

        sizes = {
            #inv_args: [r_cap=None, r_cont=None, u_cap=None, b_cap=None, u_slotcap=None, b_slotcap=None]
            'tiny': [self, 100, None, 10, 10, 2, 0],
            'small': [self, 100, None, 10, 10, 5, 2],
            'medium': [self, 100, None, 10, 10, 8, 4],
            'large': [self, 100, None, 10, 10, 13, 8],
            'huge': [self, 100, None, 10, 10, 20, 14],
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
            paths = paths.split(',')
            paths = [i for i in paths if i != '']
            for path in paths:
                district = theJar['districts'][path]
                self.setPath(district)

        theJar['regions'][region_name].addDistrict(self)
        theJar['districts'][name] = self
    
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
                for channel in category.channels:
                    if channel.name.lower() == self.name.lower():
                        print("Channel was found for", self.name, "district.")
                        self.channel = channel
                        return

                self.channel = await category.create_text_channel(self.name)
                await self.channel.set_permissions(self.guild.default_role, read_messages=False)
                await self.channel.set_permissions(playerRole, read_messages = True)
                return
        print("Error: Category not found. This may be due to the delay not long enough after the category is created.")


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

    def movePlayer(self, player):
        #If player is already in a location, check if they can move. Otherwise, set it to true.
        if player.location:
            can_move = self.moveCheck(player)
            #If player is in location AND can move, remove them from the current location's player list.
            if can_move:
                player.location.players.remove(player)
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
