import nextcord
from nextcord.ext import commands
from _99_functions import *
from _00_cogs.dice.dice import roll_dice

class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command
    async def ping(self, ctx):
        await reply(ctx, 'Pog.')

    @commands.command
    async def roll(self, ctx, quant, sides, succ):
        report_dict = roll_dice(int(quant), int(sides), int(succ))
        if report_dict['result']:
            status = "SUCCESS"
        else:
            status = "FAILURE"
        report_str = "-----Results-----\n\n"+"Rolls: "+str(report_dict['rolls'])+"\n"+"Hits: "+str(report_dict['hits'])+"\n"+"Hit Count: "+str(report_dict['hit_count'])
        await reply(ctx, status)
        await say(ctx, str(report_str))

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


