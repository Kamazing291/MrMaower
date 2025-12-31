from random import choice
import discord
from variables import bot, guild

@bot.tree.command(name="8-ball", description="tells your prophecy", guild=guild)
@discord.app_commands.describe(question="your question")
async def ball(interaction: discord.Interaction, question: str):
    answers = ["Yes", "No", "Maybe", "I don't know", "Ask me later", "The fact you're asking me, a program is kinda depressing ngl"]
    yon = ["am", "is ", "are ", "will ", "can ", "should ", "do ", "does ", "did ", "would ", "could ", "shall ", "might "]
    q = question.lower().strip()

    if not any(q.startswith(element) for element in yon):
        await interaction.response.send_message("Ask me a yes or no question, stupid!")
        return
    
    await interaction.response.send_message(f"{question}: {choice(answers)}")