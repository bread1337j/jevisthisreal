import asyncio
import discord
from discord.ext import commands
import os

import importlib
import analysis

#anything but using more than one python file yo

class Bot(discord.Client):
    def __init__(self) -> None:
        super().__init__(intents=discord.Intents.none())
        self.tree = discord.app_commands.CommandTree(self)
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
    result: str = await (analysis.analyzets(text))
    await interaction.followup.send(result[:2000])

async def reload_loop() -> None:
    """Runs a continuous loop that allows the user
    to refresh the functions in analysis.py by pressing 'r'"""
    while True:
        line = await asyncio.to_thread(input)
        if line.strip() == "r":
            importlib.reload(analysis)
            print("reloaded")

@bot.event
async def on_ready() -> None:
    """Function ran on startup"""
    print(f"Logged in as {bot.user}")


bot.run(os.getenv("DISCORD_TOKEN", ""))




