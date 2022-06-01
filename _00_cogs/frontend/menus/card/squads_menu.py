from discord import SelectOption
from nextcord import Interaction, ButtonStyle
from _00_cogs.frontend.elements import Button, UnlimitedSelect
from _00_cogs.frontend.state_error import StateError
from _00_cogs.frontend.menu import Menu
from _01_functions import *
from _02_global_dicts import theJar
import _00_cogs.frontend.menus.menus as Menus


def squadOptions(state):
    if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

    player = theJar['players'][state['player']]

    options = []

    for squad in player.squads:
        rep = squad.drop_rep()
        options.append(SelectOption(label=rep, value=squad.uniqueID))
    
    return options

class SquadsMenu(Menu):
    def __init__(self):
        super().__init__('squadsmenu')

    def render(self, state):
        content = 'Select a squad below to view its information and issue orders'

        embed = createEmbed(content, title='**================[Squads]================**')

        return ('', [embed])

    @UnlimitedSelect(id='squad', optionsFun=squadOptions)
    async def squad(self, state, interaction: Interaction):
        if 'player' not in state:
            raise StateError

        squadID = interaction.data['values'][0]

        await Menus.squadMenu.show(interaction, reply=True, newState={'player': state['player'], 'squad': squadID})
        return True

