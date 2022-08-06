from discord import SelectOption
from nextcord import Interaction, ButtonStyle
from _00_cogs.frontend.elements import Button, UnlimitedSelect
from _00_cogs.frontend.menus.card.actions.action import getAction, resolveAction
from _00_cogs.frontend.menus.card.actions.param_menu import ParamMenu
from _00_cogs.frontend.state_error import StateError
from _00_cogs.frontend.menu import Menu, MenuView
from _01_functions import *
from _02_global_dicts import theJar
import _00_cogs.frontend.menus.menus as Menus
import _00_cogs.frontend.modals.modals as Modals

def selectOptions(state):
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

    if len(action.act_params[param_num]) <= param_stage + 1:
        raise StateError

    raw_options = action.act_params[param_num][param_stage + 1][1]
    options = []

    for raw_opt_value, raw_opt_label in raw_options:
        options.append(SelectOption(label=raw_opt_label, value=raw_opt_value))

    return options

class SelectParamMenu(ParamMenu):
    def __init__(self):
        super().__init__('selectparammenu', 'an option')

    @UnlimitedSelect(id='select', optionsFun=selectOptions)
    async def select(self, state, interaction: Interaction):
        await self.onParam(state, interaction, interaction.data['values'][0])