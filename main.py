import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from cogs.notion_cog import AddStockCog, AddEntryCog, ListStockCog, FibonacciCog
from cogs.notion_cog.notion_api import NotionAPI

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = "14aa21e2ec2280cc8766f22405b7a07e"

class StockBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="/", intents=intents)
        self.notion_api = NotionAPI(NOTION_TOKEN, DATABASE_ID)

    async def setup_hook(self):
        # Add all cogs
        await self.add_cog(AddStockCog(self))
        await self.add_cog(AddEntryCog(self))
        await self.add_cog(ListStockCog(self))
        await self.add_cog(FibonacciCog(self))
        
        # Sync commands
        await self.tree.sync()

    async def on_ready(self):
        print(f'Logged in as {self.user}')

def main():
    bot = StockBot()
    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()
