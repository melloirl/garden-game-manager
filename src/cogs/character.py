from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from config.base_cogs import PlayerCog
from models.character import Character
from repositories.character_repository import (
    get_character_by_player_id,
)
from repositories.user_repository import get_or_create_user
from services.character_service import (
    calculate_character_max_hp,
    calculate_character_max_mp,
)
from utils.arcana_bitfield import get_skill_ids
from views.owner import OwnerView

if TYPE_CHECKING:
    from models.arcana import ArcanaSkill


class CharacterView(OwnerView):
    def __init__(
        self,
        character: Character,
        arcana_skills: list["ArcanaSkill"],
        user: discord.Member,
    ):
        super().__init__(user)
        self.character = character
        self.arcana_skills = arcana_skills
        self.current_option = "info"

    def format_character_title(self):
        title = f", {self.character.title}" if self.character.title else ""
        return f"{self.character.name}{title}"

    def overview_embed(self):
        def generate_hearts(current_hp: int, max_hp: int, total_hearts: int = 5) -> str:
            ratio = current_hp / max_hp if max_hp > 0 else 0
            filled = int(ratio * total_hearts)
            return "♥" * filled + "♡" * (total_hearts - filled)

        embed_color = int(self.character.mana_nature.color, 16)
        embed = discord.Embed(
            title=self.format_character_title(),
            description="*Visão Geral*",
            color=embed_color,
        )
        embed.add_field(name="Idade", value=self.character.age, inline=True)
        embed.add_field(name="Origem", value=self.character.region.name, inline=True)
        embed.add_field(name="Raça", value=self.character.race.name, inline=True)
        embed.add_field(name="Mana", value=self.character.mana_nature.name, inline=True)
        embed.add_field(
            name="HP",
            value=generate_hearts(
                self.character.current_hp, calculate_character_max_hp(self.character)
            ),
            inline=True,
        )
        embed.add_field(
            name="MP",
            value=generate_hearts(
                self.character.current_mp, calculate_character_max_mp(self.character)
            ),
            inline=True,
        )
        embed.add_field(
            name="Nível",
            value=f"{self.character.level} ({self.character.xp_points} XP)",
            inline=True,
        )
        embed.set_image(url=self.character.image_url)
        embed.set_footer(
            text=f"Origem: {self.character.region.name}",
            icon_url=self.character.region.icon_url,
        )
        return embed

    def attributes_embed(self):
        embed_color = int(self.character.mana_nature.color, 16)
        embed = discord.Embed(title="Atributos", color=embed_color)

        embed.add_field(
            name="Vitalidade", value=f"+{self.character.vitality}", inline=True
        )
        embed.add_field(name="Força", value=f"+{self.character.strength}", inline=True)
        embed.add_field(
            name="Resistência", value=f"+{self.character.resistance}", inline=True
        )
        embed.add_field(
            name="Inteligência", value=f"+{self.character.intelligence}", inline=True
        )
        embed.add_field(
            name="Destreza", value=f"+{self.character.dexterity}", inline=True
        )
        embed.add_field(name="Mana", value=f"+{self.character.mana}", inline=True)
        embed.add_field(
            name="Pontos Restantes", value=self.character.remaining_points, inline=False
        )
        embed.set_thumbnail(url="https://i.imgur.com/aEfpfgp.png")

        return embed

    def story_embed(self):
        embed_color = int(self.character.mana_nature.color, 16)
        embed = discord.Embed(
            title="História",
            description=self.character.story or "Nenhuma história disponível",
            color=embed_color,
        )
        # Potentially add a short snippet if story is too long
        return embed

    def skills_embed(self):
        embed_color = int(self.character.mana_nature.color, 16)
        embed = discord.Embed(
            title="Arcana",
            description="Habilidades de arcana desbloqueadas pelo personagem",
            color=embed_color,
        )
        skill_ids = get_skill_ids(self.character.arcana_skills)
        if not skill_ids:
            embed.add_field(
                name="Nenhuma habilidade desbloqueada", value="Tente treinar mais!"
            )
            return embed

        lines = []
        for skill_id in skill_ids:
            skill = self.arcana_skills[skill_id]
            tier_symbol = {1: "⭐", 2: "🌟", 3: "💫"}.get(skill.tier.tier_level, "")
            lines.append(f"{tier_symbol} **{skill.name}** — {skill.description}")

        embed.add_field(name="Habilidades:", value="\n".join(lines), inline=False)
        return embed

    def get_embeds_for_option(self, option: str) -> list[discord.Embed]:
        if option == "info":
            return [self.overview_embed()]
        elif option == "attributes":
            return [self.attributes_embed()]
        elif option == "story":
            return [self.story_embed()]
        elif option == "arcana_skills":
            return [self.skills_embed()]
        # Default/fallback
        return [self.overview_embed()]

    @discord.ui.select(
        placeholder="Selecione uma categoria",
        options=[
            discord.SelectOption(label="Visão Geral", value="info"),
            discord.SelectOption(label="Atributos", value="attributes"),
            discord.SelectOption(label="História", value="story"),
            discord.SelectOption(label="Arcana", value="arcana_skills"),
        ],
    )
    async def skill_select(
        self, interaction: discord.Interaction, select: discord.ui.Select
    ):
        self.current_option = select.values[0]
        embeds = self.get_embeds_for_option(self.current_option)
        await interaction.response.edit_message(embeds=embeds, view=self)


class CharacterCog(PlayerCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)
        self.arcana_skills = bot.arcana_skills

    @app_commands.command(
        name="ficha", description="Mostra a ficha do seu personagem ativo."
    )
    async def player(self, interaction: discord.Interaction):
        user = get_or_create_user(interaction.user.id)
        character = get_character_by_player_id(user.id)
        self.bot.logger.info(f"Bitfield: {character.arcana_skills}")
        view = CharacterView(character, self.arcana_skills, interaction.user)
        # To avoid cluttering the channel, the message will be deleted after 5 minutes.
        await interaction.response.send_message(
            embed=view.overview_embed(),
            view=view,
            delete_after=5 * 60,
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(CharacterCog(bot))
