from nextcord import Interaction, ButtonStyle
from _00_cogs.frontend.elements import Button
from .manage_menu import manageMenu
from _00_cogs.frontend.menu import Menu


class SquadsMenu(Menu):
    def __init__(self):
        super().__init__('squadsmenu')

    def render(self, state):

        return ('test', [])
        
squadsMenu = SquadsMenu()