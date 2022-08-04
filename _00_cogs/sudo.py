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
            "cn" : {"name" : "CN-"+cn_id, "pfp" : "https://cdn.discordapp.com/attachments/1004377757561651281/1004377851144978552/CN002.png"},
            "merchant" : {"name" : "The Merchant", "pfp" : "https://cdn.discordapp.com/attachments/1004377757561651281/1004377891762614392/The_Merchant.png"},
            "traveler" : {"name" : "The Traveler", "pfp" : "https://cdn.discordapp.com/attachments/1004377757561651281/1004377972691710062/firefox_qMni7BDnMw.png"},

            }
class Sudo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    #@slash_command(name="sudo", guild_ids=guilds)
    #async def sudo_c(self, ctx, profile, channel, message):
        #await self.sudo_f(ctx, profile, message, channel)

    async def sudo_f(self, ctx, profile, message, channel=None, embed=None):
        if channel:
            channel = nextcord.utils.get(ctx.guild.text_channels, name=channel)
        else:
            channel = ctx.channel
        webhook = await channel.create_webhook(name=time.time())
        await webhook.send(message, embed=embed, username=sudo_profiles[profile]["name"], avatar_url=sudo_profiles[profile]["pfp"])
        await webhook.delete()

def setup(bot):
    bot.add_cog(Sudo(bot))
