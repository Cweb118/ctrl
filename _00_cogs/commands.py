import nextcord
from nextcord import slash_command
from nextcord.ext import commands
from _01_functions import *
from _02_global_dicts import player_dict, resource_dict, region_dict, district_dict
from _00_cogs.mechanics.dice_class import Dice
from _00_cogs.mechanics.resource_class import Resource
from _00_cogs.architecture.locations_class import Region, District
from _00_cogs.mechanics.unit_classes.__unit_parent_class import Unit
from _00_cogs.mechanics.unit_classes._unit_kits import unit_kits_dict

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


#----------testing----------

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

    @commands.command(name="region", guild_ids=guilds)
    async def region_c(self, ctx, name):
        region = region_dict[name]
        report = region.report()
        await say(ctx,report)

    @commands.command(name="district", guild_ids=guilds)
    async def district_c(self, ctx, name):
        district = district_dict[name]
        report = district.report()
        report = report+"\n\n"+district.inventory.report()
        await say(ctx,report)

    @commands.command(name="move", guild_ids=guilds)
    async def move_c(self, ctx, name):
        player = player_dict[ctx.author.id]
        district = district_dict[name]
        report = district.movePlayer(player)
        await say(ctx,report)

    @commands.command(name="roll", guild_ids=guilds)
    async def roll_c(self, ctx, quantity, sides, threshold):
        die_set = Dice(int(quantity), int(sides))
        await die_set.roll(ctx, threshold)

    @commands.command(name="inv", guild_ids=guilds)
    async def inv_c(self, ctx):
        player = player_dict[ctx.author.id]
        report = player.inventory.report()
        await say(ctx,report)

    @commands.command(name="man", guild_ids=guilds)
    async def man_c(self, ctx, type):
        player = player_dict[ctx.author.id]
        man = player.inventory.makeCard(unit_kits_dict[type], 'unit')
        report = str(man.report())
        await say(ctx,report)

    @commands.command(name="unitmove", guild_ids=guilds)
    async def unitmove_c(self, ctx, card_type, card_number, target_type, target):
        player = player_dict[ctx.author.id]
        card = player.inventory.getCard(card_type, int(card_number))
        if target_type == 'district':
            destination = district_dict[target]
        elif target_type == 'unit':
            destination = player.inventory.getCard(target_type, int(target))
        report = card.moveUnit(target_type, destination)
        await say(ctx,report)


    @commands.command(name="harvest", guild_ids=guilds)
    async def harvest_c(self, ctx):
        player = player_dict[ctx.author.id]
        for card in player.inventory.cards['unit']:
            if card.status == "Played":
                report = card.harvest()
                await say(ctx,report)

    @commands.command(name="stats", guild_ids=guilds)
    async def stats_c(self, ctx):
        player = player_dict[ctx.author.id]
        report = player.report()
        await say(ctx,report)

    @commands.command(name="cardrep", guild_ids=guilds)
    async def cardrep_c(self, ctx, card_type, card_number):
        player = player_dict[ctx.author.id]
        report = player.inventory.cardReport(card_type, int(card_number))
        await say(ctx,report)

    @commands.command(name="cardnick", guild_ids=guilds)
    async def cardnick_c(self, ctx, card_type, card_number, nick):
        player = player_dict[ctx.author.id]
        card = player.inventory.cards[card_type][int(card_number)-1]
        report = card.setNick(nick)
        report = player.inventory.cardReport(card_type, int(card_number))
        await say(ctx,report)

    @commands.command(name="playcard", guild_ids=guilds)
    async def playcard_c(self, ctx, card_type, card_number, target_type, target):
        player = player_dict[ctx.author.id]
        card = player.inventory.cards[card_type][int(card_number)-1]
        targ = None
        if target_type == 'district':
            targ = district_dict[target]
        elif target_type == 'unit':
            targ = player.inventory.cards[target_type][int(target)-1]
        elif target_type == 'building':
            targ = player.inventory.cards[target_type][int(target)-1]
        if targ:
            status = card.playCard(player, targ)
            if status:
                report = str(card)+" successfully played to "+str(targ)
            else:
                report = 'Error: One or more requirements not met.'
        else:
            report = 'Error: Invalid location.'
        await say(ctx,report)

    @commands.command(name="givecard", guild_ids=guilds)
    async def givecard_c(self, ctx, card_type, card_number, user: nextcord.Member):
        player = player_dict[ctx.author.id]
        report = player.inventory.moveCard(card_type, int(card_number), user)
        await say(ctx,report)

    @commands.command(name="givecard", guild_ids=guilds)
    async def givecard_c(self, ctx, card, target_obj):
        player = player_dict[ctx.author.id]
        status = target_obj.inventory.playCard(self, card, player, target_obj)

    @commands.command(name="giveres", guild_ids=guilds)
    async def giveres_c(self, ctx, resource_name, quantity: int, user: nextcord.Member):
        resource = resource_dict[resource_name]
        giver = player_dict[ctx.author.id]
        taker = player_dict[user.id]
        report = giver.inventory.giveResource(resource, quantity, giver, taker)
        await say(ctx,report)

    @commands.command(name="dropres", guild_ids=guilds)
    async def dropres_c(self, ctx, resource_name, quantity: int, target_type, target):
        resource = resource_dict[resource_name]
        giver = player_dict[ctx.author.id]
        report = giver.inventory.dropres(resource, quantity, target_type, target)
        await say(ctx,report)

    @commands.command(name="unitdropres", guild_ids=guilds)
    async def unitdropres_c(self, ctx, unit_type, unit_number, resource_name, quantity: int, target_type, target):
        resource = resource_dict[resource_name]
        player = player_dict[ctx.author.id]
        giver = player.inventory.getCard(unit_type, unit_number)
        report = giver.inventory.dropres(resource, quantity, target_type, target)
        await say(ctx,report)

    @commands.command(name="takeres", guild_ids=guilds)
    async def takeres_c(self, ctx, resource_name, quantity: int, target_type, target):
        resource = resource_dict[resource_name]
        taker = player_dict[ctx.author.id]
        report = taker.inventory.takeres(resource, quantity, target_type, target)
        await say(ctx,report)

    @commands.command(name="unittakeres", guild_ids=guilds)
    async def unittakeres_c(self, ctx, unit_type, unit_number, resource_name, quantity: int, target_type, target):
        resource = resource_dict[resource_name]
        player = player_dict[ctx.author.id]
        taker = player.inventory.getCard(unit_type, unit_number)
        report = taker.inventory.takeres(resource, quantity, target_type, target)
        await say(ctx,report)




    @commands.command(name="addres", guild_ids=guilds)
    async def addres_c(self, ctx, resource_name, quantity: int, user: nextcord.Member):
        resource = resource_dict[resource_name]
        try:
            if quantity > 0:
                target = player_dict[user.id]
                target.inventory.addResource(resource, quantity)
                report = "You have gained "+str(quantity)+" "+str(resource)
            else:
                report = "Error: Insufficient quantity of resource."
        except:
            report = "Transaction Failed."
        await say(ctx,report)

    @commands.command(name="resource", guild_ids=guilds)
    async def res_c(self, ctx, resource_name):
        resource = resource_dict[resource_name]
        report = resource.report()
        await say(ctx,report)

"""
@bot.command()
async def player_init(ctx):
    for channel in nextcord.utils.get(ctx.guild.categories, name='Players').channels:
        await channel.delete()

    for player in nextcord.utils.get(ctx.guild.roles, name='player').members:
        print("Processing "+player.display_name)
        category = nextcord.utils.get(ctx.guild.categories, name='Players')
        overwrites = {
            ctx.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            player: nextcord.PermissionOverwrite(read_messages=True),
        }
        await ctx.message.guild.create_text_channel(player.display_name.lower(), category=category, overwrites=overwrites)
    await say(ctx, "playerinit complete!")

@bot.command()
async def interface_init(ctx):
    for channel in nextcord.utils.get(ctx.guild.categories, name='Interface').channels:
        await channel.delete()

    for player in nextcord.utils.get(ctx.guild.roles, name='player').members:
        print("Processing "+player.display_name)
        category = nextcord.utils.get(ctx.guild.categories, name='Interface')
        overwrites = {
            ctx.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            player: nextcord.PermissionOverwrite(read_messages=True),
        }
        name = player.display_name.lower().replace(" ",'-')+"_interface"
        print(name)
        await ctx.message.guild.create_text_channel(name, category=category, overwrites=overwrites)

        channel = nextcord.utils.get(ctx.guild.channels, name=name)
        options = [
            nextcord.SelectOption(label="Red", description="The color red!"),
            nextcord.SelectOption(label="Blue", description="The color blue!")
        ]
        select = nextcord.ui.Select(custom_id=name+"_colorsel", placeholder="Select a color!", options=options)
        view = nextcord.ui.View()
        view.add_item(select)
        print(view)

        await channel.send("Choose!", view=view)
    await say(ctx, "interfaceinit complete!")
 """

def setup(bot):
    bot.add_cog(Commands(bot))


