import random
import re

import discord
from discord.ext import commands

from config.base_cogs import BaseCog
from repositories.character_repository import get_character_by_player_id
from repositories.user_repository import get_or_create_user

dice_attr_pattern = re.compile(
    r"(\d+)\s*[dD]\s*(\d+)\s*(?:[+\-]\s*(\d+))?\s*(?:([a-zA-ZçãõáéíóúâêîôûàèìòùäëïöüÇÃÕÁÉÍÓÚÂÊÎÔÛÀÈÌÒÙÄËÏÖÜ]+))?"
)


ATTRIBUTE_MAPPINGS = {
    # Vitality
    "vitalidade": "vitality",
    "vida": "vitality",
    "vit": "vitality",
    # Dexterity
    "destreza": "dexterity",
    "des": "dexterity",
    "dex": "dexterity",
    # Intelligence
    "inteligencia": "intelligence",
    "inteligência": "intelligence",
    "int": "intelligence",
    # Strength
    "força": "strength",
    "forca": "strength",
    "for": "strength",
    "str": "strength",
    # Resistance
    "resistencia": "resistance",
    "resistência": "resistance",
    "res": "resistance",
    # Mana
    "mana": "mana",
    "man": "mana",
}

PORTUGUESE_MAPPINGS = {
    "vitality": "vitalidade",
    "dexterity": "destreza",
    "intelligence": "inteligência",
    "strength": "força",
    "resistance": "resistência",
    "mana": "mana",
}


class DiceCog(BaseCog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(bot)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        # Find all dice expressions that match our pattern
        matches = dice_attr_pattern.findall(message.content)
        if not matches:
            return

        for match in matches:
            number_of_dice = int(match[0])
            sides_per_die = int(match[1])

            # Handle numeric modifier
            modifier = int(match[2]) if match[2] else 0

            # Handle attribute modifier
            attr_name = match[3].lower() if match[3] else None

            if attr_name:
                # Get character's attribute value
                user = get_or_create_user(message.author.id)
                character = get_character_by_player_id(user.id)

                if character and attr_name in ATTRIBUTE_MAPPINGS:
                    attr_value = getattr(character, ATTRIBUTE_MAPPINGS[attr_name])
                    modifier += attr_value

            # Roll the dice
            rolls = [random.randint(1, sides_per_die) for _ in range(number_of_dice)]
            total = sum(rolls) + modifier

            # Build notation string
            notation_str = f"{number_of_dice}d{sides_per_die}"
            if modifier != 0:
                notation_str += f" {modifier:+d}"
            if attr_name:
                # Get the Portuguese display name for the attribute
                english_attr = ATTRIBUTE_MAPPINGS[attr_name]
                portuguese_attr = PORTUGUESE_MAPPINGS[english_attr]
                notation_str += f" ({portuguese_attr.capitalize()})"

            await message.reply(f"` {total} ` ⟵ {rolls} {notation_str}")


async def setup(bot: commands.Bot):
    await bot.add_cog(DiceCog(bot))
