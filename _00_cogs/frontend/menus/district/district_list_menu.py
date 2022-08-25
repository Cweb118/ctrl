from nextcord import Interaction, ButtonStyle, SelectOption
from _00_cogs.frontend.elements import Button, UnlimitedSelect
from _00_cogs.frontend.menu import Menu
from _00_cogs.frontend.state_error import StateError
from _02_global_dicts import theJar
from _01_functions import *
import _00_cogs.frontend.menus.menus as Menus

def districtOptions(state):
    options = []

    for district in theJar['districts'].values():
        options.append(SelectOption(label=district.name, value=district.name))

    return options

class DistrictListMenu(Menu):
    def __init__(self):
        super().__init__('districtlistmenu')

    def render(self, state):
        return ('Select a district', [])

    @UnlimitedSelect(id='district', optionsFun=districtOptions)
    async def district(self, state, interaction: Interaction):
        district_name = interaction.data['values'][0] 
        district = theJar['districts'][district_name]

        report, title, fields = district.report()
        embed = createEmbed(report, title=title, fields=fields)

        await interaction.followup.send(content='', embeds=[embed], ephemeral=True)
        return True