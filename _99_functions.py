


async def say(ctx, msg):
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
