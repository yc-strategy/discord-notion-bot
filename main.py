import os
from dotenv import load_dotenv
import discord
import asyncio
from discord import app_commands
from cogs.alpha import AlphaCog
from cogs.elon_monitor import ElonMonitorCog
from notion_cog import NotionCog

# Load environment variables from .env file
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

class CustomClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.alpha_api = AlphaAPI()
        self.elon_monitor_channels = set()

    async def setup_hook(self):
        # Load cogs
        await self.tree.add_cog(NotionCog(self))
        await self.tree.add_cog(AlphaCog(self.alpha_api, self))
        await self.tree.add_cog(ElonMonitorCog(self))
        # Start background task
        self.bg_task = self.loop.create_task(self.background_task())

    async def background_task(self):
        await self.wait_until_ready()
        while not self.is_closed():
            if self.elon_monitor_channels:
                try:
                    # Code for background task
                    pass
                except Exception as e:
                    print(f"Error in background task: {e}")
            await asyncio.sleep(5 * 60 * 60)  # 5 hours in seconds

discord_client = CustomClient()

# Load the Discord API key from .env file
discord_token = os.getenv("DISCORD_TOKEN")

discord_client.run(discord_token)
