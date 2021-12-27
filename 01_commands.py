import nextcord
from keys import *
from nextcord.ext import commands
bot = commands.Bot(command_prefix='!')

@bot.command()
async def ping(ctx):
    await ctx.reply('Pog!')

print("Connected to server "+prime_guild+"!")
bot.run(prime_token)

