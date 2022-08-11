from discord import SelectOption
from nextcord import Interaction, ButtonStyle
from _00_cogs.frontend.elements import Button, UnlimitedSelect
from _00_cogs.frontend.state_error import StateError
from _00_cogs.frontend.menu import Menu, MenuView
from _01_functions import *
from _02_global_dicts import theJar
import _00_cogs.frontend.menus.menus as Menus
import _00_cogs.frontend.modals.modals as Modals

class CommandMenu(Menu):
    def __init__(self):
        super().__init__('commandmenu')

    def render(self, state):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        player = theJar['players'][state['player']]
        card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

        if card is None:
            raise StateError

        return ('What orders do you want to give the ' + card.title + ' card?', [])

    @Button(id='move', label='Move', style=ButtonStyle.success, includeFun=lambda state: 'card_type' in state and state['card_type'] == 'unit')
    async def move(self, state, interaction: Interaction):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError 

        player = theJar['players'][state['player']]
        card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

        if card is None:
            raise StateError

        await Menus.moveMenu.show(interaction, newState={'card': state['card'], 'card_type': state['card_type'], 'player': state['player']})
        return False

    @Button(id='gather', label='Gather', style=ButtonStyle.success)
    async def gather(self, state, interaction: Interaction):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError 

        player = theJar['players'][state['player']]
        card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

        if card is None:
            raise StateError

        if type(card.location).__name__ == 'District':
            await Menus.transferResourceMenu.show(interaction, reply=True, newState={'src_type': 'district', 'src_district': card.location.name, 'dest_type': 'card', 'dest_card': state['card'], 'dest_card_type': state['card_type'], 'dest_player': state['player']})
        else:
            await Menus.transferResourceMenu.show(interaction, reply=True, newState={'src_type': 'card', 'src_card': card.location.uniqueID, 'src_card_type': 'building', 'src_player': state['player'], 'dest_type': 'card', 'dest_card': state['card'], 'dest_card_type': state['card_type'], 'dest_player': state['player']})        
        
        return False

    @Button(id='drop', label='Drop', style=ButtonStyle.success)
    async def drop(self, state, interaction: Interaction):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError 

        player = theJar['players'][state['player']]
        card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

        if card is None:
            raise StateError

        if type(card.location).__name__ == 'District':
            await Menus.transferResourceMenu.show(interaction, reply=True, newState={'src_type': 'card', 'src_card': state['card'], 'src_card_type': state['card_type'], 'src_player': state['player'], 'dest_type': 'district', 'dest_district': card.location.name})
        else:
            await Menus.transferResourceMenu.show(interaction, reply=True, newState={'src_type': 'card', 'src_card': state['card'], 'src_card_type': state['card_type'], 'src_player': state['player'], 'dest_type': 'card', 'dest_card': card.location.uniqueID, 'dest_card_type': 'building', 'dest_player': state['player']})

        return False

    @Button(id='act', label='Act', style=ButtonStyle.success)
    async def act(self, state, interaction: Interaction):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError 

        player = theJar['players'][state['player']]
        card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

        await Menus.actMenu.show(interaction, newState={'card': state['card'], 'card_type': state['card_type'], 'player': state['player']})
        return False

    @Button(id='cancel', label='Cancel', style=ButtonStyle.danger)
    async def cancel(self, state, interaction: Interaction):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        await Menus.cardMenu.show(interaction, newState={'card': state['card'], 'card_type': state['card_type'], 'player': state['player']})
        return False