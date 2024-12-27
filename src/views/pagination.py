from typing import Callable, Optional

import discord

from views.owner import OwnerView


class PaginationView(OwnerView):
    def __init__(
        self, user: discord.Member, interaction: discord.Interaction, get_page: Callable
    ):
        super().__init__(user)
        self.interaction = interaction
        self.get_page = get_page
        self.total_pages: Optional[int] = None
        self.index = 1
        super().__init__(user)

    async def navigate(self):
        emb, self.total_pages = await self.get_page(self.index)
        if self.total_pages == 1:
            await self.interaction.response.edit(embed=emb)
