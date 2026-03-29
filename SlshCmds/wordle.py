from os import getenv
from re import fullmatch
from aiohttp import ClientSession
import discord
from variables import bot, guild, client, owner

@bot.tree.command(name="wordle", description="daily wordle", guild=guild)
async def wordle(interaction: discord.Interaction):
    collection = client["main"]["wordle"]
    doc = collection.find_one()

    if not interaction.user.nick:
        await interaction.response.send_message("You can't play wordle now")
        return
    if interaction.user.display_name in doc["plays"]:
        await interaction.response.send_message("You've played today")
        return
    
    word = doc["word"]
    
    collection.update_one({}, {"$push": {"plays": interaction.user.display_name}})

    length = len(word)
    lives = 6

    await interaction.response.send_message(f"Enter a {length} letter word (lives = {lives}):")
    if doc["done"]:
        await interaction.followup.send(f"PS: {doc["win"]} has already gotten today's word")

    def check(msg: discord.Message):
        return msg.author == interaction.user and msg.channel == interaction.channel
    symbols = {"black": "⬛", "yellow": "🟨", "green": "🟩"}
    def out(s: str):
        n = len(word)
        result = [symbols["black"]] * n

        remaining = {}

        for i in range(n):
            if s[i] == word[i]:
                result[i] = symbols["green"]
            else:
                remaining[word[i]] = remaining.get(word[i], 0) + 1
        
        for i in range(n):
            if result[i] == symbols["green"]:
                continue
            ch = s[i]
            if remaining.get(ch, 0) > 0:
                result[i] = symbols["yellow"]
                remaining[ch] -= 1
        
        return " ".join(result)
    async def isWord(word: str):
        if fullmatch(r"[a-z]+", word) is None:
            return False

        url = f"{getenv("DICT")}{guess}"

        async with ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    return True
                if r.status == 404:
                    return False
                
                return True
    
    while True:
        try:
            msg = await bot.wait_for("message", timeout=3600, check=check)
            guess = msg.content.strip().lower()

            if guess == "exit!":
                return
            
            if len(guess) != length:
                await msg.reply(f"Give a {length} letter word")
                continue
            elif not await isWord(guess):
                await msg.reply("Give a valid english word")
                continue

            response = out(guess)
            
            lives -= 1
            await msg.reply(response)
            await interaction.channel.send(f"lives left = {lives}")
            if guess == word:
                doc = collection.find_one()
                if doc["done"]:
                    await msg.reply(f"You win, but {doc["win"]} has won before you")
                    return

                await msg.reply("You win!")
                streak = doc["streak"]+1 if interaction.user.id != owner else 0
                collection.update_one({}, {
                    "$set": {
                        "done": True,
                        "win": interaction.user.display_name,
                        "streak": streak
                    }
                })
                general = await bot.fetch_channel(int(getenv("GENERAL")))

                if interaction.user.id == owner:
                    await general.send(f"# Wordle of the Day\n<@&{int(getenv("WORDLE"))}> has lost its {doc["streak"]} day streak. Today's wordle was **{word}**, shame on you.")
                else:
                    await general.send(f"# Wordle of the Day\n<@&{int(getenv("WORDLE"))}> is on a **{streak}** day streak. Today's wordle (**{word}**) has been beaten by {interaction.user.mention}.")

                return
            if lives <= 0:
                if not doc["done"]:
                    await msg.reply("You lose, wait for someone else to find out the word")
                else:
                    await msg.reply(f"You lose, word was \"{word}\"")
                return
        except TimeoutError:
            await interaction.channel.send(f"{interaction.user.mention}\nTook too long to give guess, you can't play wordle until word is updated")
            return