from nextcord import Interaction, ButtonStyle
from _00_cogs.frontend.elements import Button
from .manage_menu import manageMenu
from _00_cogs.frontend.menu import Menu


class UnitsMenu(Menu):
    def __init__(self):
        super().__init__('unitsmenu')

    def render(self, state):

        return ('test', [])
        
unitsMenu = UnitsMenu()