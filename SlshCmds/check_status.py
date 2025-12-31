import discord
from variables import bot, guild

@bot.tree.command(name="check-status", description="check the bot's status", guild=guild)
async def check_status(interaction: discord.Interaction):
    await interaction.response.send_message("Working Perfectly! :D")