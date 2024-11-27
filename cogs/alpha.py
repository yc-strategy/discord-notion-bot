import discord
from discord import app_commands
from alphaplus import AlphaAPI

class AlphaCog(app_commands.Group):
    def __init__(self, alpha_api, bot):
        super().__init__()
        self.alpha_api = alpha_api
        self.bot = bot

    @app_commands.command(
        name="alpha",
        description="Get K-line data for a stock or crypto"
    )
    @app_commands.choices(asset_type=[
        discord.app_commands.Choice(name="Stock", value="stock"),
        discord.app_commands.Choice(name="Crypto", value="crypto")
    ])
    async def alpha_command(
        self,
        interaction: discord.Interaction,
        asset_type: str = "stock",
        symbol: str = "AAPL.US"  # Default symbol
    ):
        try:
            await interaction.response.defer()
            is_stock = asset_type == "stock"
            asset_name = "Stock" if is_stock else "Crypto"
            symbol = symbol.upper()
            if is_stock:
                kline_data = self.alpha_api.get_stock_kline_data(symbol=symbol)
            else:
                kline_data = self.alpha_api.get_kline_data(symbol=symbol)
            if kline_data and 'data' in kline_data and 'kline_list' in kline_data['data']:
                response = f"**K-line Data for {symbol} ({asset_name}):**\n"
                for kline in kline_data['data']['kline_list']:
                    response += f"\nHigh: {kline['high_price']}\n"
                    response += f"Low: {kline['low_price']}\n"
                    response += f"Open: {kline['open_price']}\n"
                    response += f"Close: {kline['close_price']}\n"
                await interaction.followup.send(response)
            else:
                await interaction.followup.send(f"Could not get data for {symbol}")
        except Exception as e:
            print(f"Error in alpha command: {str(e)}")
            await interaction.followup.send("Sorry, an error occurred while fetching the data.")