from discord import SelectOption
from nextcord import Interaction, ButtonStyle
from _00_cogs.frontend.elements import Button, UnlimitedSelect
from _00_cogs.frontend.state_error import StateError
from _00_cogs.frontend.menu import Menu, MenuView
from _01_functions import *
from _02_global_dicts import theJar
import _00_cogs.frontend.menus.menus as Menus
import _00_cogs.frontend.modals.modals as Modals

def cantInteract(state):
    if 'card' not in state or 'card_type' not in state:
        raise StateError

    if 'player' not in state or state['player'] not in theJar['players']:
        raise StateError

    player = theJar['players'][state['player']]
    card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

    if card.location == player.location:
        return False

    return True

class ManageMenu(Menu):
    def __init__(self):
        super().__init__('managemenu')

    def render(self, state):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        player = theJar['players'][state['player']]
        card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

        if card is None:
            raise StateError

        return ('What do you want to do with the ' + card.title + ' card?', [])

    @Button(id='take', label='Take', style=ButtonStyle.success, disabledFun=cantInteract)
    async def take(self, state, interaction: Interaction):
        await Menus.transferResourceMenu.show(interaction, reply=True, newState={'src_type': 'card', 'src_card': state['card'], 'src_card_type': state['card_type'], 'src_player': state['player'], 'dest_type': 'player', 'dest_player': state['player']})
        return False

    @Button(id='give', label='Give', style=ButtonStyle.success, disabledFun=cantInteract)
    async def give(self, state, interaction: Interaction):
        await Menus.transferResourceMenu.show(interaction, reply=True, newState={'src_type': 'player', 'src_player': state['player'], 'dest_type': 'card', 'dest_card': state['card'], 'dest_card_type': state['card_type'], 'dest_player': state['player']})
        return False

    @Button(id='nickname', label='Nickname', style=ButtonStyle.success, defer=False)
    async def nickname(self, state, interaction: Interaction):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        player = theJar['players'][state['player']]
        card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

        if card is None:
            raise StateError

        await Modals.nicknameModal.show(interaction, state={'card': state['card'], 'card_type': state['card_type'], 'player': state['player']})
        return False

    @Button(id='cancel', label='Cancel', style=ButtonStyle.danger)
    async def cancel(self, state, interaction: Interaction):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        await Menus.cardMenu.show(interaction, newState={'card': state['card'], 'card_type': state['card_type'], 'player': state['player']})
        return False