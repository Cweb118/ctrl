from discord import SelectOption
from nextcord import Interaction, ButtonStyle
from _00_cogs.frontend.elements import Button, UnlimitedSelect
from _00_cogs.frontend.menu import Menu
from _00_cogs.frontend.state_error import StateError
from _02_global_dicts import theJar
from _01_functions import *
import _00_cogs.frontend.menus.menus as Menus

class InteractMenu(Menu):
    def __init__(self):
        super().__init__('interactmenu')

    def render(self, state):
        return('How do you want to interact with this location?', [])

    @Button(id='take', label='Take', style=ButtonStyle.success)
    async def take(self, state, interaction: Interaction):
        if 'district' not in state:
            raise StateError

        await Menus.transferResourceMenu.show(interaction, reply=True, newState={'src_type': 'district', 'src_district': state['district'], 'dest_type': 'player', 'dest_player': interaction.user.id})
        return False

    @Button(id='drop', label='Drop', style=ButtonStyle.success)
    async def drop(self, state, interaction: Interaction):
        if 'district' not in state:
            raise StateError

        await Menus.transferResourceMenu.show(interaction, reply=True, newState={'src_type': 'player', 'src_player': interaction.user.id, 'dest_type': 'district', 'dest_district': state['district']})
        return False