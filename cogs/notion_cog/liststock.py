import discord
from discord import app_commands
from discord.ext import commands

class ListStockCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.notion_api = bot.notion_api

    def build_table(self, headers, rows):
        # Determine the width of each column
        columns = list(zip(*([headers] + rows)))
        col_widths = [max(len(str(val)) for val in col) for col in columns]

        # Build the format string
        format_str = ' | '.join('{{:{}}}'.format(width) for width in col_widths)
        separator = '-+-'.join('-' * width for width in col_widths)

        # Build the table
        lines = [
            format_str.format(*headers),
            separator
        ]
        for row in rows:
            lines.append(format_str.format(*row))
        return '\n'.join(lines)

    def format_stock_list(self, stocks):
        # Build table data
        table_data = []
        for item in stocks:
            name = item['properties']['Name']['title'][0]['text']['content']
            open_price = item['properties']['Open Price']['number']
            high_price = item['properties']['High Price']['number']
            low_price = item['properties']['Low Price']['number']
            close_price = item['properties']['Close Price']['number']
            
            table_data.append([
                name,
                open_price if open_price is not None else 'N/A',
                high_price if high_price is not None else 'N/A',
                low_price if low_price is not None else 'N/A',
                close_price if close_price is not None else 'N/A'
            ])
            
        # Create headers for the table
        headers = ['Symbol', 'Open', 'High', 'Low', 'Close']
        # Build the table as a string
        table_str = self.build_table(headers, table_data)
        return table_str

    @app_commands.command(name="notionlist", description="Lists stocks from Notion database")
    async def notionlist(self, interaction: discord.Interaction):
        await interaction.response.defer()
        
        stocks = self.notion_api.get_stocks()
        if not stocks:
            await interaction.followup.send("Failed to fetch stocks from Notion")
            return
            
        message = self.format_stock_list(stocks)
        await interaction.followup.send(f"```\n{message}\n```")