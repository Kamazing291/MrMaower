from importlib import import_module
from os import listdir, getenv

from variables import bot, guild
from wake_ping import ping

if __name__ == "__main__":
    for folder in ["MsgCmds", "SlshCmds"]:
        for file in listdir(f"./{folder}"):
            if file.endswith(".py"):
                module = f"{folder}.{file[:-3]}"
                import_module(module)

@bot.event
async def on_ready():
    await bot.tree.sync(guild=guild)
    print(f"{bot.user.display_name} has connected")

ping()

bot.run(getenv("TOKEN"))