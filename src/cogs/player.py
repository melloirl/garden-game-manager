import discord
from discord.ext import commands
from discord import app_commands
from services.character_service import get_character_by_player_id
from services.user_service import get_or_create_user
from models.character import Character
from utils.arcana_bitfield import get_skill_ids

class CharacterView(discord.ui.View):
    def __init__(self, character: Character, arcana_skills: list["ArcanaSkill"]):
        super().__init__()
        self.character = character
        self.arcana_skills = arcana_skills

    def format_character_title(self):
        title = f", {self.character.title}" if self.character.title else ""
        return f"{self.character.name}{title}"
    
    def info_embed(self):
        embed_color = int(self.character.mana_nature.color, base=16)
        embed = discord.Embed(title=self.format_character_title(), description="*Informações*", color=embed_color)
        embed.add_field(name="Idade", value=self.character.age, inline=True)
        embed.add_field(name="Origem", value=self.character.region.name, inline=True)
        embed.add_field(name=u"\u200B", value=u"\u200B", inline=True) # Empty field to center the text content
        embed.add_field(name="Raça", value=self.character.race.name, inline=True)
        embed.add_field(name="Mana", value=self.character.mana_nature.name, inline=True)
        embed.add_field(name=u"\u200B", value=u"\u200B", inline=True) # Empty field to center the text content
        embed.set_image(url=self.character.image_url)
        embed.set_footer(text=f"{self.character.region.name}", icon_url=self.character.region.icon_url)
        return embed
  
    def skills_embed(self):
        embed_color = int(self.character.mana_nature.color, base=16)
        embed = discord.Embed(title=f"{self.character.name}", description="*Habilidades*", color=embed_color)
        # Get the skill id list from the bitfield
        skill_ids = get_skill_ids(self.character.arcana_skills)
        skill_names = [self.arcana_skills[skill_id].name for skill_id in skill_ids]

        embed.add_field(name="Habilidades:", value="\n".join(skill_names), inline=False)
        return embed
   
    @discord.ui.select(placeholder="Informações", options=[discord.SelectOption(label="Informações", value="info"), discord.SelectOption(label="Habilidades", value="skills")])
    async def skill_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        if select.values[0] == "info":
            await interaction.response.edit_message(embed=self.info_embed(), view=self)
        elif select.values[0] == "skills":
            await interaction.response.edit_message(embed=self.skills_embed(), view=self)

class PlayerCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.arcana_skills = bot.arcana_skills

    @app_commands.command(name="ficha", description="Mostra a ficha do seu personagem ativo.")
    async def player(self, interaction: discord.Interaction):
        user = get_or_create_user(interaction.user.id)
        character = get_character_by_player_id(user.id)
        self.bot.logger.info(f"Bitfield: {character.arcana_skills}")
        view = CharacterView(character, self.arcana_skills)
        embed = view.info_embed()
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(PlayerCog(bot))
