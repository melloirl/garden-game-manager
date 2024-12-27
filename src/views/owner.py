import discord


class OwnerView(discord.ui.View):
    """This view can only be interacted with by the original sender"""

    def __init__(self, user: discord.Member):
        super().__init__(timeout=None)
        self.user = user

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id == self.user.id:
            return True
        else:
            emb = discord.Embed(
                description="Somente o autor do comando pode realizar esta ação",
                color=16711680,
            )
            await interaction.response.send_message(
                embed=emb, ephemeral=True, delete_after=5
            )
            return False
