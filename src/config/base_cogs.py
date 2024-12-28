import discord
from discord.ext import commands

from repositories.character_repository import get_character_by_player_id
from repositories.user_repository import get_or_create_user


class BaseCog(commands.Cog):
    """
    Automatically registers the user before each slash command.
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """
        Called before every slash command in this Cog runs.
        Return True to allow the command, False to block it.
        """
        try:
            get_or_create_user(interaction.user.id, interaction.user.display_name)
        except Exception as e:
            self.bot.logger.error(f"Error in user registration: {e}", exc_info=True)
        return True


class PlayerCog(BaseCog):
    """
    Extends BaseCog to *also* check if the user has a character in the DB
    for every slash command in this Cog.
    """

    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(bot)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """
        Runs *in addition to* BaseCog's interaction_check.
        If BaseCog's interaction_check doesn't raise or return False,
        this function is called next.
        """
        # 1) Let BaseCog do user registration
        base_check_ok = await super().interaction_check(interaction)
        if not base_check_ok:
            return False

        # 2) Now check if the user has a character
        user = get_or_create_user(interaction.user.id)
        if not get_character_by_player_id(user.id):
            emb = discord.Embed(
                title="Você não possui um personagem registrado!",
                description="Entre em contato com <@!149655287744167936> para criar um personagem.",
                color=discord.Color.red(),
            )
            await interaction.response.send_message(embed=emb, ephemeral=True)
            return False

        return True
