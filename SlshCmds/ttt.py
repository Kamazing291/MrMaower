from random import randint
import discord
from discord import ButtonStyle
from discord.ui import Button, View
from variables import bot, guild

@bot.tree.command(name="tic-tac-toe", description="play a game", guild=guild)
@discord.app_commands.describe(opponent="person")
async def ttt(interaction: discord.Interaction, opponent: discord.Member):
    if interaction.user == opponent :
        await interaction.response.send_message("Stop playing with yourself")
        return
    
    turn = randint(0, 1)

    SYMBOLS = {
        "none": "\u200b",
        "x": "❌",
        "o": "⭕"
    }
    WIN = [
        [0, 1, 2],  # First row
        [3, 4, 5],  # Second row
        [6, 7, 8],  # Third row
        [0, 3, 6],  # First column
        [1, 4, 7],  # Second column
        [2, 5, 8],  # Third column
        [0, 4, 8],  # Diagonal
        [2, 4, 6]   # Diagonal
    ]

    grid = [
        Button(label=SYMBOLS["none"], style=ButtonStyle.primary, row=0, custom_id="s1"),
        Button(label=SYMBOLS["none"], style=ButtonStyle.primary, row=0, custom_id="s2"),
        Button(label=SYMBOLS["none"], style=ButtonStyle.primary, row=0, custom_id="s3"),
        Button(label=SYMBOLS["none"], style=ButtonStyle.primary, row=1, custom_id="s4"),
        Button(label=SYMBOLS["none"], style=ButtonStyle.primary, row=1, custom_id="s5"),
        Button(label=SYMBOLS["none"], style=ButtonStyle.primary, row=1, custom_id="s6"),
        Button(label=SYMBOLS["none"], style=ButtonStyle.primary, row=2, custom_id="s7"),
        Button(label=SYMBOLS["none"], style=ButtonStyle.primary, row=2, custom_id="s8"),
        Button(label=SYMBOLS["none"], style=ButtonStyle.primary, row=2, custom_id="s9")
    ]

    async def member():
        p1 = interaction.user if turn == 0 else opponent
        p2 = interaction.user if turn == 1 else opponent
        cp = p1

        view = View(timeout=600)
        for i in grid:
            view.add_item(i)

        async def callback(interaction2: discord.Interaction):
            nonlocal cp, grid

            if interaction2.user != cp:
                await interaction2.response.send_message("This button is not for you!", ephemeral=True)
                return
            
            choice = int(interaction2.data["custom_id"][1]) - 1

            if cp == p1:
                if grid[choice].label != SYMBOLS["none"]:
                    await interaction2.response.send_message("Can't overwrite squares!", ephemeral=True)
                    return
                grid[choice].label = SYMBOLS["x"]
                grid[choice].disabled = True
                cp = p2
            elif cp == p2:
                if grid[choice].label != SYMBOLS["none"]:
                    await interaction2.response.send_message("Can't overwrite squares!", ephemeral=True)
                    return
                grid[choice].label = SYMBOLS["o"]
                grid[choice].disabled = True
                cp = p1

            for a, b, c in WIN:
                if grid[a].label == grid[b].label == grid[c].label and grid[a].label != SYMBOLS["none"]:
                    for btn in grid:
                        btn.disabled = True
                    await interaction2.response.edit_message(content=f"{grid[a].label}, {p1.mention if grid[a].label == SYMBOLS['x'] else p2.mention} WINS!", view=view)
                    return
            if all(i.label != SYMBOLS["none"] for i in grid):
                await interaction2.response.edit_message(content="DRAW", view=view)
                return
            
            await interaction2.response.edit_message(content=f"Choose {cp.mention}: ", view=view)

        for i in grid:
            i.callback = callback

        await interaction.response.send_message(f"Choose {cp.mention}: ", view=view)
    
    async def dbot():
        REVERSE = {value: key for key, value in SYMBOLS.items()}
        player = interaction.user
        p_symbol = "x" if turn == 0 else "o"
        b_symbol = "x" if turn == 1 else "o"

        def evaluate():
            return [REVERSE[button.label] for button in grid]
        def availability(board=None):
            if board is None:
                board = evaluate()

            return [i for i, v in enumerate(board) if v == "none"]
        
        def check_win(board, symbol: str):
            for win in WIN:
                if all(board[i] == symbol for i in win):
                    return True
            return False
        
        def next_win(board, symbol: str):
            for move in availability(board):
                board[move] = symbol
                if check_win(board, symbol):
                    board[move] = "none"
                    return move
                board[move] = "none"
            return None
        def fork(board, symbol):
            for move in availability(board):
                board[move] = symbol
                win_threats = 0
                for next_move in availability(board):
                    board[next_move] = symbol
                    if check_win(board, symbol):
                        win_threats += 1
                    board[next_move] = "none"
                board[move] = "none"
                if win_threats >= 2:
                    return move
            return None
        def opp_corner(board):
            corners = [(0, 8), (2, 6), (6, 2), (8, 0)]
            for c, oc in corners:
                if board[c] == p_symbol and board[oc] == "none":
                    return oc
            return None
        def emp_corner(board):
            for pos in [0, 2, 6, 8]:
                if board[pos] == "none":
                    return pos
            return None
        def emp_side(board):
            for pos in [1, 3, 5, 7]:
                if board[pos] == "none":
                    return pos
            return None
        
        def best_move():
            tgrid = evaluate()

            move = next_win(tgrid, b_symbol)
            if move != None:
                return move
            
            move = next_win(tgrid, p_symbol)
            if move != None:
                return move
            
            move = fork(tgrid, b_symbol)
            if move != None:
                return move
            
            ofork = fork(tgrid, p_symbol)
            if ofork != None:
                for move in availability():
                    cboard = evaluate()
                    cboard[move] = b_symbol
                    if next_win(cboard, b_symbol) != None:
                        return move
                return ofork
            
            if tgrid[4] == "none":
                return 4
            
            move = opp_corner(tgrid)
            if move != None:
                return move
            
            move = emp_corner(tgrid)
            if move != None:
                return move
            
            move = emp_side(tgrid)
            if move != None:
                return move
            
            return None

        view = View(timeout=600)
        for i in grid:
            view.add_item(i)
        
        async def callback(interaction2: discord.Interaction):
            nonlocal grid

            if interaction2.user != player:
                await interaction2.response.send_message("This button is not for you!", ephemeral=True)
                return
            
            choice = int(interaction2.data["custom_id"][1]) - 1
            if grid[choice].label != SYMBOLS["none"]:
                await interaction2.response.send_message("Can't overwrite squares!", ephemeral=True)
                return
            grid[choice].label = SYMBOLS[p_symbol]
            grid[choice].disabled = True

            if check_win(evaluate(), p_symbol):
                for btn in grid:
                    btn.disabled = True
                await interaction2.response.edit_message(content=f"{SYMBOLS[p_symbol]}, You WIN!", view=view)
                return
            
            move = best_move()
            if move == None:
                await interaction2.response.edit_message(content="DRAW", view=view)
                return
            
            grid[move].label = SYMBOLS[b_symbol]
            grid[move].disabled = True

            move = best_move()
            if move == None:
                await interaction2.response.edit_message(content="DRAW", view=view)
                return

            if check_win(evaluate(), b_symbol):
                for btn in grid:
                    btn.disabled = True
                await interaction2.response.edit_message(content=f"{SYMBOLS[b_symbol]}, I WIN!", view=view)
                return
            
            await interaction2.response.edit_message(content=f"Choose {player.mention}: ", view=view)
        
        for i in grid:
            i.callback = callback

        if b_symbol == "x":
            move = best_move()
            grid[move].label = SYMBOLS[b_symbol]
            grid[move].disabled = True
        
        await interaction.response.send_message(f"Choose {player.mention}: ", view=view)
            
    
    if opponent.bot and opponent != bot.user:
        await interaction.response.send_message("Bro, play with me")
        return
    if opponent == bot.user:
        await dbot()
        return
    await member()