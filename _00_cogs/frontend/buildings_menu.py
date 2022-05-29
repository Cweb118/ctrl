from nextcord import Interaction, ButtonStyle
from _00_cogs.frontend.elements import Button
from .manage_menu import manageMenu
from _00_cogs.frontend.menu import Menu


class BuildingsMenu(Menu):
    def __init__(self):
        super().__init__('buildingsMenu')

    def render(self, state):

        return ('test', [])
        
buildingsMenu = BuildingsMenu()