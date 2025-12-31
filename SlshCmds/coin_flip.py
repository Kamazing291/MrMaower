import discord
from random import randint
from variables import bot, guild

@bot.tree.command(name="coin-flip", description="flip a coin", guild=guild)
async def flip(interaction: discord.Interaction):
    result = "heads" if randint(0, 1) == 0 else "tails"
    pic = discord.File(open(f"assets/{result}.png", "rb"))
    await interaction.response.send_message(result.upper(), file=pic)