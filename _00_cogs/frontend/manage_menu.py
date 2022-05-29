from nextcord import Interaction, ButtonStyle
from _00_cogs.frontend.elements import Button
from _00_cogs.frontend.menu import Menu


class ManageMenu(Menu):
    def __init__(self):
        super().__init__('managemenu')

    def render(self, state):
        if not ('count' in state):
            state['count'] = 0

        return ('Count: ' + str(state['count']), [])

    @Button(id='take', label='Take', style=ButtonStyle.success)
    async def take(self, state, interaction: Interaction):
        return False

    @Button(id='drop', label='Drop', style=ButtonStyle.success)
    async def drop(self, state, interaction: Interaction):
        return False

    @Button(id='name', label='Name', style=ButtonStyle.success)
    async def name(self, state, interaction: Interaction):
        return False

manageMenu = ManageMenu()