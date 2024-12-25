import discord
import os
from discord import app_commands
from discord.ext import commands
import random
from services.user_service import get_or_create_user


class AdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    def get_filtered_cogs(self, current: str = None):
        cogs_dir = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "..", "cogs")
        )
        cogs = [
            f[:-3]
            for f in os.listdir(cogs_dir)
            if f.endswith(".py") and f != "__init__.py"
        ]
        if current:
            filtered_cogs = [cog for cog in cogs if cog.startswith(current)]
        else:
            filtered_cogs = cogs
        return filtered_cogs

    async def extension_name_autocomplete(
        self, interaction: discord.Interaction, current: str
    ):
        filtered_cogs = self.get_filtered_cogs(current)
        return [app_commands.Choice(name=cog, value=cog) for cog in filtered_cogs[:25]]

    @commands.is_owner()
    @commands.guild_only()
    @app_commands.command(name="reload", description="Reload a cog and sync commands")
    @app_commands.autocomplete(extension_name=extension_name_autocomplete)
    async def reload_cog(
        self,
        interaction: discord.Interaction,
        extension_name: str = None,
        sync: bool = False,
    ):
        """
        Reload a cog and sync commands.
        """
        # Immediately defer to avoid timeout
        await interaction.response.defer(thinking=True)

        try:
            if not extension_name:
                for cog in self.get_filtered_cogs():
                    self.bot.logger.info(f"Reloading extension: {cog}")
                    await self.bot.reload_extension(f"cogs.{cog}")
            else:
                full_ext_name = f"cogs.{extension_name}"
                self.bot.logger.info(
                    f"Attempting to reload extension: {extension_name}"
                )
                await self.bot.reload_extension(full_ext_name)

            if sync:
                guild_id = os.getenv("DISCORD_GUILD_ID")
                if not guild_id:
                    raise ValueError("DISCORD_GUILD_ID not set in environment.")
                guild_obj = discord.Object(id=guild_id)
                self.bot.logger.debug("Syncing command tree...")
                synced = await self.bot.tree.sync(guild=guild_obj)
                self.bot.logger.debug(f"Synced {len(synced)} commands.")

            # Send final follow-up message
            await interaction.followup.send(
                f"Reloaded extension: {extension_name if extension_name else 'all'}{' and synced commands.' if sync else '.'}",
                ephemeral=True,
            )
            self.bot.logger.info(
                f"Successfully reloaded {extension_name if extension_name else 'all'} {'and synced commands.' if sync else '.'}"
            )
        except Exception as e:
            self.bot.logger.error(
                f"Failed to reload extension {extension_name if extension_name else 'all'}: {str(e)}",
                exc_info=True,
            )
            # Send an error follow-up
            await interaction.followup.send(
                f"Error reloading extension {extension_name if extension_name else 'all'}: {e}",
                ephemeral=True,
            )

    @commands.is_owner()
    @commands.guild_only()
    @app_commands.command(
        name="turns",
        description="Generates an ordered list of turns for each player in a role",
    )
    async def turns(self, interaction: discord.Interaction, role: discord.Role):
        """
        Generates an ordered list of turns for each player in a role.
        """
        players = role.members
        self.bot.logger.info(
            f"Generating turns for role: {role.name} with {len(players)} players"
        )
        self.bot.logger.info(f"Players: {players}")
        if len(players) == 0:
            await interaction.response.send_message(
                "No players in the role.", ephemeral=True
            )
            return

        # Create the formatted turn list with markdown
        turn_list = ["# Ordem dos Turnos"]
        random.shuffle(players)
        turn_list.extend(
            [f"{i + 1}. {player.mention}" for i, player in enumerate(players)]
        )

        await interaction.response.send_message("\n".join(turn_list))

    @commands.is_owner()
    @commands.guild_only()
    @app_commands.command(name="register_user", description="Register a user")
    async def register_user(
        self, interaction: discord.Interaction, user: discord.Member
    ):
        get_or_create_user(user.id, user.display_name)
        await interaction.response.send_message(
            f"Registered user: {user.display_name}", ephemeral=True
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(AdminCog(bot))
