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

class ParamMenu(Menu):
    def __init__(self, id, type_display):
        super().__init__(id)

        self.type_display = type_display

    def render(self, state):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        player = theJar['players'][state['player']]
        card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

        if card is None:
            raise StateError

        if 'action' not in state:
            raise StateError

        action = getAction(card, state['action'])

        if action is None:
            raise StateError

        if 'act_params' not in state or 'act_param' not in state or 'act_param_stage' not in state:
            raise StateError

        param_num = state['act_param']

        if len(action.act_params) <= param_num:
            raise StateError

        param_name = action.act_params[param_num][0]

        return ('Parameter: ' + param_name + '\n\n' + 'Please select ' + self.type_display)

    async def onParam(state, interaction: Interaction, param):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        player = theJar['players'][state['player']]
        card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

        if card is None:
            raise StateError

        if 'action' not in state:
            raise StateError

        action = getAction(card, state['action'])

        if action is None:
            raise StateError

        if 'act_params' not in state or 'act_param' not in state or 'act_param_stage' not in state:
            raise StateError

        params = state['act_params']
        param_num = state['act_param']
        param_stage = state['act_param_stage']

        if len(action.act_params) <= param_num:
            raise StateError

        while len(params) <= param_num:
            params.append(None)

        params[param_num] = param

        await resolveAction(interaction, {
            'card': state['card'], 'card_type': state['card_type'],
            'player': state['player'],
            'action': state['action'],
            'act_params': params, 'act_param': param_num, 'act_param_stage': param_stage
        })

    @Button(id='cancel', label='Cancel', style=ButtonStyle.danger)
    async def cancel(self, state, interaction: Interaction):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        await Menus.commandMenu.show(interaction, newState={'card': state['card'], 'card_type': state['card_type'], 'player': state['player']})
        return False