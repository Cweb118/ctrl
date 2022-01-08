import nextcord
from nextcord import slash_command
from nextcord import webhook
from nextcord.ext import commands

guilds = [588095612436742173, 778448646642728991]

class Sudo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @slash_command(name="sudo", guild_ids=guilds)
    async def sudo(self, ctx, channel, message):
        channel = nextcord.utils.get(ctx.guild.text_channels, name=channel)
        webhook = await channel.create_webhook(name="Test")
        await webhook.send(message, username="test", avatar_url="https://cdn.discordapp.com/attachments/825443696152543314/929510309239062568/Untitled-2.png")


def setup(bot):
    bot.add_cog(Sudo(bot))