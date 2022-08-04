import time
import nextcord
from _00_cogs.sudo import Sudo, sudo_profiles


def createEmbed(msg, title=None, color=None, fields=None):
    if not title:
        title = ''
    if not color:
        color = 0x8c8c8c
    embedded = nextcord.Embed(title=title, color=color, description=msg)
    if fields:
        for field in fields:
            embedded.add_field(name=field['title'], value=field['value'], inline=field['inline'])

    return embedded

async def say(ctx, msg, channel=None, title=None, color=None, fields=None, sudo=False):
    #Sends a message in the channel of interaction's origin (or otherwise, specified channel name)
    embedded = createEmbed(msg, title, color, fields)
    if not channel:
        channel = ctx.channel
    if sudo:
        await sudo_say(ctx, '', channel, embed=embedded)
    else:
        await channel.send(embed=embedded)

async def sudo_say(ctx, message, channel, profile='cn', embed=None):
    #Sends a message in the channel of interaction's origin (or otherwise, specified channel name) as a sudo profile
    if not channel:
        channel = ctx.channel
    webhook = await channel.create_webhook(name=time.time())
    if embed:
        await webhook.send(message, embed=embed, username=sudo_profiles[profile]["name"], avatar_url=sudo_profiles[profile]["pfp"])
    else:
        await webhook.send(message, username=sudo_profiles[profile]["name"], avatar_url=sudo_profiles[profile]["pfp"])
    await webhook.delete()
