import asyncio
import discord
from discord.ext import commands
import os
import io

import importlib
import analysis
import response

from pathlib import Path
wordsfolder = ["words/" + f.name for f in Path("words").iterdir() if f.is_file()]

class Bot(discord.Client):
    def __init__(self) -> None:
        super().__init__(intents=discord.Intents.none())
        self.tree = discord.app_commands.CommandTree(self)
        self.words = response.getWords(wordsfolder)
    async def setup_hook(self) -> None:
        synced = await self.tree.sync()
        print(f"synced {len(synced)}: {[c.name for c in synced]}")
        print(f"app id: {self.application_id}")
        self.loop.create_task(reload_loop())

bot = Bot()



@bot.tree.context_menu(name="analyze")
@discord.app_commands.allowed_installs(guilds=True, users=True)
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def analyze(interaction: discord.Interaction, message: discord.Message) -> None:
    """Front end for the analyzets function"""
    text = message.content
    if not text:
        await interaction.response.send_message("No text in that message.",
                                                ephemeral=True)
        return
    await interaction.response.defer(thinking=True)
    result: str = await (analysis.analyzets(text, message.jump_url))
    await interaction.followup.send(result[:2000])

@bot.tree.context_menu(name="respond")
@discord.app_commands.allowed_installs(guilds=True, users=True)
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def respond(interaction: discord.Interaction, message: discord.Message) -> None:
    """Front end for the respondtots function"""
    text = message.content
    if not text:
        await interaction.response.send_message("No text in that message.",
                                                ephemeral=True)
        return
    await interaction.response.defer(thinking=True)
    result: str = await (response.respondtots(text, message.jump_url, bot.words))
    if(not result.strip()):
        result = "I have nothing to say here. Your hambug bores me."
    await interaction.followup.send(result[:2000])



async def reload_loop() -> None:
    """Runs a continuous loop that allows the user
    to refresh the function in analysis.py by pressing 'r'"""
    while True:
        line = await asyncio.to_thread(input)
        if line.strip() == "r":
            importlib.reload(analysis)
            importlib.reload(response)
            print("reloaded")
            bot.words = response.getWords(wordsfolder)

@bot.event
async def on_ready() -> None:
    """Function ran on startup"""
    print(f"Logged in as {bot.user}")


bot.run(os.getenv("DISCORD_TOKEN", ""))




