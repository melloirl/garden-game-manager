from typing import TYPE_CHECKING, Literal

import discord

from models.character import Character
from services.arcana_service import get_arcana_skill_ids
from services.character_service import (
    calculate_character_max_hp,
    calculate_character_max_mp,
    calculate_character_remaining_points,
)
from views.pagination import OwnerView, PaginationView

if TYPE_CHECKING:
    from models.arcana import ArcanaSkill


class CharacterView(OwnerView):
    def __init__(
        self,
        character: Character,
        arcana_skills: list["ArcanaSkill"],
        user: discord.Member,
        page: Literal["info", "attributes", "story", "arcana_skills"] = None,
    ):
        super().__init__(user)
        self.character = character
        self.arcana_skills = arcana_skills
        self.current_option = page or "info"
        self.pagination_view = None

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
            text=f"{self.character.region.name}",
            icon_url=self.character.region.icon_url,
        )
        return embed

    def attributes_embed(self):
        remaining_points = calculate_character_remaining_points(self.character)
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
        if remaining_points > 0:
            embed.add_field(
                name="Pontos Restantes",
                value=remaining_points,
                inline=False,
            )
            embed.set_footer(
                text="Use o comando /pontos para distribuir seus pontos em atributos!"
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
        return embed

    async def get_skills_page(self, page: int) -> tuple[discord.Embed, int]:
        """Returns (embed, total_pages) for the skills pagination"""
        skill_ids = get_arcana_skill_ids(self.character.arcana_skills)
        if not skill_ids:
            embed = discord.Embed(
                title="Arcana",
                description="Nenhuma habilidade desbloqueada\nTente treinar mais!",
                color=int(self.character.mana_nature.color, 16),
            )
            return embed, 1

        # Calculate pagination
        items_per_page = 5
        total_pages = (len(skill_ids) + items_per_page - 1) // items_per_page
        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        current_page_skills = skill_ids[start_idx:end_idx]

        # Create embed for current page
        embed = discord.Embed(
            title="Arcana",
            description="Habilidades de arcana desbloqueadas pelo personagem",
            color=int(self.character.mana_nature.color, 16),
        )

        lines = []
        for skill_id in current_page_skills:
            skill = self.arcana_skills[skill_id]
            lines.append(f"**{skill.name}**")

        embed.add_field(
            name=f"Habilidades (Página {page}/{total_pages}):",
            value="\n".join(lines),
            inline=False,
        )
        return embed, total_pages

    async def handle_skills_view(self, interaction: discord.Interaction):
        """Creates and manages the paginated skills view"""
        if not self.pagination_view:
            self.pagination_view = PaginationView(
                interaction.user, interaction, self.get_skills_page
            )
            await self.pagination_view.navigate()
        else:
            await interaction.response.send_message(
                "Uma visualização de habilidades já está ativa.", ephemeral=True
            )

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
        if self.current_option == "arcana_skills":
            await self.handle_skills_view(interaction)
        else:
            embeds = self.get_embeds_for_option(self.current_option)
            await interaction.response.edit_message(embeds=embeds, view=self)
