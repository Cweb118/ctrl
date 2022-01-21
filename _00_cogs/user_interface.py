
import nextcord
from _02_global_dicts import player_dict, district_dict
from nextcord import interactions
from nextcord.ext import commands
from nextcord.ext.commands import bot

class TargetSelect(nextcord.ui.Select):
    def __init__(self, optionsDict):
        options = []
        for key in optionsDict.keys():
            options.append(nextcord.SelectOption(label=key, description=optionsDict[key]))
        super().__init__(options=options, min_values=1, max_values=1, placeholder="Select a target for your card!")

class CardSelect(nextcord.ui.Select):
    def __init__(self, optionsDict):
        #Options should be a dict that contains what should be displayed in the dropdown. The key should be the name and the value the description.
        options = []
        for key in optionsDict.keys():
            options.append(nextcord.SelectOption(label=key, description=optionsDict[key]))
        super().__init__(options=options, min_values=1, max_values=1, placeholder="Select a card to play!")

        self.selection = None
    
    async def callback(self, interaction: nextcord.Interaction):
        self.selection = self.values[0]

class DropdownView(nextcord.ui.View):
    def __init__(self, cardsDict, targetDict):
        super().__init__(timeout=None)
        self.add_item(CardSelect(cardsDict))
        self.add_item(TargetSelect(targetDict))
    
    @nextcord.ui.button(label="Play", style=nextcord.ButtonStyle.green)
    async def playCard(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        pass


class UserInterface(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="playUI")
    async def playUI(self, ctx):
        id = ctx.author.id
        player = player_dict[id]
        playerCards = player.inventory.cards

        cards = {}
        targets = {}

        for card in playerCards["unit"]:
            cards[card.title] = card.description
        view = DropdownView(cards)

        await ctx.send(" a", view=view)


def setup(bot):
    bot.add_cog(UserInterface(bot))
