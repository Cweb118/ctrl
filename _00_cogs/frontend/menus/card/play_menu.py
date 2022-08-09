from discord import SelectOption
from nextcord import Interaction, ButtonStyle
from _00_cogs.frontend.elements import Button, UnlimitedSelect
from _00_cogs.frontend.state_error import StateError
from _00_cogs.frontend.menu import Menu, MenuView
from _01_functions import *
from _02_global_dicts import theJar
import _00_cogs.frontend.menus.menus as Menus

class PlayMenu(Menu):
    def __init__(self):
        super().__init__('playmenu')

    def render(self, state):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        player = theJar['players'][state['player']]
        card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

        if card is None:
            raise StateError

        return ('Where do you want to play the ' + card.title + ' card?', [])

    @Button(id='district', label='Current District', style=ButtonStyle.success)
    async def district(self, state, interaction: Interaction):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        player = theJar['players'][state['player']]
        card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

        if card is None:
            raise StateError

        can_play, result = await card.playCard(player, theJar['districts'][player.location])

        if result == '':
            result = 'Error'

        if can_play:
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

        player = theJar['players'][state['player']] 

        await Menus.buildingPlayMenu.show(interaction, newState={'card': state['card'], 'card_type': state['card_type'], 'player': state['player'], 'district': player.location})
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

class BuildingPlayMenu(Menu):
    def __init__(self):
        super().__init__('buildingplaymenu')

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

        can_play, result = await card.playCard(player, building)

        if result == '':
            result = 'Error'

        if can_play:
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

        await Menus.playMenu.show(interaction, newState={'card': state['card'], 'card_type': state['card_type'], 'player': state['player']})
