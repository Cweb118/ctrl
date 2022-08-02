import time
import random

import nextcord
from nextcord import slash_command
from nextcord import webhook
from nextcord.ext import commands

guilds = [588095612436742173, 778448646642728991]

cn_opts = ['000?', '00??', '0???', '????', '?0??', '??0?', '0?0?', '00??', '?00?']
cn_id = cn_opts[random.randint(0,8)]
sudo_profiles = {
            "cn" : {"name" : "CN-"+cn_id, "pfp" : "https://media.discordapp.net/attachments/160848693044445184/929636685359222834/unknown.jpg?width=528&height=669"},
            "merchant" : {"name" : "The Merchant", "pfp" : "https://media.discordapp.net/attachments/825443696152543314/929653537682632725/frog_final_2.jpg?width=810&height=671"},
            "traveler" : {"name" : "The Traveler", "pfp" : "https://media.discordapp.net/attachments/160848693044445184/929636685359222834/unknown.jpg?width=528&height=669"},

            }
class Sudo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @slash_command(name="sudo", guild_ids=guilds)
    async def sudo_c(self, ctx, profile, channel, message):
        await self.sudo_f(ctx, profile, channel, message)

    async def sudo_f(self, ctx, profile, channel, message, embed):
        channel = nextcord.utils.get(ctx.guild.text_channels, name=channel)
        webhook = await channel.create_webhook(name=time.time())
        await webhook.send(message, embed=embed, username=sudo_profiles[profile]["name"], avatar_url=sudo_profiles[profile]["pfp"])
        await webhook.delete()

def setup(bot):
    bot.add_cog(Sudo(bot))
