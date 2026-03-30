from os import getenv
import discord
from variables import bot, guild, agent

@bot.tree.command(name="ask", description="ask me a question", guild=guild)
@discord.app_commands.describe(prompt="your prompt")
async def ask(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()

    messages = [{"role": "user", "content": prompt}]

    try:
        response = agent.beta.conversations.start(
            agent_id=getenv("AGENT_ID"), 
            inputs=messages
        )
        
        await interaction.followup.send(f"{prompt}: ")
        await interaction.followup.send(response.outputs[0].content)
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")