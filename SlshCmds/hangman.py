import discord
from aiohttp import ClientSession
from os import getenv
from variables import bot, guild

@bot.tree.command(name="hangman", description="torment a man who is hanged", guild=guild)
async def hm(interaction: discord.Interaction):
    word = ""

    url = "https://api.api-ninjas.com/v2/randomword"

    headers = { "X-API-Key": getenv("NINJA_KEY") }

    async with ClientSession(headers=headers) as session:
        async with session.get(url) as r:
            data = await r.json()
            word = str(data[0])

    def check(msg: discord.Message):
        return msg.author == interaction.user and msg.channel == interaction.channel
    def out(left: set[str]):
        result = []

        for ch in word:
            if ch in left:
                result.append(ch)
            else:
                result.append("\\_")
        
        return "# " + "".join(result)
    def hang(lives: int):
        lines = [
            "\u200b \\_\\_",
            "/  \\",
            "|   ",
            "|  ",
            "\\-  "
        ]

        # head
        if lives < 6:
            lines[2] += "O"

        # middle
        torso = ""

        if lives < 5:
            torso = "  |"
        
        if lives < 4:
            torso = "-" + torso.strip()
        
        if lives < 3:
            torso += "-"

        lines[3] += torso

        # legs
        if lives < 2:
            lines[4] += "/"
        
        if lives < 1:
            lines[4] += "\\"

        return "\n".join(lines)

    lives = 6
    left = set(word)
    done = set()
    await interaction.response.send_message(f"{hang(lives)}\n# {"\\_" * len(word)}")

    while True:
        try:
            msg = await bot.wait_for("message", timeout=3600, check=check)
            guess = msg.content.strip().lower()

            if guess == "exit!":
                return
            
            if len(guess) != 1:
                await msg.reply("Enter only 1 letter")
                continue
            elif guess in done:
                await msg.reply("You already tried this letter")
                continue
            
            if guess in left:
                left.remove(guess)
            else:
                lives -= 1

            done.add(guess)
            response = out(done)

            await msg.reply(hang(lives))
            await interaction.channel.send(response)

            if not left:
                await msg.reply("You **win**!")
                return
            
            if lives <= 0:
                await msg.reply(f"You lose, word was **{word}**")
                return
        except TimeoutError:
            await interaction.channel.send(f"{interaction.user.mention}\nTook too long to give letter, session terminated")
            return

