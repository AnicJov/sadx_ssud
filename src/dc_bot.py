from discord.ext import commands
from draft import DraftController
from typing import List

import discord


class SSUDBot(commands.Bot):
    def __init__(self, controller):
        self.controller = controller
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=intents)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

class ChoiceButton(discord.ui.Button['Choice']):
    icons = {
        "Tails": ('tails', 1337077438802563204),
        "Super Sonic": ('supersonic', 1337077427935117326),
        "Knuckles": ('knuckles', 1337077410625093662),
        "Gamma": ('gamma', 1337077396582436985),
        "Big": ('big', 1337077386939863071),
        "Amy": ('amy', 1337077368048713729)
    }

    def __init__(self, story: str):
        self.story = story
        super().__init__(style=discord.ButtonStyle.secondary, emoji=discord.PartialEmoji(name=self.icons[story][0], id=self.icons[story][1]), label=story)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(content=f"You banned {self.story}")


class Choice(discord.ui.View):
    children: List[ChoiceButton]

    choices = ["Amy", "Big", "Gamma", "Knuckles", "Super Sonic", "Tails"]

    def __init__(self):
        super().__init__()

        for choice in self.choices:
            self.add_item(ChoiceButton(choice))
    

if __name__ == "__main__":
    controller = DraftController()
    bot = SSUDBot(controller)

    @bot.command()
    async def choice(ctx: commands.Context):
        """Starts a counter for pressing."""
        await ctx.send('Player 1, choose a story to ban:', view=Choice())

    bot.run('MTMzNzA3NDczOTIzNTEyNzM0Nw.GO9giO.7h0hY1eWUVkTM_dWxnroxyqyF7D1XXMbL3dwWc')
