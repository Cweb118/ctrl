from discord import SelectOption
from nextcord import Interaction, ButtonStyle
from _00_cogs.frontend.elements import Button, UnlimitedSelect
from _00_cogs.frontend.state_error import StateError
from _00_cogs.frontend.menu import Menu
from _01_functions import *
from _02_global_dicts import theJar
import _00_cogs.frontend.menus.menus as Menus


class PlayerInfoMenu(Menu):
    def __init__(self):
        super().__init__('playerinfomenu')

    def render(self, state):
        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        player = theJar['players'][state['player']]
        report, title, fields = player.report()

        embed = createEmbed(report, title=title, fields=fields)

        return ('', [embed])