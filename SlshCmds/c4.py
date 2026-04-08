from random import randint
import discord
from discord.ui import Button, View
from variables import bot, guild

ROWS, COLUMNS = 6, 7

@bot.tree.command(name="connect-4", description="play a game", guild=guild)
@discord.app_commands.describe(opponent="person")
async def connect(interaction: discord.Interaction, opponent: discord.Member):
    if interaction.user == opponent:
        await interaction.response.send_message("Stop playing with yourself")
        return
    
    if opponent.bot:
        await interaction.response.send_message("Lmao ts loser doesn't have friends")
        return
    
    turn = randint(0, 1)

    SYMBOLS = {
        "none": "⚫",
        "p1": "🔴",
        "p2": "🟡"
    }

    grid = [[SYMBOLS["none"] for _ in range(COLUMNS)] for _ in range(ROWS)]
    depths = [ROWS - 1 for _ in range(COLUMNS)]

    buttons = [Button(label=str(i + 1), style=discord.ButtonStyle.primary, custom_id=f"s{i}") for i in range(COLUMNS)]

    p1 = interaction.user if turn == 0 else opponent
    p2 = interaction.user if turn == 1 else opponent
    cp = p1

    view = View(timeout=600)
    for i in buttons:
        view.add_item(i)

    def out():
        result = []

        for row in grid:
            result.append(" ".join(row))

        return "\n".join(result)
    
    def check_win(symbol: str):
        # horizontal
        for r in range(ROWS):
            for c in range(COLUMNS - 3):
                if all(grid[r][c+i] == symbol for i in range(4)):
                    return True
        
        # vertical
        for r in range(ROWS - 3):
            for c in range(COLUMNS):
                if all(grid[r+i][c] == symbol for i in range(4)):
                    return True
                
        # diagonal - down right
        for r in range(ROWS - 3):
            for c in range(COLUMNS - 3):
                if all(grid[r+i][c+i] == symbol for i in range(4)):
                    return True
        
        # diagonal - down left
        for r in range(ROWS - 3):
            for c in range(3, COLUMNS):
                if all(grid[r+i][c-i] == symbol for i in range(4)):
                    return True
        
        return False
    
    async def callback(interaction2: discord.Interaction):
        nonlocal cp, buttons

        if interaction2.user != cp:
            await interaction2.response.send_message("This button is not for you!", ephemeral=True)
            return
        
        choice = int(interaction2.data["custom_id"][1])

        depth = depths[choice]

        if depths[choice] < 0:
            await interaction2.response.send_message("Column full", ephemeral=True)
            return
        
        grid[depth][choice] = SYMBOLS["p1"] if cp is p1 else SYMBOLS["p2"]
        depths[choice] -= 1

        if depth <= 0:
            buttons[choice].disabled = True
        
        if check_win(SYMBOLS["p1"] if cp is p1 else SYMBOLS["p2"]):
            for button in buttons:
                button.disabled = True
            await interaction2.response.edit_message(content=f"{cp.mention} WINS!\n{out()}", view=view)
            return
        if all(d < 0 for d in depths):
            await interaction2.response.edit_message(content=f"DRAW\n{out()}", view=view)
            return

        cp = p1 if cp is p2 else p2

        await interaction2.response.edit_message(content=f"Choose {cp.mention}:\n{out()}", view=view)
    
    for i in buttons:
        i.callback = callback

    await interaction.response.send_message(f"Choose {cp.mention}:\n{out()}", view=view)
