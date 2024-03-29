from discord import SelectOption
from nextcord import Interaction, ButtonStyle
from _00_cogs.frontend.elements import Button, UnlimitedSelect
from _00_cogs.frontend.state_error import StateError
from _00_cogs.frontend.menu import Menu, MenuView
from _01_functions import *
from _02_global_dicts import theJar
import _00_cogs.frontend.menus.menus as Menus

def inBuilding(state):
    if 'card' not in state or 'card_type' not in state:
        raise StateError

    if 'player' not in state or state['player'] not in theJar['players']:
        raise StateError

    player = theJar['players'][state['player']]
    card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

    if card is None:
        raise StateError

    return card.district != card.location

class MoveMenu(Menu):
    def __init__(self):
        super().__init__('movemenu')

    def render(self, state):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        player = theJar['players'][state['player']]
        card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

        if card is None:
            raise StateError

        return ('Where do you want to move the ' + card.title + ' card?', [])

    @Button(id='current_district', label='Current District', style=ButtonStyle.success, includeFun=inBuilding)
    async def current_district(self, state, interaction: Interaction):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        player = theJar['players'][state['player']]
        card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

        if card is None:
            raise StateError

        district = card.district

        can_move, result = await card.moveUnit('district', district)

        if result == '':
            result = 'Error'

        if can_move:
            await interaction.edit_original_message(content=result, view=MenuView())
        else:
            await interaction.followup.send(content=result, ephemeral=True)

        return False

    @Button(id='district', label='Adjacent District', style=ButtonStyle.success, includeFun=lambda state: not inBuilding(state))
    async def district(self, state, interaction: Interaction):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        player = theJar['players'][state['player']]
        card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

        if card is None:
            raise StateError
        
        await Menus.districtMoveMenu.show(interaction, newState={'card': state['card'], 'card_type': state['card_type'], 'player': state['player']})
        return False
    
    @Button(id='building', label='Local Building', style=ButtonStyle.success)
    async def building(self, state, interaction: Interaction):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        await Menus.buildingMoveMenu.show(interaction, newState={'card': state['card'], 'card_type': state['card_type'], 'player': state['player']})
        return False

    @Button(id='cancel', label='Cancel', style=ButtonStyle.danger)
    async def cancel(self, state, interaction: Interaction):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        await Menus.commandMenu.show(interaction, newState={'card': state['card'], 'card_type': state['card_type'], 'player': state['player']})
        return False

def districtOptions(state):
    if 'card' not in state or 'card_type' not in state:
        raise StateError

    if 'player' not in state or state['player'] not in theJar['players']:
        raise StateError

    player = theJar['players'][state['player']]
    card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

    if card is None:
        raise StateError

    district = card.district
    paths = district.paths

    options = []

    for path in paths:
        options.append(SelectOption(label=path, value=path))

    return options

class DistrictMoveMenu(Menu):
    def __init__(self):
        super().__init__('districtmove')

    def render(self, state):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        player = theJar['players'][state['player']]
        card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

        if card is None:
            raise StateError

        return ('To what district do you want to move the ' + card.title + ' card?', [])
        
    @UnlimitedSelect(id='district', optionsFun=districtOptions)
    async def district(self, state, interaction: Interaction):
        state['district'] = interaction.data['values'][0]
        return False

    @Button(id='confirm', label='Confirm', style=ButtonStyle.success)
    async def confirm(self, state, interaction: Interaction):
        if 'district' not in state:
            return False

        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        player = theJar['players'][state['player']]
        card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

        if card is None:
            raise StateError

        district = theJar['districts'][state['district']]

        can_move, result = await card.moveUnit('district', district)

        if result == '':
            result = 'Error'

        if can_move:
            await interaction.edit_original_message(content=result, view=MenuView())
        else:
            await interaction.followup.send(content=result, ephemeral=True)

        return False

    @Button(id='cancel', label='Cancel', style=ButtonStyle.danger)
    async def cancel(self, state, interaction: Interaction):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        await Menus.moveMenu.show(interaction, newState={'card': state['card'], 'card_type': state['card_type'], 'player': state['player']})

def travelOptions(state):
    if 'card' not in state or 'card_type' not in state:
        raise StateError

    if 'player' not in state or state['player'] not in theJar['players']:
        raise StateError

    player = theJar['players'][state['player']]
    card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

    if card is None:
        raise StateError

    district = card.district
    buildings = district.inventory.slots['building']

    options = []

    for building in buildings:
        options.append(SelectOption(label=building.title, value=building.uniqueID))

    return options

class BuildingMoveMenu(Menu):
    def __init__(self):
        super().__init__('buildingmove')

    def render(self, state):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        player = theJar['players'][state['player']]
        card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

        if card is None:
            raise StateError

        return ('In which building do you want to play the ' + card.title + ' card?', [])
        
    @UnlimitedSelect(id='building', optionsFun=travelOptions)
    async def building(self, state, interaction: Interaction):
        state['building'] = interaction.data['values'][0]
        return False

    @Button(id='confirm', label='Confirm', style=ButtonStyle.success)
    async def confirm(self, state, interaction: Interaction):
        if 'building' not in state:
            return False

        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        player = theJar['players'][state['player']]
        card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

        if card is None:
            raise StateError

        district = card.district
        building = district.inventory.getSlotCardByUniqueID('building', state['building'])

        if building is None:
            raise StateError

        can_move, result = await card.moveUnit('building', building)

        if result == '':
            result = 'Error'

        if can_move:
            await interaction.edit_original_message(content=result, view=MenuView())
        else:
            await interaction.followup.send(content=result, ephemeral=True)

        return False

    @Button(id='cancel', label='Cancel', style=ButtonStyle.danger)
    async def cancel(self, state, interaction: Interaction):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        await Menus.moveMenu.show(interaction, newState={'card': state['card'], 'card_type': state['card_type'], 'player': state['player']})
