import random
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from config.base_cogs import BaseCog
from models.gacha import GachaResult
from repositories.character_repository import (
    get_character_by_player_id,
    update_character,
)
from repositories.gacha_repository import get_gacha_config
from repositories.user_repository import get_or_create_user, increment_gacha_count
from services.arcana_service import (
    add_arcana_skill,
    create_arcana_data,
    pick_skill_with_probability,
)


class GachaCog(BaseCog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(bot)
        self.config = get_gacha_config()

        game_data = self.bot.game_data
        arcana_list = game_data.arcana
        arcana_skills_list = game_data.arcana_skills
        arcana_tiers_list = game_data.arcana_tiers

        # Build all arcana data via the service
        arcana_data = create_arcana_data(
            arcana_list=arcana_list,
            arcana_skills_list=arcana_skills_list,
            arcana_tiers_list=arcana_tiers_list,
        )

        # Now, store these references as instance variables
        self.arcana_name_map = arcana_data["arcana_name_map"]
        self.skill_details_map = arcana_data["skill_details_map"]
        self.tier_config = arcana_data["tier_config"]
        self.arcana_skills = arcana_data["arcana_skills"]
        self.sorted_tiers = arcana_data["sorted_tiers"]

    def create_embed(self, skill: GachaResult, arcana_name: str) -> discord.Embed:
        arcana = self.arcana_name_map.get(arcana_name.lower())
        if not arcana:
            raise ValueError(f"Arcana '{arcana_name}' not found")

        skill_details = self.skill_details_map.get(skill.name)
        tier_color = self.tier_config[skill.tier_level]["color"]
        tier_name = self.tier_config[skill.tier_level]["name"]

        embed = discord.Embed(
            title=skill.name,
            description=(
                skill_details.description
                if skill_details
                else "Sem descrição disponível."
            ),
            color=tier_color,
        )
        embed.add_field(name="Tier", value=tier_name, inline=True)
        embed.add_field(name="Chance", value=f"{skill.chance * 100:.0f}%", inline=True)
        embed.set_footer(text=arcana.name, icon_url=arcana.icon_url)
        return embed

    @app_commands.command(name="gacha", description="Rola um feitiço elemental")
    @app_commands.describe(arcana="A arcana de magias que você quer rolar")
    @commands.guild_only()
    async def gacha(
        self,
        interaction: discord.Interaction,
        arcana: Optional[
            Literal[
                "Destruição",
                "Criação",
                "Fortificação",
                "Divinação",
                "Transformação",
                "Amarração",
                "Cura",
                "Transportação",
            ]
        ] = None,
    ):
        try:
            self.bot.logger.info(f"Executing 'gacha' command. Arcana: {arcana}")

            if not self.config.enabled:
                await interaction.response.send_message(
                    "Nossos mercadores ainda não estão prontos para vender novos cancioneiros neste momento. Aguarde mais um pouco!",
                    ephemeral=True,
                )
                return

            # If user didn't choose an arcana, pick a random one
            if arcana is None:
                chosen_arcana = random.choice(list(self.arcana_name_map.values()))
                arcana_name = chosen_arcana.name
            else:
                arcana_name = arcana

            # Use the refactored probability picker
            skill = pick_skill_with_probability(
                arcana_name,
                self.arcana_name_map,
                self.arcana_skills,
                self.sorted_tiers,
                GachaResult,
            )

            if skill is None:
                self.bot.logger.info("No skill found. Informing the user.")
                await interaction.response.send_message(
                    "Nenhum item encontrado. Tente novamente."
                )
                return

            # Build the embed
            skill_embed = self.create_embed(skill, arcana_name)

            # Example: increment user’s gacha count
            increment_gacha_count(interaction.user.id)

            # If you track arcs for a character:
            user = get_or_create_user(interaction.user.id)
            character = get_character_by_player_id(user.id)
            if character:
                self.bot.logger.info(
                    f"Adding skill {skill.skill_id} to user {interaction.user.id}"
                )
                new_arcana_skills = add_arcana_skill(
                    character.arcana_skills, skill.skill_id - 1
                )
                character.arcana_skills = new_arcana_skills
                update_character(character)

            await interaction.response.send_message(embed=skill_embed)
            self.bot.logger.info(f"Successfully sent skill: {skill}")

        except Exception as e:
            self.bot.logger.error(f"Error in 'gacha' command: {e}", exc_info=True)
            await interaction.response.send_message(
                "Ocorreu um erro ao executar o comando gacha. Por favor, tente novamente mais tarde."
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(GachaCog(bot))
