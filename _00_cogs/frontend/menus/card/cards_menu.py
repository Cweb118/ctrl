from discord import SelectOption
from nextcord import Interaction, ButtonStyle
from _00_cogs.frontend.elements import Button, UnlimitedSelect
from _00_cogs.frontend.state_error import StateError
from _00_cogs.frontend.menu import Menu
from _01_functions import *
from _02_global_dicts import theJar
import _00_cogs.frontend.menus.menus as Menus

def cardOptions(state):
    if 'card_type' not in state:
        raise StateError

    if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

    player = theJar['players'][state['player']]

    options = []

    for unit in player.inventory.cards[state['card_type']]:
        rep = unit.drop_rep()
        (line1, line2) = rep.split('\n  ')

        options.append(SelectOption(label=line1, value=unit.uniqueID, description=line2))
    
    return options

class CardsMenu(Menu):
    def __init__(self):
        super().__init__('cardsmenu')

    def render(self, state):
        if 'card_type' not in state:
            raise StateError

        content = 'Select a ' + state['card_type'] + ' below to view its information and issue orders'

        if state['card_type'] == 'unit':
            title = '**=================[Units]================**'
        else:
            title = '**===============[Buildings]===============**'

        embed = createEmbed(content, title=title)

        return ('', [embed])

    @UnlimitedSelect(id='card', optionsFun=cardOptions)
    async def card(self, state, interaction: Interaction):
        if 'card_type' not in state:
            raise StateError

        if 'player' not in state:
            raise StateError

        cardID = interaction.data['values'][0]

        await Menus.cardMenu.show(interaction, reply=True, newState={'card': cardID, 'card_type': state['card_type'], 'player': state['player']})
        return True

def canPlayCard(state):
    if 'card' not in state or 'card_type' not in state:
        raise StateError

    if 'player' not in state or state['player'] not in theJar['players']:
        raise StateError

    player = theJar['players'][state['player']]
    card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

    return card.status == 'Held'

class CardMenu(Menu):
    def __init__(self):
        super().__init__('cardmenu')

    def render(self, state):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        player = theJar['players'][state['player']]
        card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

        if card == None:
            raise StateError

        report, title, fields = card.report()
        embed = createEmbed(report, title=title, fields=fields)

        return ('', [embed])

    @Button(id='play', label='Play', style=ButtonStyle.success, disabledFun=lambda state: not canPlayCard(state))
    async def play(self, state, interaction: Interaction):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        await Menus.playMenu.show(interaction, newState={'card': state['card'], 'card_type': state['card_type'], 'player': state['player']})
        return False

    @Button(id='manage', label='Manage', style=ButtonStyle.success)
    async def manage(self, state, interaction: Interaction):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        await Menus.manageMenu.show(interaction, newState={'card': state['card'], 'card_type': state['card_type'], 'player': state['player']})
        return False

    @Button(id='command', label='Command', style=ButtonStyle.success, includeFun=lambda state: 'card_type' in state and state['card_type'] == 'unit')
    async def command(self, state, interaction: Interaction):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        await Menus.commandMenu.show(interaction, newState={'card': state['card'], 'card_type': state['card_type'], 'player': state['player']})
        return False

    @Button(id='link', label='Link', style=ButtonStyle.success, includeFun=lambda state: 'card_type' in state and state['card_type'] == 'building')
    async def link(self, state, interaction: Interaction):
        return False

