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
        Region(name)
        report = "Region "+name+" created."
        await say(ctx,report)

    @commands.command(name="makedistrict", guild_ids=guilds)
    async def makedistrict_c(self, ctx, name, region_name, paths=None):
        district = District(name, region_name, paths)
        region = region_dict[region_name]
        region.addDistrict(district)
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
        await say(ctx,report)


    @commands.command(name="man", guild_ids=guilds)
    async def man_c(self, ctx, type):
        kit = list(unit_kits_dict[type])
        kit = [ctx.author]+kit
        man = Unit(*kit)
        report = str(man.report())
        await say(ctx,report)

    @commands.command(name="harvest", guild_ids=guilds)
    async def harvest_c(self, ctx):
        player = player_dict[ctx.author.id]
        for card in player.inventory.cards:
            report = card.harvest()
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

    @commands.command(name="cardrep", guild_ids=guilds)
    async def cardrep_c(self, ctx, card_number):
        player = player_dict[ctx.author.id]
        report = player.inventory.cardReport(int(card_number))
        await say(ctx,report)

    @commands.command(name="givecard", guild_ids=guilds)
    async def givecard_c(self, ctx, card_number, user: nextcord.Member):
        player = player_dict[ctx.author.id]
        report = player.inventory.moveCard(int(card_number), user)
        await say(ctx,report)

    @commands.command(name="giveres", guild_ids=guilds)
    async def giveres_c(self, ctx, resource_name, quantity: int, user: nextcord.Member):
        resource = resource_dict[resource_name]
        try:
            if quantity > 0:
                player = player_dict[ctx.author.id]
                target = player_dict[user.id]
                status = player.inventory.setResource(resource, -quantity)
                if status == True:
                    target.inventory.setResource(resource, quantity)
                    report = "You have given "+user.display_name+" "+str(quantity)+" "+str(resource)
                else:
                    report = "Error: Insufficient quantity of resource."
            else:
                report = "Error: Input less than zero."
        except:
            report = "Transaction Failed."
        await say(ctx,report)

    @commands.command(name="setres", guild_ids=guilds)
    async def setres_c(self, ctx, resource_name, quantity: int, user: nextcord.Member):
        resource = resource_dict[resource_name]
        try:
            if quantity > 0:
                target = player_dict[user.id]
                target.inventory.setResource(resource, quantity)
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


