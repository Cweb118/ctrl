from discord import SelectOption
from nextcord import Interaction, ButtonStyle
from _00_cogs.frontend.elements import Button, UnlimitedSelect
from _00_cogs.frontend.state_error import StateError
from _00_cogs.frontend.menu import Menu
from _01_functions import *
from _02_global_dicts import theJar


class SquadMenu(Menu):
    def __init__(self):
        super().__init__('squadmenu')

    def render(self, state):
        if 'squad' not in state or 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        player = theJar['players'][state['player']]
        squad = None

        for playerSquad in player.squads:
            if playerSquad.uniqueID == state['squad']:
                squad = playerSquad
                break

        if squad == None:
            raise StateError

        report, title, fields = squad.report()
        embed = createEmbed(report, title=title, fields=fields)

        return ('', [embed])

    @Button(id='move', label='Move', style=ButtonStyle.success)
    async def move(self, state, interaction: Interaction):
        return False

    @Button(id='rank', label='Rank', style=ButtonStyle.success)
    async def rank(self, state, interaction: Interaction):
        return False

    @Button(id='attack', label='Attack', style=ButtonStyle.success)
    async def attack(self, state, interaction: Interaction):
        return False

    @Button(id='disband', label='Disband', style=ButtonStyle.success)
    async def disband(self, state, interaction: Interaction):
        return False

