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

def cardOptions(card_type):
    def optionsFun(state):
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

        filter = lambda x: True

        if len(action.act_params[param_num][param_stage + 1]) > 1:
            filter = action.act_params[param_num][param_stage + 1][1]

        if 'cert_filter' in state:
            filter = lambda card: card.hasCert(state['cert_filter'])

        if len(params) <= param_num:
            raise StateError

        district_id = params[param_num]

        if district_id not in theJar['districts']:
            raise StateError

        district = theJar['districts'][district_id]
        cards = district.inventory.slots[card_type]

        options = []

        for card in cards:
            if filter(card):
                options.append(SelectOption(label=card.title, value=str(card.owner.memberID) + '|' + str(card.uniqueID)))

        return options

    return optionsFun

class UnitParamMenu(ParamMenu):
    def __init__(self):
        super().__init__('unitparammenu', 'a unit')

    @UnlimitedSelect(id='card', optionsFun=cardOptions('unit'))
    async def card(self, state, interaction: Interaction):
        await self.onParam(state, interaction, interaction.data['values'][0])

class BuildingParamMenu(ParamMenu):
    def __init__(self):
        super().__init__('buildingparammenu', 'a building')

    @UnlimitedSelect(id='card', optionsFun=cardOptions('building'))
    async def card(self, state, interaction: Interaction):
        await self.onParam(state, interaction, interaction.data['values'][0])