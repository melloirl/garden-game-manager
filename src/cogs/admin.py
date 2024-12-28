import os
import random

import discord
from discord import app_commands
from discord.ext import commands

from repositories.arcana_repository import get_arcana_skills
from repositories.character_repository import (
    get_character_by_id,
    get_character_by_player_id,
    get_characters,
    update_character,
)
from repositories.user_repository import get_or_create_user
from services.arcana_service import add_arcana_skill, remove_arcana_skill
from services.character_service import (
    restore_character,
)


@commands.is_owner()
@commands.guild_only()
class AdminCog(commands.GroupCog, group_name="admin"):
    """
    A cog group for admin commands.
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.character_cache = {}
        self.skill_cache = {}

    def _get_filtered_cogs(self, current: str = None):
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
        filtered_cogs = self._get_filtered_cogs(current)
        return [app_commands.Choice(name=cog, value=cog) for cog in filtered_cogs[:25]]

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
                for cog in self._get_filtered_cogs():
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

    @app_commands.command(
        name="reset_character", description="Reset the character to its max hp and mp"
    )
    async def reset_character(
        self, interaction: discord.Interaction, user: discord.Member
    ):
        character_user = get_or_create_user(user.id)
        character = get_character_by_player_id(character_user.id)

        if character is None:
            await interaction.response.send_message(
                "Character not found", ephemeral=True
            )
            return

        restore_character(character)
        update_character(character)
        await interaction.response.send_message(
            f"Character {character.name} has been reset to its max hp and mp",
            ephemeral=True,
        )

    async def character_id_autocomplete(
        self, interaction: discord.Interaction, current: str
    ):
        # 1. If we've already computed results for this exact prefix, return them.
        if current in self.character_cache:
            return self.character_cache[current]

        # 2. Fetch all characters from your data source.
        characters = get_characters()

        # 3. Filter by the current prefix (case-insensitive).
        filtered_characters = [
            c for c in characters if current.lower() in c.name.lower()
        ]

        # 4. Convert the first 25 matching entries into app_commands.Choice objects.
        choices = [
            app_commands.Choice(name=c.name, value=c.id)
            for c in filtered_characters[:25]
        ]

        # 5. Store them in the cache so if the user re-enters the same prefix, we skip the DB call.
        self.character_cache[current] = choices
        return choices

    async def skill_id_autocomplete(
        self, interaction: discord.Interaction, current: str
    ):
        if current in self.skill_cache:
            return self.skill_cache[current]

        skills = get_arcana_skills()
        filtered_skills = [s for s in skills if current.lower() in s.name.lower()]
        choices = [
            app_commands.Choice(name=s.name, value=s.id) for s in filtered_skills[:25]
        ]

        self.skill_cache[current] = choices
        return choices

    @app_commands.command(
        name="add_arcana_skill", description="Add a skill to a character"
    )
    @app_commands.autocomplete(character=character_id_autocomplete)
    @app_commands.autocomplete(skill=skill_id_autocomplete)
    async def add_arcana_skill(
        self, interaction: discord.Interaction, character: int, skill: int
    ):
        character_obj = get_character_by_id(character)
        updated_arcana_skills = add_arcana_skill(character_obj.arcana_skills, skill - 1)
        character_obj.arcana_skills = updated_arcana_skills
        update_character(character_obj)
        await interaction.response.send_message(
            f"Skill {skill} added to character {character_obj.name}", ephemeral=True
        )

    @app_commands.command(
        name="remove_arcana_skill", description="Remove a skill from a character"
    )
    @app_commands.autocomplete(character=character_id_autocomplete)
    @app_commands.autocomplete(skill=skill_id_autocomplete)
    async def remove_arcana_skill(
        self, interaction: discord.Interaction, character: int, skill: int
    ):
        character_obj = get_character_by_id(character)
        self.bot.logger.info(f"Character arcana skills: {character_obj.arcana_skills}")
        updated_arcana_skills = remove_arcana_skill(
            character_obj.arcana_skills, skill - 1
        )
        self.bot.logger.info(f"Updated arcana skills: {updated_arcana_skills}")
        character_obj.arcana_skills = updated_arcana_skills
        update_character(character_obj)
        await interaction.response.send_message(
            f"Skill {skill} removed from character {character_obj.name}", ephemeral=True
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(AdminCog(bot))
