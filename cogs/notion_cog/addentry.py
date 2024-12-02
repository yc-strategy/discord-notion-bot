import discord
from discord import app_commands
from discord.ext import commands

class AddEntryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.notion_api = bot.notion_api

    @app_commands.command(name="addentry", description="Adds a new entry for a stock")
    @app_commands.describe(
        stock_name="Name of the stock",
        open_price="Open price",
        high_price="High price",
        low_price="Low price",
        close_price="Close price"
    )
    async def addentry(
        self,
        interaction: discord.Interaction,
        stock_name: str,
        open_price: float,
        high_price: float,
        low_price: float,
        close_price: float
    ):
        await interaction.response.defer()
        
        page_id = self.notion_api.get_page_id_by_name(stock_name)
        if not page_id:
            await interaction.followup.send(f"Stock '{stock_name}' not found in database.")
            return
            
        prices = {
            'open': open_price,
            'high': high_price,
            'low': low_price,
            'close': close_price
        }
        
        success = self.notion_api.update_stock_prices(page_id, prices)
        if success:
            await interaction.followup.send(f"Successfully updated prices for {stock_name}")
        else:
            await interaction.followup.send(f"Failed to update prices for {stock_name}")
