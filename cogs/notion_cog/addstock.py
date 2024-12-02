import discord
from discord import app_commands
from discord.ext import commands

class AddStockCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.notion_api = bot.notion_api

    @app_commands.command(name="addstock", description="Adds a new stock to the database")
    @app_commands.describe(stock_name="Name of the stock to add")
    async def addstock(self, interaction: discord.Interaction, stock_name: str):
        await interaction.response.defer()
        
        if self.notion_api.get_page_id_by_name(stock_name):
            await interaction.followup.send(f"Stock '{stock_name}' already exists in database.")
            return
            
        success = self.notion_api.add_stock(stock_name)
        
        if success:
            await interaction.followup.send(f"Successfully added stock '{stock_name}' to database")
        else:
            await interaction.followup.send(f"Failed to add stock '{stock_name}'.")
