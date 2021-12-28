import nextcord

async def say(ctx, msg):
    if "```" not in msg:
        response = "```\n"+msg+"```"
    else:
        response = msg
    await ctx.send(response)


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
