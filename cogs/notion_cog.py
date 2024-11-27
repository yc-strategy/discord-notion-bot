import os
import requests
import discord
from discord import app_commands

class NotionCog(app_commands.Group):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.query_api_key = os.getenv("NOTION_QUERY_API_KEY")
        self.write_api_key = os.getenv("NOTION_WRITE_API_KEY")
        self.database_id = "14aa21e2ec2280cc8766f22405b7a07e"

    def get_stocks_from_notion(self):
        headers = {
            "Authorization": f"Bearer {self.query_api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        url = f"https://api.notion.com/v1/databases/{self.database_id}/query"
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            return response.json()['results']
        return None

    def format_stock_list(self, stocks):
        message = "Available stocks:\n"
        for stock in stocks:
            name = stock['properties']['Name']['title'][0]['text']['content']
            message += f"- {name}\n"
        return message

    def get_page_id_by_name(self, stock_name):
        stocks = self.get_stocks_from_notion()
        if not stocks:
            return None
        for stock in stocks:
            name = stock['properties']['Name']['title'][0]['text']['content']
            if name == stock_name:
                return stock['id']
        return None

    def update_stock_prices(self, page_id, prices):
        headers = {
            "Authorization": f"Bearer {self.write_api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        data = {
            "properties": {
                "High Price": {"number": prices['high']},
                "Low Price": {"number": prices['low']},
                "Open Price": {"number": prices['open']},
                "Close Price": {"number": prices['close']}
            }
        }
        url = f"https://api.notion.com/v1/pages/{page_id}"
        response = requests.patch(url, headers=headers, json=data)
        return response.status_code == 200

    @app_commands.command(name="notionlist", description="Lists stocks from Notion database")
    async def notionlist_command(self, interaction: discord.Interaction):
        await interaction.response.defer()
        stocks = self.get_stocks_from_notion()
        if not stocks:
            await interaction.followup.send("Failed to fetch stocks from Notion")
            return
        message = self.format_stock_list(stocks)
        await interaction.followup.send(message)

    @app_commands.command(name="addentry", description="Adds a new entry for a stock")
    async def addentry_command(self, interaction: discord.Interaction, stock_name: str, open_price: float, high_price: float, low_price: float, close_price: float):
        await interaction.response.defer()
        page_id = self.get_page_id_by_name(stock_name)
        if not page_id:
            await interaction.followup.send(f"Stock '{stock_name}' not found in database.")
            return
        prices = {
            'high': high_price,
            'low': low_price,
            'open': open_price,
            'close': close_price
        }
        success = self.update_stock_prices(page_id, prices)
        if success:
            await interaction.followup.send(f"Successfully updated prices for {stock_name}")
        else:
            await interaction.followup.send(f"Failed to update prices for {stock_name}")