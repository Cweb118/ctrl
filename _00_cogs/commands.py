from discord import Interaction
from nextcord import slash_command
from nextcord.ext import commands

from _00_cogs.architecture.player_fabs_class import Fab
from _01_functions import *
from info_dict import info_dict
from _02_global_dicts import theJar
from _00_cogs.mechanics.dice_class import Dice
from _00_cogs.mechanics.resource_class import Resource
from _00_cogs.architecture.locations_class import Region, District
from _00_cogs.mechanics.unit_classes.__unit_parent_class import Unit, Squad
from _00_cogs.mechanics.building_classes.__building_parent_class import Building
from _00_cogs.mechanics.building_classes._building_kits import building_kits_dict
from _00_cogs.mechanics.battle_logic import battle

guilds = [588095612436742173, 778448646642728991]

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

#----------comms----------

    @slash_command(name="ping", guild_ids=guilds)
    async def ping(self, ctx):
        await send(ctx, 'Pog.')

    @commands.command(name="pm", guild_ids=guilds)
    async def pm_c(self, ctx, user: nextcord.Member):
        await player_pm(ctx, user)

    @commands.command(name='pa', guild_ids=guilds)
    @commands.has_role('control')
    async def pa_c(self, ctx, room):
        print('E')
        #await pa(ctx, room)

    @commands.command(name='shout', guild_ids=guilds)
    @commands.has_role('control')
    async def shout_c(self, ctx, channel: nextcord.TextChannel):
        await shout(ctx, channel)

#----------player----------

    @slash_command(name="region", guild_ids=guilds)
    async def region_c(self, ctx: Interaction, name):
        await self.region_f(ctx, name)

    async def region_f(self, ctx, name):
        region = theJar['regions'][name]
        report, title, fields = region.report()
        await say(ctx, report, title=title, fields=fields)


    @slash_command(name="district", guild_ids=guilds)
    async def district_c(self, ctx: Interaction, name):
        await self.district_f(ctx, name)

    async def district_f(self, ctx, name):
        district = theJar['districts'][name]
        report, title, fields = district.report()
        await say(ctx, report, title=title, fields=fields)


    @slash_command(name="move", guild_ids=guilds)
    async def move_c(self, ctx: Interaction, name):
        await self.move_f(ctx, name)

    async def move_f(self, ctx, name):
        player = theJar['players'][ctx.user.id]
        district = theJar['districts'][name]
        report = district.movePlayer(player)
        await say(ctx,report)


    @slash_command(name="inv", guild_ids=guilds)
    async def inv_c(self, ctx: Interaction):
        await self.inv_f(ctx)

    async def inv_f(self, ctx):
        player = theJar['players'][ctx.user.id]
        report, title, fields = player.inventory.report()
        await say(ctx, report, title=title, fields=fields)

    @slash_command(name="stats", guild_ids=guilds)
    async def stats_c(self, ctx: Interaction):
        await self.stats_f(ctx)

    async def stats_f(self, ctx):
        player = theJar['players'][ctx.user.id]
        report, title, fields = player.report()
        await say(ctx, report, title=title, fields=fields)


    @slash_command(name="resource", guild_ids=guilds)
    async def resource_c(self, ctx: Interaction, resource_name):
        await self.resource_f(ctx, resource_name)

    async def resource_f(self, ctx, resource_name):
        resource = theJar['resources'][resource_name]
        report = resource.report()
        await say(ctx, report)

    #OLD:
    """
    @commands.command(name="cardrep", guild_ids=guilds)
    async def cardrep_c(self, ctx, card_type, card_number):
        player = theJar['players'][ctx.user.id]
        report, title, fields = player.inventory.cardReport(card_type, int(card_number))
        await say(ctx, report, title=title, fields=fields)

    @commands.command(name="link", guild_ids=guilds)
    async def link_c(self, ctx, building_child_number, building_parent_number):
        player = theJar['players'][ctx.user.id]
        building_child = player.inventory.getCard('building', int(building_child_number))
        building_parent = player.inventory.getCard('building', int(building_parent_number))
        building_parent.addLink(building_child)

    @slash_command(name="playcard", guild_ids=guilds)
    async def playcard_c(self, ctx: Interaction, card_type, card_number, target_type, target):
        await self._playcard_c(ctx, card_type, card_number, target_type, target)

    async def _playcard_c(self, ctx: Interaction, card_type, card_number, target_type, target):
        player = theJar['players'][ctx.user.id]
        card = player.inventory.cards[card_type][int(card_number)-1]
        targ = None
        if target_type == 'district':
            targ = theJar['districts'][target]
        elif target_type == 'unit':
            targ = player.inventory.cards[target_type][int(target)-1]
        elif target_type == 'building':
            targ = player.inventory.cards[target_type][int(target)-1]
        if targ:
            can_play, report = card.playCard(player, targ)
        else:
            report = 'Error: Invalid location.'
        await say(ctx,report)

    @commands.command(name="unplaycard", guild_ids=guilds)
    async def unplaycard_c(self, ctx, card_type, card_number):
        player = theJar['players'][ctx.user.id]
        card = player.inventory.cards[card_type][int(card_number)-1]
        report = card.unplayCard(player)
        await say(ctx,report)

    @commands.command(name="unitmove", guild_ids=guilds)
    async def unitmove_c(self, ctx, card_type, card_number, target_type, target):
        player = theJar['players'][ctx.user.id]
        card = player.inventory.getCard(card_type, int(card_number))
        if target_type == 'district':
            destination = theJar['districts'][target]
        elif target_type == 'unit':
            destination = player.inventory.getCard(target_type, int(target))
        report = card.moveUnit(target_type, destination)
        await say(ctx,report)

    @commands.command(name="cardnick", guild_ids=guilds)
    async def cardnick_c(self, ctx, card_type, card_number, nick):
        player = theJar['players'][ctx.user.id]
        card = player.inventory.cards[card_type][int(card_number)-1]
        report = card.setNick(nick)
        report = player.inventory.cardReport(card_type, int(card_number))
        #await say(ctx,report)

    @commands.command(name="givecard", guild_ids=guilds)
    async def givecard_c(self, ctx, card_type, card_number, user: nextcord.Member):
        player = theJar['players'][ctx.user.id]
        report = player.inventory.moveCard(card_type, int(card_number), user)
        await say(ctx,report)

    @commands.command(name="giveres", guild_ids=guilds)
    #player gives resource to another player
    async def giveres_c(self, ctx, resource_name, quantity: int, user: nextcord.Member):
        resource = theJar['resources'][resource_name]
        giver = theJar['players'][ctx.user.id]
        taker = theJar['players'][user.id]
        report = giver.inventory.giveResource(resource, quantity, giver, taker)
        await say(ctx,report)

    @commands.command(name="dropres", guild_ids=guilds)
    #player drops a resource into a target destination (location, unit, building)
    async def dropres_c(self, ctx, resource_name, quantity: int, target_type, target):
        resource = theJar['resources'][resource_name]
        giver = theJar['players'][ctx.user.id]
        report = giver.inventory.dropres(resource, quantity, target_type, target)
        await say(ctx,report)

    @commands.command(name="unitdropres", guild_ids=guilds)
    #a unit drops a unit to a target destination (location, unit, building) as directed by a player
    async def unitdropres_c(self, ctx, unit_type, unit_number, resource_name, quantity: int, target_type, target):
        resource = theJar['resources'][resource_name]
        player = theJar['players'][ctx.user.id]
        giver = player.inventory.getCard(unit_type, unit_number)
        report = giver.inventory.dropres(resource, quantity, target_type, target)
        await say(ctx,report)

    @commands.command(name="takeres", guild_ids=guilds)
    #a player takes a resource from a public storage (location, unit, building)
    async def takeres_c(self, ctx, resource_name, quantity: int, target_type, target):
        resource = theJar['resources'][resource_name]
        taker = theJar['players'][ctx.user.id]
        report = taker.inventory.takeres(resource, quantity, target_type, target)
        await say(ctx,report)

    @commands.command(name="unittakeres", guild_ids=guilds)
    #a unit takes a resource from a public storage (location, unit, building) as directed by a player
    async def unittakeres_c(self, ctx, unit_type, unit_number, resource_name, quantity: int, target_type, target):
        resource = theJar['resources'][resource_name]
        player = theJar['players'][ctx.user.id]
        taker = player.inventory.getCard(unit_type, unit_number)
        report = taker.inventory.takeres(resource, quantity, target_type, target)
        await say(ctx,report)

    """


#----------testing/control----------
    @slash_command(name="play", guild_ids=guilds)
    async def play_c(self, ctx: Interaction):
        player = theJar['players'][ctx.user.id]
        #player.inventory.addCard(Building(*building_kits_dict['wooden_wall']), 'building')
        #player.inventory.addCard(Building(*building_kits_dict['mother_tree']), 'building')
        #player.inventory.addCard(Building(*building_kits_dict['bountiful_field']), 'building')
        #player.addCard(building_kits_dict['mother_tree'], 'building')
        #player.addCard(building_kits_dict['bountiful_field'], 'building')
        await self.makeunit_f(ctx, ['Aratori'])
        await self.makeunit_f(ctx, ['Prismari'])
        await self.makeunit_f(ctx, ['Warrior'])
        await self.makeunit_f(ctx, ['Warrior', 'Aratori'])
        #await self.cardrep_c(ctx, 'unit', 1)
        #await self.cardrep_c(ctx, 'unit', 2)
        #await self.cardrep_c(ctx, 'unit', 3)
        #await self.cardrep_c(ctx, 'unit', 4)
        man = player.inventory.getCard('unit', 4)
        man.delTrait('Aratori')
        #await self.cardrep_c(ctx, 'unit', 4)
        man.addTrait('Prismari')
        #await self.cardrep_c(ctx, 'unit', 4)
        #await self._makeunit_c(ctx, ['Ranger', 'Aratori'])
        #await self._makeunit_c(ctx, ['Guardian', 'Aratori'])
        #await self._makeunit_c(ctx, ['Alchemist', 'Otavan'])
        #await self._makeunit_c(ctx, ['Worker', 'Automata'])

        #await self.makefab_c(ctx, "Tim the Bandit King", 'Home', 'Bandits')
        await self.move_f(ctx, 'Home')

        #await self._playcard_c(ctx, 'building', 1, 'district', 'Home')
        #await self._playcard_c(ctx, 'building', 2, 'district', 'Home')
        #await self._playcard_c(ctx, 'building', 3, 'district', 'Home')
        #await self.playcard_c(ctx, 'building', 2, 'district', 'Home')
        #await self.link_c(ctx, 2, 1)
        #await self._playcard_c(ctx, 'unit', 4, 'district', 'Home')
        #await self.cardnick_c(ctx, 'unit', 4, 'Tim')
        #await self._playcard_c(ctx, 'unit', 3, 'district', 'Home')
        #await self.cardnick_c(ctx, 'unit', 3, 'Tom')
        #await self.playcard_c(ctx, 'unit', 3, 'district', 'Home')
        #await self.cardnick_c(ctx, 'unit', 3, 'Tem')

        #await self.joinsquad_c(ctx, 2, 1)
        #await self.playcard_c(ctx, 'unit', 4, 'district', 'Home')
        #await self.cardnick_c(ctx, 'unit', 4, 'Bob')
        #await self.playcard_c(ctx, 'unit', 5, 'district', 'Home')
        #await self.cardnick_c(ctx, 'unit', 5, 'B0b')

    @slash_command(name="cartplay", guild_ids=guilds)
    async def cartplay_c(self, ctx: Interaction):
        player = theJar['players'][ctx.user.id]
        #player.faction = 'Bandit'
        await self.move_f(ctx, 'Home')
        await self.makeunit_f(ctx, ['Warrior', 'Aratori'])
        await self.makeunit_f(ctx, ['Warrior', 'Aratori'])
        await self.makeunit_f(ctx, ['Warrior', 'Aratori'])
        await self.makeunit_f(ctx, ['Warrior', 'Aratori'])
        await self.makeunit_f(ctx, ['Ranger', 'Aratori'])
        await self.makeunit_f(ctx, ['Ranger', 'Aratori'])
        await self.makeunit_f(ctx, ['Ranger', 'Aratori'])
        await self.makeunit_f(ctx, ['Ranger', 'Aratori'])
        await self.makeunit_f(ctx, ['Guardian', 'Aratori'])
        await self.makeunit_f(ctx, ['Guardian', 'Aratori'])
        await self.makeunit_f(ctx, ['Guardian', 'Aratori'])
        await self.makeunit_f(ctx, ['Guardian', 'Aratori'])
        await self.makeunit_f(ctx, ['Knight', 'Aratori'])
        await self.makeunit_f(ctx, ['Knight', 'Aratori'])
        await self.makeunit_f(ctx, ['Knight', 'Aratori'])
        await self.makeunit_f(ctx, ['Knight', 'Aratori'])
        await self.makeunit_f(ctx, ['Alchemist', 'Aratori'])
        await self.makeunit_f(ctx, ['Alchemist', 'Aratori'])
        await self.makeunit_f(ctx, ['Alchemist', 'Aratori'])
        await self.makeunit_f(ctx, ['Alchemist', 'Aratori'])
        i = 1
        while i < 21:
            await self._playcard_c(ctx, 'unit', i, 'district', 'Home')
            i += 1
        await self.joinsquad_c(ctx, 5, 1)
        await self.joinsquad_c(ctx, 10, 1)
        await self.joinsquad_c(ctx, 15, 1)

    @commands.command(name="makefab", guild_ids=guilds)
    async def makefab_c(self, ctx, name, region, alg):
        player = theJar['players'][ctx.user.id]
        Fab(player, name, theJar['districts'][region], alg)
        report = "Fab \""+name+"\" created."
        await say(ctx,report)

    @commands.command(name="fabrep", guild_ids=guilds)
    async def fabrep_c(self, ctx, name):
        fab = theJar['fabs'][name]
        report = fab.report()
        await say(ctx,report)

    @commands.command(name="fabplaycard", guild_ids=guilds)
    async def fabplaycard_c(self, ctx, name, card_type, card_number, target_type, target):
        fab = theJar['fabs'][name]
        card = fab.inventory.cards[card_type][int(card_number)-1]
        targ = None
        if target_type == 'district':
            targ = theJar['districts'][target]
        elif target_type == 'unit':
            targ = fab.inventory.cards[target_type][int(target)-1]
        elif target_type == 'building':
            targ = fab.inventory.cards[target_type][int(target)-1]
        if targ:
            can_play, report = card.playCard(fab, targ)
        else:
            report = 'Error: Invalid location.'
        await say(ctx,report)


    @commands.command(name="makeregion", guild_ids=guilds)
    async def makeregion_c(self, ctx, name):
        Region(name, guild=ctx.guild)
        report = "Region "+name+" created."
        await say(ctx,report)

    @commands.command(name="makedistrict", guild_ids=guilds)
    async def makedistrict_c(self, ctx, name, region_name, size, paths=None):
        District(name, region_name, size, paths, guild=ctx.guild)
        report = "District "+name+" created in the "+region_name+" region."
        await say(ctx,report)


    @slash_command(name="addres", guild_ids=guilds)
    async def addres_c(self, ctx: Interaction, resource_name, quantity: int, user: nextcord.Member):
        await self.addres_f(ctx, resource_name, quantity, user)

    async def addres_f(self, ctx, resource_name, quantity: int, user: nextcord.Member):
        resource = theJar['resources'][resource_name]
        try:
            if quantity > 0:
                target = theJar['players'][user.id]
                target.inventory.addResource(resource, quantity)
                report = "You have gained "+str(quantity)+" "+str(resource)
            else:
                report = "Error: Insufficient quantity of resource."
        except:
            report = "Transaction Failed."
        await say(ctx,report)

    @slash_command(name="countstr", guild_ids=guilds)
    async def addres_c(self, ctx: Interaction, location):
        await self.countstr_f(ctx, location)

    async def countstr_f(self, ctx, location):
        district = theJar['districts'][location]
        report = district.civics.strReport()
        await say(ctx,report)

    @slash_command(name="raiseinf", guild_ids=guilds)
    async def raiseinf_c(self, ctx: Interaction, user: nextcord.Member, quantity: int, ):
        await self.raiseinf_f(ctx, user, quantity)

    async def raiseinf_f(self, ctx, user, quantity):
        player = theJar['players'][user.id]
        player.modStatCap(theJar['resources']['Influence'], quantity)


    @slash_command(name="makeunit", guild_ids=guilds)
    async def makeunitd_c(self, ctx: Interaction, traits):
        await self.makeunit_f(ctx, traits)

    async def makeunit_f(self, ctx: Interaction, traits):
        player = theJar['players'][ctx.user.id]
        status, man = player.inventory.addCard(Unit(), 'unit')
        for trait in traits:
            man.addTrait(trait)
        report = str(man.report())
        await say(ctx,report)

    @commands.command(name="unitmove", guild_ids=guilds)
    async def unitmove_c(self, ctx, card_type, card_number, target_type, target):
        player = theJar['players'][ctx.user.id]
        card = player.inventory.getCard(card_type, int(card_number))
        if target_type == 'district':
            destination = theJar['districts'][target]
        elif target_type == 'unit':
            destination = player.inventory.getCard(target_type, int(target))
        can_move, report = card.moveUnit(target_type, destination)
        await say(ctx,report)

    @commands.command(name="unitaction", guild_ids=guilds)
    async def unit_action_c(self, ctx, action_name, action_arg, card_type, card_number, target_type, target_id):
        player = theJar['players'][ctx.user.id]
        actor = player.inventory.getCard(card_type, int(card_number))
        actee = None
        trait_action = None
        #cover all possible cases pls
        if target_type == 'district':
            actee = theJar['districts'][target_id]
        elif target_type == 'unit':
            actee = player.inventory.getCard(target_type, int(target_id))

        if len(actor.traits['on_act']) > 0:
            for trait in actor.traits['on_act']:
                if trait.trait_title == action_name:
                    trait_action = trait

        if trait_action and actee:
            action_report = trait_action.action.act(actor, actee, action_arg)


    @commands.command(name="info", guild_ids=guilds)
    async def run_c(self, ctx, argu):
        try:
            info = info_dict[argu.lower()]
            await say(ctx, info['info'], title=info['title'])
        except:
            await say(ctx, 'Error: No results for query \''+argu+'\'')


#-----Squads-----
    @commands.command(name="joinsquad", guild_ids=guilds)
    async def joinsquad_c(self, ctx, unit_number, join_unit_number):
        try:
            player = theJar['players'][ctx.user.id]
        except:
            player = theJar['players'][ctx.user.id]
        joiner = player.inventory.getCard('unit', int(unit_number))
        joinee = player.inventory.getCard('unit', int(join_unit_number))
        if joiner.location == joinee.location:
            if joinee.squad:
                joinee.squad.addUnit(joiner)
            else:
                squad_units = [joinee, joiner]
                Squad(squad_units)

    @commands.command(name="squad", guild_ids=guilds)
    async def squad_c(self, ctx, squad_id):
        player = theJar['players'][ctx.user.id]
        squad = player.squads[int(squad_id)-1]
        report, title, fields = squad.report()
        await say(ctx, report, title=title, fields=fields)

    @commands.command(name="squadmove", guild_ids=guilds)
    async def squadmove_c(self, ctx, squad_id, target_type, target):
        player = theJar['players'][ctx.user.id]
        squad = player.squads[int(squad_id)-1]
        if target_type == 'district':
            destination = theJar['districts'][target]
        #elif target_type == 'unit':
        #    destination = player.inventory.getCard(target_type, int(target))
        report = squad.moveSquad(target_type, destination)
        await say(ctx,report)


    @commands.command(name="civics", guild_ids=guilds)
    async def civics_c(self, ctx, location):
        location = theJar['districts'][location]
        civ = location.civics
        report, title, fields = civ.report()
        await say(ctx, report, title=title, fields=fields)


    @commands.command(name="stance", guild_ids=guilds)
    async def stance_c(self, ctx, location, stance):
        player = theJar['players'][ctx.user.id]
        location = theJar['districts'][location]
        civ = location.civics
        civ.setStance(player, stance)
        report, title, fields = civ.report()
        await say(ctx, report, title=title, fields=fields)

def setup(bot):
    bot.add_cog(Commands(bot))


