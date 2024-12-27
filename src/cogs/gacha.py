import random
from typing import Dict, Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

from config.base_cogs import BaseCog
from models.arcana import Arcana, ArcanaSkill, ArcanaTier
from models.gacha import GachaResult
from repositories.character_repository import (
    get_character_by_player_id,
    update_character_arcana_skills,
)
from services.user_service import increment_gacha_count
from utils.arcana_bitfield import add_skill


class GachaCog(BaseCog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(bot)
        self.reload_config()
        self.arcana_name_map = {a.name.lower(): a for a in self.arcanas}
        self.skill_details_map = {s.name: s for s in self.skills}

    def reload_config(self):
        """Load configuration from database"""
        try:
            self.skills: list[ArcanaSkill] = self.bot.arcana_skills
            self.bot.logger.debug(f"Loaded {len(self.skills)} skills")

            self.tiers: list[ArcanaTier] = self.bot.arcana_tiers
            self.bot.logger.debug(f"Loaded {len(self.tiers)} tiers")

            self.arcanas: list[Arcana] = self.bot.arcanas
            self.bot.logger.debug(f"Loaded {len(self.arcanas)} arcanas")

            # Create a mapping of tier levels to their probabilities and colors
            self.tier_config: Dict[int, Dict] = {}
            for tier in self.tiers:
                self.tier_config[tier.tier_level] = {
                    "name": tier.tier_name,
                    "probability": tier.probability,
                    "color": int(tier.color, base=16),
                }

            # Organize skills by arcana and tier_level
            self.arcana_skills: Dict[int, Dict] = {}
            for arcana in self.arcanas:
                self.arcana_skills[arcana.id] = {
                    "name": arcana.name,
                    "icon_url": arcana.icon_url,
                    "skills_by_tier": {},
                }

            for skill in self.skills:
                try:
                    if skill.arcana_id in self.arcana_skills:
                        tier_level = skill.tier.tier_level
                        if (
                            tier_level
                            not in self.arcana_skills[skill.arcana_id]["skills_by_tier"]
                        ):
                            self.arcana_skills[skill.arcana_id]["skills_by_tier"][
                                tier_level
                            ] = []
                        self.arcana_skills[skill.arcana_id]["skills_by_tier"][
                            tier_level
                        ].append(skill)
                except Exception as e:
                    self.bot.logger.error(
                        f"Error processing skill {skill.name}: {str(e)}\n{type(e).__name__}: {str(e)}"
                    )
                    continue

            # Pre-sort tiers once during initialization
            self.sorted_tiers = sorted(self.tiers, key=lambda x: x.tier_level)

        except Exception as e:
            self.bot.logger.error(
                f"Error in reload_config: {str(e)}\n{type(e).__name__}: {str(e)}"
            )
            raise

    def pick_with_probability(self, arcana_name: str) -> Optional[GachaResult]:
        """Pick a random skill from a given arcana based on tier probability."""
        arcana = self.arcana_name_map.get(arcana_name.lower())
        if not arcana:
            return None

        # Get the arcana configuration
        arcana_config = self.arcana_skills[arcana.id]

        random_seed = random.random()
        cumulative_prob = 0.0

        # Sort tiers by tier_level
        sorted_tiers = sorted(self.tiers, key=lambda x: x.tier_level)

        for tier in sorted_tiers:
            cumulative_prob += tier.probability
            if (
                tier.tier_level in arcana_config["skills_by_tier"]
                and arcana_config["skills_by_tier"][tier.tier_level]
            ):
                if random_seed <= cumulative_prob:
                    chosen_skill: ArcanaSkill = random.choice(
                        arcana_config["skills_by_tier"][tier.tier_level]
                    )
                    return GachaResult(
                        name=chosen_skill.name,
                        tier_level=tier.tier_level,
                        tier_name=tier.tier_name,
                        chance=tier.probability,
                        skill_id=chosen_skill.id,
                    )

        return None

    def create_embed(self, skill: GachaResult, arcana_name: str) -> discord.Embed:
        arcana = next(
            (a for a in self.arcanas if a.name.lower() == arcana_name.lower()), None
        )
        if not arcana:
            raise ValueError(f"Arcana {arcana_name} not found")

        # O(1) skill-details lookup
        skill_details = self.skill_details_map.get(skill.name)

        tier_color = self.tier_config[skill.tier_level]["color"]
        tier_name = self.tier_config[skill.tier_level]["name"]

        embed = discord.Embed(
            title=skill.name,
            description=skill_details.description
            if skill_details
            else "Sem descrição disponível.",
            color=tier_color,
        )
        embed.add_field(name="Tier", value=tier_name, inline=True)
        embed.add_field(name="Chance", value=f"{skill.chance * 100:.0f}%", inline=True)
        embed.set_footer(text=arcana.name, icon_url=arcana.icon_url)
        return embed

    @app_commands.command(name="gacha", description="Rola um feitiço elementar")
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

            if arcana is None:
                # Pick a random arcana if none was provided
                chosen_arcana = random.choice(self.arcanas)
                self.bot.logger.info(f"Chosen arcana: {chosen_arcana.name}")
                skill = self.pick_with_probability(chosen_arcana.name)
                arcana_name = chosen_arcana.name
            else:
                skill = self.pick_with_probability(arcana)
                arcana_name = arcana

            if skill is None:
                self.bot.logger.info("No skill found. Informing the user.")
                await interaction.response.send_message(
                    "Nenhum item encontrado. Tente novamente."
                )
                return

            skill_embed = self.create_embed(skill, arcana_name)

            # Example: increment user’s gacha count
            increment_gacha_count(interaction.user.id)

            # If you have character logic:
            character = get_character_by_player_id(interaction.user.id)
            if character:
                self.bot.logger.info(
                    f"Adding skill {skill.skill_id} to user {interaction.user.id}"
                )
                self.bot.logger.info(
                    f"Character arcana skills: {character.arcana_skills}"
                )
                new_arcana_skills = add_skill(
                    character.arcana_skills, skill.skill_id - 1
                )
                self.bot.logger.info(f"New arcana skills: {new_arcana_skills}")
                update_character_arcana_skills(character.id, new_arcana_skills)

            await interaction.response.send_message(embed=skill_embed)
            self.bot.logger.info(f"Successfully sent skill: {skill}")

        except Exception as e:
            self.bot.logger.error(f"Error in 'gacha' command: {e}", exc_info=True)
            await interaction.response.send_message(
                "Ocorreu um erro ao executar o comando gacha. Por favor, tente novamente mais tarde."
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(GachaCog(bot))
