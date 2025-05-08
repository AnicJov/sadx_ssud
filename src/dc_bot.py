import discord
from discord.ext import commands
from time import sleep

from splits import generate_livesplit_file, generate_split_names


AUTHORIZED_USERS = [
    147104361032450048, # Anic
    127194734916665346, # Labrys
    277453062111494145, # Skoob
    493499862281748507, # Wither
    204385793559625728, # Drum
    265601121328955392, # Mimik
    998715376898678916, # Underground
    83959976095125504,  # Deku
]

PACEKEEPING_CHANNEL = 1369855193583321209

class ChoiceButton(discord.ui.Button):
    icons = {
        "Tails": ('tails', 1337077438802563204),
        "Super Sonic": ('supersonic', 1337077427935117326),
        "Knuckles": ('knuckles', 1337077410625093662),
        "Gamma": ('gamma', 1337077396582436985),
        "Big": ('big', 1337077386939863071),
        "Amy": ('amy', 1337077368048713729)
    }

    def __init__(self, story: str, controller, player: discord.User):
        self.story = story
        self.controller = controller
        self.player = player
        self.draft_phase = self.controller.draft_phase
        emoji_name, emoji_id = self.icons[story]
        emoji = discord.PartialEmoji(name=emoji_name, id=emoji_id)
        super().__init__(style=discord.ButtonStyle.secondary, emoji=emoji, label=story)

    async def callback(self, interaction: discord.Interaction):
        # Only allow the correct player
        if interaction.user.id != self.player.id:
            await interaction.response.send_message("You're not allowed to make this choice.", ephemeral=True)
            return

        # Prevent late responses
        if self.draft_phase != self.controller.draft_phase:
            await interaction.message.delete()
            await interaction.response.send_message("This choice has already been made.", ephemeral=True)
            return

        await interaction.message.delete()
        self.controller.make_choice(self.story)

class ChoiceView(discord.ui.View):
    def __init__(self, controller, prompt: str, player: discord.User):
        super().__init__(timeout=None)
        self.controller = controller
        self.player = player
        self.prompt = prompt
        for story in self.controller.available_choices():
            self.add_item(ChoiceButton(story, controller, player))

class DraftBot(commands.Bot):
    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        self.p1_user = None
        self.p2_user = None
        self.channel = None
        self.pacekeeping_channel = None

    async def on_ready(self):
        self.pacekeeping_channel = self.get_channel(PACEKEEPING_CHANNEL)
        if self.pacekeeping_channel is None:
            self.pacekeeping_channel = await self.fetch_channel(PACEKEEPING_CHANNEL)

    async def setup_hook(self):
        # register commands

        # TODO: Create !choice command
        # TODO: Create !auth command
        # TODO: Add coinflip funciton

        @self.command(name="start")
        async def start(ctx, user1: discord.User, user2: discord.User):
            if ctx.author.id not in AUTHORIZED_USERS:
                await ctx.send("You are not authorized to start a draft.")
                return
            if self.controller.draft_phase != 0:
                await ctx.send("A draft is already in progress.")
                return
            self.p1_user = user1
            self.p2_user = user2
            self.channel = ctx.channel
            await ctx.send(f"Draft started between {user1.mention} and {user2.mention}. Use !spin to begin.")

        @self.command(name="reset")
        async def reset(ctx):
            if ctx.author.id not in AUTHORIZED_USERS:
                return
            self.controller.reset_draft()
            await ctx.send("Draft has been reset.")

        @self.command(name="undo")
        async def undo(ctx):
            if ctx.author.id not in AUTHORIZED_USERS:
                return
            self.controller.undo_last_action()
            await ctx.send("Reverted last action.")

        @self.command(name="spin")
        async def spin(ctx):
            if ctx.author.id not in AUTHORIZED_USERS:
                return
            if self.controller.draft_phase != 0:
                await ctx.send("Cannot spin now.")
                return
            self.controller.spin_wheel()
            await ctx.send("Spinning the wheel...")

        @self.command(name="countdown")
        async def countdown(ctx, count=5):
            if ctx.author.id not in AUTHORIZED_USERS:
                return
            for i in reversed(range(count+1)):
                if i == 0:
                    await ctx.send("# GO!")
                    return

                await ctx.send(str(i))
                sleep(1)

    async def on_draft_updated(self):
        phase = self.controller.draft_phase

        # Generate split file(s)
        if phase == 5:
            picks = "\n- ".join(self.controller.picks)
            splits_path = generate_livesplit_file(self.controller.picks)
            if "Gamma" in self.controller.picks:
                alt_splits_path = generate_livesplit_file(self.controller.picks, glitched_gamma=False)

        # Create and send last action performed
        if not self.channel:
            return

        last_action = self.controller.history[-1]
        last_action_string = ""

        match last_action[0]:
            case "wheel":
                last_action_string += "The wheel"
            case "p1":
                if self.p1_user:
                    last_action_string += self.p1_user.display_name
                else:
                    last_action_string += "Player 1"
            case "p2":
                if self.p2_user:
                    last_action_string += self.p2_user.display_name
                else:
                    last_action_string += "Player 2"

        last_action_string += " picked ✅ " if last_action[1] == "pick" else " banned 🚫 "
        
        if last_action[1] == "pick":
            last_action_string += "**" + self.controller.picks[-1] + "**"
        else:
            last_action_string += "**" + self.controller.bans[-1] + "**"

        await self.channel.send(last_action_string)

        # Prompt for next action
        if phase == 1:
            view = ChoiceView(self.controller, "Player 1: Choose a story to ban", self.p1_user)
            await self.channel.send(f"{self.p1_user.mention}, ban a story:", view=view)
        elif phase == 2:
            view = ChoiceView(self.controller, "Player 2: Choose a story to ban", self.p2_user)
            await self.channel.send(f"{self.p2_user.mention}, ban a story:", view=view)
        elif phase == 3:
            view = ChoiceView(self.controller, "Player 2: Choose a story to pick", self.p2_user)
            await self.channel.send(f"{self.p2_user.mention}, pick a story:", view=view)
        elif phase == 4:
            view = ChoiceView(self.controller, "Player 1: Choose a story to pick", self.p1_user)
            await self.channel.send(f"{self.p1_user.mention}, pick a story:", view=view)
        elif phase == 5:
            await self.channel.send(f"Draft complete!\nStories picked: \n- {picks}")
            await self.channel.send("Here are your splits:", file=discord.File(splits_path))
            # TODO: Send pacekeeping slits for both glitched and linear Gamma
            await self.pacekeeping_channel.send("Pacekeeping splits "
                                                + "+".join(self.controller.picks)
                                                + " for " + self.p1_user.display_name
                                                + " vs. " + self.p2_user.display_name + ":")
            await self.pacekeeping_channel.send("```\n" + "\n".join(generate_split_names(self.controller.picks)) + "```")
            if "Gamma" in self.controller.picks:
                await self.channel.send(file=discord.File(alt_splits_path))

def create_bot(controller):
    intents = discord.Intents.default()
    intents.message_content = True
    bot = DraftBot(controller, command_prefix="!", intents=intents)
    return bot
