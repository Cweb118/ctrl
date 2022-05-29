import nextcord

async def say(ctx, msg, title=None, color=None, fields=None):
    embedded = createEmbed(msg, title, color, fields)
    await ctx.send(embed = embedded)

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

async def send(ctx, msg):
    if "```" not in msg:
        response = "```\n"+msg+"```"
    else:
        response = msg
    await ctx.send(response)


async def reply(ctx, msg):
    if "```" not in msg:
        response = "```\n"+msg+"```"
    else:
        response = msg
    await ctx.reply(response)


async def player_pm(ctx, user):
    content = ctx.message.content.split('\"')[1]
    priv = nextcord.utils.get(ctx.guild.channels, name=user.display_name.lower())
    response = "```NEW MESSAGE:```"+"```"+content+"```"
    await priv.send(response)


async def shout(ctx, channel):
    content = ctx.message.content.split('\"')[1]
    response = "```"+content+"```"
    await channel.send(response)
