import discord
from discord import app_commands
from xapi import XAPI
import os

class ElonMonitorCog(app_commands.Group):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.x_api = XAPI(XAPIConfig())

    @app_commands.command(
        name="listen_elonmusk",
        description="开始在此频道监控马斯克的推文（每5小时更新一次）"
    )
    async def listen_elonmusk_command(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            channel_id = interaction.channel_id
            if channel_id in self.bot.elon_monitor_channels:
                await interaction.followup.send("此频道已在监控马斯克的推文！")
                return
            self.bot.elon_monitor_channels.add(channel_id)
            # Code to send initial summary
            await interaction.followup.send("✅ 成功开始在此频道监控马斯克的推文。更新将每5小时发送一次。")
        except Exception as e:
            print(f"Error in listen_elonmusk command: {e}")
            await interaction.followup.send("抱歉，设置监控时发生错误。")

    @app_commands.command(
        name="stoplistening",
        description="停止在此频道监控马斯克的推文"
    )
    async def stop_listening_command(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            channel_id = interaction.channel_id
            if channel_id not in self.bot.elon_monitor_channels:
                await interaction.followup.send("此频道当前未在监控马斯克的推文！")
                return
            self.bot.elon_monitor_channels.remove(channel_id)
            await interaction.followup.send("✅ 成功停止在此频道监控马斯克的推文。")
        except Exception as e:
            print(f"Error in stop_listening command: {e}")
            await interaction.followup.send("抱歉，停止监控时发生错误。")

    @app_commands.command(
        name="checkmonitors",
        description="查看哪些频道正在监控马斯克的推文"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def check_monitors_command(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            if not self.bot.elon_monitor_channels:
                await interaction.followup.send("当前没有频道在监控马斯克的推文。")
                return
            monitored_channels = []
            for channel_id in self.bot.elon_monitor_channels:
                channel = self.bot.get_channel(channel_id)
                if channel:
                    monitored_channels.append(f"#{channel.name} ({channel_id})")
            message = "**当前监控的频道：**\n" + "\n".join(monitored_channels)
            await interaction.followup.send(message)
        except Exception as e:
            print(f"Error in check_monitors command: {e}")
            await interaction.followup.send("抱歉，检查监控时发生错误。")