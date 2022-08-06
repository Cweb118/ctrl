from discord import SelectOption
from nextcord import Interaction, ButtonStyle
from _00_cogs.frontend.elements import Button, UnlimitedSelect
from _00_cogs.frontend.menus.card.actions.action import getAction, resolveAction
from _00_cogs.frontend.state_error import StateError
from _00_cogs.frontend.menu import Menu, MenuView
from _01_functions import *
from _02_global_dicts import theJar
import _00_cogs.frontend.menus.menus as Menus
import _00_cogs.frontend.modals.modals as Modals

def actionOptions(state):
    if 'card' not in state or 'card_type' not in state:
        raise StateError

    if 'player' not in state or state['player'] not in theJar['players']:
        raise StateError

    player = theJar['players'][state['player']]
    card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

    if card is None:
        raise StateError

    options = []

    if card.skillsets:
        for trait in card.skillsets.values():
            for skillset in trait:
                if 'on_act' in skillset.triggers:
                    id = skillset.act_id
                    name = skillset.act_name

                    options.append(SelectOption(label=name, value=id))

    return options

class ActMenu(Menu):
    def __init__(self):
        super().__init__('actmenu')

    def render(self, state):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        player = theJar['players'][state['player']]
        card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

        if card is None:
            raise StateError

        return ('What action do you want the ' + card.title + ' card to take?', [])

    @UnlimitedSelect(id='action', optionsFun=actionOptions)
    async def action(self, state, interaction: Interaction):
        state['action'] = interaction.data['values'][0]
        return False

    @Button(id='confirm', label='Confirm', style=ButtonStyle.success)
    async def confirm(self, state, interaction: Interaction):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        player = theJar['players'][state['player']]
        card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

        if card is None:
            raise StateError

        if 'action' not in state:
            return False

        action = getAction(card, state['action'])

        if action is None:
            raise StateError

        await resolveAction(interaction, {
            'card': state['card'], 'card_type': state['card_type'],
            'player': state['player'],
            'action': state['action'],
            'act_params': [], 'act_param': -1, 'act_param_stage': -1
        })
        return False

    @Button(id='cancel', label='Cancel', style=ButtonStyle.danger)
    async def cancel(self, state, interaction: Interaction):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        await Menus.commandMenu.show(interaction, newState={'card': state['card'], 'card_type': state['card_type'], 'player': state['player']})
        return False
