from variables import bot, owner, client
from discord.ext import commands

@bot.command()
async def stop(ctx: commands.Context):
    if ctx.author.id != owner: return

    await ctx.reply("Shutting down...")
    client.close()
    await bot.close()