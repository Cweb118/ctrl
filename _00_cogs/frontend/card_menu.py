from nextcord import Interaction, ButtonStyle
from _00_cogs.frontend.elements import Button
from .manage_menu import manageMenu
from _00_cogs.frontend.menu import Menu


class CardMenu(Menu):
    def __init__(self):
        super().__init__('cardmenu')

    def render(self, state):
        if not ('count' in state):
            state['count'] = 0

        return ('Count: ' + str(state['count']), [])

    @Button(id='play', label='Play', style=ButtonStyle.success)
    async def play(self, state, interaction: Interaction):
        return False

    @Button(id='manage', label='Manage', style=ButtonStyle.success)
    async def manage(self, state, interaction: Interaction):
        await manageMenu.show(interaction, reply=True)
        
        return False

    @Button(id='command', label='Command', style=ButtonStyle.success)
    async def command(self, state, interaction: Interaction):
        return False

cardMenu = CardMenu()