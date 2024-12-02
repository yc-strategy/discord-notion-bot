import discord
from discord import app_commands
from discord.ext import commands

class FibonacciCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.notion_api = bot.notion_api

    def calculate_fibonacci_retracement(self, high, low):
        diff = high - low
        fib_levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]
        levels = {}
        
        for level in fib_levels:
            price = high - (diff * level)
            levels[f'{level*100:.1f}%'] = price
            
        return levels

    def get_stock_prices(self, stock_name):
        stocks = self.notion_api.get_stocks()
        if not stocks:
            return None
        for stock in stocks:
            name = stock['properties']['Name']['title'][0]['text']['content']
            if name == stock_name:
                return {
                    'open': stock['properties']['Open Price']['number'],
                    'high': stock['properties']['High Price']['number'],
                    'low': stock['properties']['Low Price']['number'],
                    'close': stock['properties']['Close Price']['number']
                }
        return None

    @app_commands.command(name="showretracement", description="Shows Fibonacci retracement levels for a stock")
    @app_commands.describe(stock_name="Name of the stock to calculate Fibonacci retracement levels for")
    async def showretracement(self, interaction: discord.Interaction, stock_name: str):
        await interaction.response.defer()
        
        prices = self.get_stock_prices(stock_name)
        if not prices:
            await interaction.followup.send(f"Stock '{stock_name}' not found in database.")
            return
            
        # Check if any price is missing
        missing_prices = []
        for price_type, value in prices.items():
            if value is None:
                missing_prices.append(price_type)
                
        if missing_prices:
            missing_str = ', '.join(missing_prices)
            await interaction.followup.send(
                f"Cannot calculate Fibonacci retracement levels. Missing prices for '{stock_name}': {missing_str}"
            )
            return
            
        fib_levels = self.calculate_fibonacci_retracement(prices['high'], prices['low'])
        
        message = f"Fibonacci Retracement Levels for {stock_name} (fetched from Notion database):\n\n"
        message += f"High: {prices['high']:.2f}\n"
        message += f"Low: {prices['low']:.2f}\n"
        message += f"Open: {prices['open']:.2f}\n"
        message += f"Close: {prices['close']:.2f}\n\n"
        message += "Fibonacci Levels:\n"
        message += "-----------------\n"
        
        for level, price in fib_levels.items():
            message += f"{level}: {price:.2f}\n"
            
        await interaction.followup.send(f"```\n{message}\n```")