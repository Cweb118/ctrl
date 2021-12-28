import nextcord
from nextcord import slash_command
from nextcord.ext import commands
from _01_functions import *
from _00_cogs.mechanics.dice_class import Dice
from _00_cogs.mechanics.unit_classes.__unit_parent_class import Unit
from _00_cogs.mechanics.unit_classes._unit_kits import unit_kits_dict

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

#----------comms----------

    @slash_command(name="ping")
    async def ping(self, ctx):
        await send(ctx, 'Pog.')

    @commands.command(name="pm")
    async def pm_c(self, ctx, user: nextcord.Member):
        await player_pm(ctx, user)

    @commands.command(name='pa')
    @commands.has_role('control')
    async def pa_c(self, ctx, room):
        print('E')
        #await pa(ctx, room)

    @commands.command(name='shout')
    @commands.has_role('control')
    async def shout_c(self, ctx, channel: nextcord.TextChannel):
        await shout(ctx, channel)


#----------testing----------


    @commands.command(name="man")
    async def man(self, ctx, type):
        kit = list(unit_kits_dict[type])
        kit = [ctx.author.id]+kit
        man = Unit(*kit)
        report = "Unit Report: \n\n"+str(man)
        await say(ctx,report)
        await man.die_set.roll(ctx, man.stats['fortitude'])


    @commands.command(name="roll")
    async def roll_c(self, ctx, quantity, sides, threshold):
        die_set = Dice(int(quantity), int(sides))
        await die_set.roll(ctx, threshold)


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


