from nextcord import Interaction, ButtonStyle
from _00_cogs.frontend.elements import Button
from _00_cogs.frontend.menu import Menu
from _00_cogs.frontend.travel_menu import travelMenu
from _02_global_dicts import theJar
from _01_functions import *


class DistrictMenu(Menu):
    def __init__(self):
        super().__init__('districtmenu')

    def render(self, state):
        if 'district' not in state or state['district'] not in theJar['districts']:
            return

        district = theJar['districts'][state['district']]
        report, title, fields = district.report()
        embed = createEmbed(report, title=title, fields=fields)
        return ('', [embed])

    @Button(id='travel', label='Travel', style=ButtonStyle.success)
    async def travel(self, state, interaction: Interaction):
        if 'district' not in state:
            return False

        await travelMenu.show(interaction, reply=True, newState={'district': state['district']})
        return False

    @Button(id='interact', label='Interact', style=ButtonStyle.success)
    async def interact(self, state, interaction: Interaction):
        return False

districtMenu = DistrictMenu()