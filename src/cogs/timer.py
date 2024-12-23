import discord
from discord.ext import commands, tasks
from discord import app_commands

class ActivityTimer:
    def __init__(self):
        self._is_active = False

    def start(self):
        self._is_active = True

    def stop(self):
        self._is_active = False

    def is_active(self) -> bool:
        return self._is_active


class TimerCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.timer = ActivityTimer()
        self.user: discord.User | None = None
        self.channel: discord.abc.Messageable | None = None

        self._ping_loop.start()

    @tasks.loop(minutes=20)
    async def _ping_loop(self):
        if self.timer.is_active() and self.channel and self.user:
            await self.user.send(f"{self.user.mention}, passaram-se 20 minutos!")

    @_ping_loop.before_loop
    async def before_ping_loop(self):
        await self.bot.wait_until_ready()

    @app_commands.command(name="timer", description="Toggles a 20 minutes timer.")
    @app_commands.default_permissions(administrator=True)
    async def timer(self, interaction: discord.Interaction):
        """
        Toggling command for admins only. 
        If the timer is inactive, it starts sending messages periodically. 
        If it's active, it stops sending those messages.
        """

        if not self.timer.is_active():
            self.timer.start()

            self.user = interaction.user
            self.channel = interaction.channel

            await interaction.response.send_message(
                "Timer started! I'll ping this channel periodically.",
            )
        else:
            # Stop the timer
            self.timer.stop()
            self.user = None
            self.channel = None

            await interaction.response.send_message(
                "Timer stopped! No more messages will be sent."
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(TimerCog(bot))
