import time
import nextcord
from nextcord import slash_command
from nextcord import webhook
from nextcord.ext import commands

guilds = [588095612436742173, 778448646642728991]
profiles = {"merchant" : {"name" : "The Merchant", "pfp" : "https://media.discordapp.net/attachments/825443696152543314/929653537682632725/frog_final_2.jpg?width=810&height=671"},
            "traveler" : {"name" : "The Traveler", "pfp" : "https://media.discordapp.net/attachments/160848693044445184/929636685359222834/unknown.jpg?width=528&height=669"}}
class Sudo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @slash_command(name="sudo", guild_ids=guilds)
    async def sudo(self, ctx, profile, channel, message):
        channel = nextcord.utils.get(ctx.guild.text_channels, name=channel)
        webhook = await channel.create_webhook(name=time.time())
        await webhook.send(message, username=profiles[profile]["name"], avatar_url=profiles[profile]["pfp"])
        await webhook.delete()

def setup(bot):
    bot.add_cog(Sudo(bot))