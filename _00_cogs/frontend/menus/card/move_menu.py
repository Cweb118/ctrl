from discord import SelectOption
from nextcord import Interaction, ButtonStyle
from _00_cogs.frontend.elements import Button, UnlimitedSelect
from _00_cogs.frontend.state_error import StateError
from _00_cogs.frontend.menu import Menu, MenuView
from _01_functions import *
from _02_global_dicts import theJar
import _00_cogs.frontend.menus.menus as Menus

def districtOptions(state):
    if 'card' not in state or 'card_type' not in state:
        raise StateError

    if 'player' not in state or state['player'] not in theJar['players']:
        raise StateError

    player = theJar['players'][state['player']]
    card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

    if card is None:
        raise StateError

    district = card.location
    paths = district.paths

    options = []
    options.append(SelectOption(label=district.name, value=district.name))

    for path in paths:
        options.append(SelectOption(label=path.name, value=path.name))

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

        return ('Where do you want to move the ' + card.title + ' card?', [])
        
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

        await Menus.districtMoveMenu.show(interaction, newState={'card': state['card'], 'card_type': state['card_type'], 'player': state['player'], 'district': state['district']})
        return False

    @Button(id='cancel', label='Cancel', style=ButtonStyle.danger)
    async def cancel(self, state, interaction: Interaction):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        if 'district' not in state:
            raise StateError

        await Menus.commandMenu.show(interaction, newState={'card': state['card'], 'card_type': state['card_type'], 'player': state['player']})

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

    @Button(id='district', label='District', style=ButtonStyle.success)
    async def district(self, state, interaction: Interaction):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        player = theJar['players'][state['player']]
        card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

        if card is None:
            raise StateError

        district = theJar['districts'][state['district']]

        can_move, result = card.moveUnit(player, 'district', district)

        if result == '':
            result = 'Error'

        if can_move:
            await interaction.edit_original_message(content=result, view=MenuView())
        else:
            await interaction.followup.send(content=result, ephemeral=True)

        return False
    
    @Button(id='building', label='Building', style=ButtonStyle.success)
    async def building(self, state, interaction: Interaction):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        if 'district' not in state:
            raise StateError

        player = theJar['players'][state['player']] 

        await Menus.buildingMoveMenu.show(interaction, newState={'card': state['card'], 'card_type': state['card_type'], 'player': state['player'], 'district': state['district']})
        return False

    @Button(id='cancel', label='Cancel', style=ButtonStyle.danger)
    async def cancel(self, state, interaction: Interaction):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        await Menus.cardMenu.show(interaction, newState={'card': state['card'], 'card_type': state['card_type'], 'player': state['player']})
        return False

def travelOptions(state):
    if 'district' not in state or state['district'] not in theJar['districts']:
        raise StateError

    district = theJar['districts'][state['district']]
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

        if 'district' not in state or state['district'] not in theJar['districts']:
            raise StateError

        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        player = theJar['players'][state['player']]
        card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

        if card is None:
            raise StateError

        district = theJar['districts'][state['district']]
        building = district.inventory.getSlotCardByUniqueID('building', state['building'])

        if building is None:
            raise StateError

        can_move, result = card.moveUnit(player, 'building', building)

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

        if 'district' not in state:
            raise StateError

        await Menus.moveMenu.show(interaction, newState={'card': state['card'], 'card_type': state['card_type'], 'player': state['player'], 'district': state['district']})