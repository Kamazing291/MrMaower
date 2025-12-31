from os import getenv
from re import fullmatch
from aiohttp import ClientSession
from discord.ext import commands
from variables import bot, owner, client

@bot.command()
async def word(ctx: commands.Context, word: str, *, hint: str | None = None):
    if ctx.author.id != owner:
        return
    
    async def isWord(string: str):
        if fullmatch(r"[a-z]+", string) is None:
            return False

        url = f"{getenv("DICT")}{string}"

        async with ClientSession() as session:
            async with session.get(url) as r:
                if r.status == 200:
                    return True
                if r.status == 404:
                    return False
                
                return True
    try:
        await ctx.message.delete()
    except Exception:
        pass

    word = word.strip().lower()
    if not await isWord(word):
        await ctx.reply("Not valid word", ephemeral=True)
        return
    
    collection = client["main"]["wordle"]
    collection.update_one({}, {
        "$set": {
            "done": False,
            "word": word,
            "plays": []
        }
    })


    ann = await bot.fetch_channel(int(getenv("ANNOUNCE")))
    if hint is None:
        await ann.send(f"<@&{int(getenv("WORDLE"))}>\nToday's word is set. It is a {len(word)} letter word\ngl")
    else:
        await ann.send(f"<@&{int(getenv("WORDLE"))}>\nToday's word is set. Hint is ||{hint}||. It is a {len(word)} letter word\ngl")