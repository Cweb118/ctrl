from discord import SelectOption
from nextcord import Interaction, ButtonStyle
from _00_cogs.frontend.elements import Button, UnlimitedSelect
from _00_cogs.frontend.menu import Menu
from _00_cogs.frontend.state_error import StateError
from _02_global_dicts import theJar
from _01_functions import *

def travelOptions(state):
    if 'district' not in state or state['district'] not in theJar['districts']:
        raise StateError

    district = theJar['districts'][state['district']]
    paths = district.paths

    options = []

    for path in paths:
        options.append(SelectOption(label=path, value=path))

    return options


class TravelMenu(Menu):
    def __init__(self):
        super().__init__('travelmenu')

    def render(self, state):
        return('Select Destination:', [])

    
    @UnlimitedSelect(id='destination', optionsFun=travelOptions)
    async def destination(self, state, interaction: Interaction):
        state['destination'] = interaction.data['values'][0]
        return False

    @Button(id='confirm', label='Confirm', style=ButtonStyle.success)
    async def travel(self, state, interaction: Interaction):
        if 'destination' not in state:
            return False

        if state['destination'] not in theJar['districts'] or interaction.user.id not in theJar['players']:
            raise StateError
        
        destination = theJar['districts'][state['destination']]
        player = theJar['players'][interaction.user.id]

        await destination.movePlayer(player)

        return False

