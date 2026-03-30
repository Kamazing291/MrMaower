from os import getenv
import discord
from variables import bot, guild, agent, client

CW = 20
collection = client["main"]["AI"]

def get_history():
    doc = collection.find_one({"_id": "shared"})
    return doc["messages"] if doc else []

def save_message(role: str, content: str):
    collection.update_one(
        {"_id": "shared"},
        {
            "$push": {
                "messages": {
                    "$each": [{"role": role, "content": content}],
                    "$slice": -CW
                }
            }
        },
        upsert=True
    )

@bot.tree.command(name="ask", description="ask me a question", guild=guild)
@discord.app_commands.describe(prompt="your prompt")
async def ask(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()

    save_message("user", prompt)
    history = get_history()

    try:
        response = agent.beta.conversations.start(
            agent_id=getenv("AGENT_ID"), 
            inputs=history
        )

        reply = response.outputs[0].content
        save_message("assistant", reply)
        
        await interaction.followup.send(f"{prompt}: ")
        await interaction.followup.send(reply)
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")