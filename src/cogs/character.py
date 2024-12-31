from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from config.base_cogs import PlayerCog
from repositories.character_repository import (
    get_character_by_player_id,
)
from repositories.user_repository import get_or_create_user
from views.character import CharacterView


class CharacterCog(PlayerCog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(bot)
        self.arcana_skills = self.bot.game_data.arcana_skills

    @app_commands.command(
        name="ficha", description="Mostra a ficha do seu personagem ativo."
    )
    async def player(
        self,
        interaction: discord.Interaction,
        pagina: Optional[
            Literal["info", "attributes", "story", "arcana_skills"]
        ] = None,
        mostrar: bool = False,
    ):
        user = get_or_create_user(interaction.user.id)
        character = get_character_by_player_id(user.id)
        view = CharacterView(
            character, self.arcana_skills, interaction.user, page=pagina
        )

        initial_embeds = view.get_embeds_for_option(view.current_option)

        await interaction.response.send_message(
            embeds=initial_embeds, view=view, ephemeral=not mostrar
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(CharacterCog(bot))
