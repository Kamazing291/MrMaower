import discord
from random import randint
from variables import bot, guild, client

@bot.tree.command(name="ship", description="check compatibility", guild=guild)
@discord.app_commands.describe(person_1="person 1", person_2="person 2")
async def ship(interaction: discord.Interaction, person_1: discord.Member, person_2: discord.Member):
    if person_1.display_name == person_2.display_name:
        await interaction.response.send_message("Umm, you can't do that")
        return
    
    if not person_1.nick and not person_1.bot:
        await interaction.response.send_message(f"{person_1.display_name}'s nickname needs to be set first")
        return
    if not person_2.nick and not person_2.bot:
        await interaction.response.send_message(f"{person_1.display_name}'s nickname needs to be set first")
        return

    compatibility = randint(0, 100)

    collection = client["main"]["ships"]

    query = {
        "$or": [
            {"user1": person_1.display_name, "user2": person_2.display_name},
            {"user1": person_2.display_name, "user2": person_1.display_name}
        ]
    }
    there = collection.find_one(query)

    if there:
        compatibility = there["compatibility"]
    else:
        collection.insert_one({
            "user1": person_1.display_name,
            "user2": person_2.display_name,
            "compatibility": compatibility
        })
    
    name1 = person_1.display_name
    name2 = person_2.display_name
    s_name = name1[0:3]+name2[-3:len(name2)] if name1 < name2 else name2[0:3]+name1[-3:len(name1)]
    
    await interaction.response.send_message(f"{name1} & {name2} are {compatibility}% compatible for each other. The ship is called {s_name}")