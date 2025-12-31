from random import choice
import discord
from discord import ButtonStyle
from discord.ui import Button, View
from variables import bot, guild

@bot.tree.command(name="rock-paper-scissors", description="play a game", guild=guild)
@discord.app_commands.describe(opponent="person")
async def rps(interaction: discord.Interaction, opponent: discord.Member):
    p1 = interaction.user
    p2 = opponent

    if p1 == p2:
        await interaction.response.send_message("Bro, you gotta stop playing with yourself")
        return
    
    async def member():
        rock = Button(label="🪨", style=ButtonStyle.primary, custom_id="rock")
        paper = Button(label="📜", style=ButtonStyle.primary, custom_id="paper")
        scissors = Button(label="✂️", style=ButtonStyle.primary, custom_id="scissors")

        view = View(timeout=60)
        view.add_item(rock)
        view.add_item(paper)
        view.add_item(scissors)

        async def callback_1(interaction: discord.Interaction):
            if interaction.user != p1:
                await interaction.response.send_message("This button is not for you!", ephemeral=True)
                return
            
            view.stop()

            p1_choice = interaction.data["custom_id"]

            rock = Button(label="🪨", style=ButtonStyle.primary, custom_id="rock")
            paper = Button(label="📜", style=ButtonStyle.primary, custom_id="paper")
            scissors = Button(label="✂️", style=ButtonStyle.primary, custom_id="scissors")

            view2 = View(timeout=60)
            view2.add_item(rock)
            view2.add_item(paper)
            view2.add_item(scissors)

            async def callback_2(interaction: discord.Interaction):
                if interaction.user != p2:
                    await interaction.response.send_message("This button is not for you!", ephemeral=True)
                    return
                
                view2.stop()

                p2_choice = interaction.data["custom_id"]

                dic = {"rock": "🪨", "paper": "📜", "scissors": "✂️"}
                
                if p1_choice == p2_choice:
                    await interaction.response.send_message(f"Both of you picked {dic[p1_choice]}. Hence DRAW")
                    return
                
                winner = 0
                loser = 0
                wc = ""
                lc = ""

                if (
                    (p1_choice == "rock" and p2_choice == "scissors")
                    or (p1_choice == "paper" and p2_choice == "rock")
                    or (p1_choice == "scissors" and p2_choice == "paper")
                ):
                    winner = p1
                    wc = p1_choice
                    loser = p2
                    lc = p2_choice
                else:
                    winner = p2
                    wc = p2_choice
                    loser = p1
                    lc = p1_choice
                
                await interaction.response.send_message(f"{winner.mention} wins with {dic[wc]} and {loser.mention} loses with {dic[lc]}")
                

            rock.callback = callback_2
            paper.callback = callback_2
            scissors.callback = callback_2

            await interaction.response.send_message(f"Choose {p2.mention}: ", view=view2)

        rock.callback = callback_1
        paper.callback = callback_1
        scissors.callback = callback_1

        await interaction.response.send_message(f"Choose {p1.mention}: ", view=view)
    async def dbot():
        rock = Button(label="🪨", style=ButtonStyle.primary, custom_id="rock")
        paper = Button(label="📜", style=ButtonStyle.primary, custom_id="paper")
        scissors = Button(label="✂️", style=ButtonStyle.primary, custom_id="scissors")

        view = View(timeout=60)
        view.add_item(rock)
        view.add_item(paper)
        view.add_item(scissors)

        async def callback(interaction: discord.Interaction):
            if interaction.user != p1:
                await interaction.response.send_message("This button is not for you!", ephemeral=True)
                return
            
            view.stop()

            p1_choice = interaction.data["custom_id"]
            p2_choice = choice(["rock", "paper", "scissors"])

            dic = {"rock": "🪨", "paper": "📜", "scissors": "✂️"}
                
            if p1_choice == p2_choice:
                await interaction.response.send_message(f"Both of us picked {dic[p1_choice]}. Hence DRAW")
                return
            
            wc = ""
            lc = ""

            if (
                (p1_choice == "rock" and p2_choice == "scissors")
                or (p1_choice == "paper" and p2_choice == "rock")
                or (p1_choice == "scissors" and p2_choice == "paper")
            ):
                wc = p1_choice
                lc = p2_choice
                await interaction.response.send_message(f"You win with {dic[wc]} and I lose with {dic[lc]}")
            else:
                wc = p2_choice
                lc = p1_choice
                await interaction.response.send_message(f"I win with {dic[wc]} and you lose with {dic[lc]}")

        rock.callback = callback
        paper.callback = callback
        scissors.callback = callback

        await interaction.response.send_message(f"Choose {p1.mention}: ", view=view)

    if opponent.bot and opponent != bot.user:
        await interaction.response.send_message("Bro, play with me")
        return
    if opponent == bot.user:
        await dbot()
        return
    await member()