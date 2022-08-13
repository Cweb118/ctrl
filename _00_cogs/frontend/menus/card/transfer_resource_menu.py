from discord import SelectOption
from nextcord import Interaction, ButtonStyle
from _00_cogs.frontend.elements import Button, UnlimitedSelect
from _00_cogs.frontend.state_error import StateError
from _00_cogs.frontend.menu import Menu, MenuView
from _01_functions import *
from _02_global_dicts import theJar
import _00_cogs.frontend.menus.menus as Menus
import _00_cogs.frontend.modals.modals as Modals

def getSrcAndDest(state):
    srcInv = None
    srcName = ''

    if state['src_type'] == 'card':
        if 'src_card' not in state or 'src_card_type' not in state:
            raise StateError

        if 'src_player' not in state or state['src_player'] not in theJar['players']:
            raise StateError

        srcPlayer = theJar['players'][state['src_player']]
        srcCard = srcPlayer.inventory.getCardByUniqueID(state['src_card_type'], state['src_card'])

        srcInv = srcCard.inventory
        srcName = srcCard.title + "'s"
    elif state['src_type'] == 'player':
        if 'src_player' not in state or state['src_player'] not in theJar['players']:
            raise StateError

        srcPlayer = theJar['players'][state['src_player']]
        
        srcInv = srcPlayer.inventory
        srcName = 'your'
    elif state['src_type'] == 'district':
        if 'src_district' not in state or state['src_district'] not in theJar['districts']:
            raise StateError

        srcDistrict = theJar['districts'][state['src_district']]

        srcInv = srcDistrict.inventory
        srcName = srcDistrict.name + "'s"
    else:
        raise StateError

    destInv = None
    destName = ''

    if state['dest_type'] == 'card':
        if 'dest_card' not in state or 'dest_card_type' not in state:
            raise StateError

        if 'dest_player' not in state or state['dest_player'] not in theJar['players']:
            raise StateError

        destPlayer = theJar['players'][state['dest_player']]
        destCard = destPlayer.inventory.getCardByUniqueID(state['dest_card_type'], state['dest_card'])

        destInv = destCard.inventory
        destName = destCard.title + "'s"
    elif state['dest_type'] == 'player':
        if 'dest_player' not in state or state['dest_player'] not in theJar['players']:
            raise StateError

        destPlayer = theJar['players'][state['dest_player']]

        destInv = destPlayer.inventory
        destName = 'your'
    elif state['dest_type'] == 'district':
        if 'dest_district' not in state or state['dest_district'] not in theJar['districts']:
            raise StateError

        destDistrict = theJar['districts'][state['dest_district']]

        destInv = destDistrict.inventory
        destName = destDistrict.name + "'s"
    else:
        raise StateError

    return (srcInv, srcName), (destInv, destName)

def resourceOptions(state):
    src, dest = getSrcAndDest(state)

    srcInv, srcName = src
    destInv, destName = dest

    options = []

    for resource, quantity in srcInv.resources.items():
        if quantity > 0 and destInv.canAddMath(resource, 1):
            #default = 'resource' in state and state['resource'] in theJar['resources'] and theJar['resources'][state['resource']] == resource
            name = resource
            default = 'resource' in state and state['resource'] == resource

            options.append(SelectOption(label=name, value=name, default=default))

    return options

def quantityOptions(state):
    if 'resource' not in state or state['resource'] not in theJar['resources']:
        raise StateError

    resource = state['resource']

    src, dest = getSrcAndDest(state)

    srcInv, srcName = src
    destInv, destName = dest

    if resource not in srcInv.resources:
        raise StateError

    quantity = srcInv.resources[resource]

    options = []

    for i in range(quantity):
        num = i + 1

        if destInv.canAddMath(resource, num):
            options.append(SelectOption(label=num, value=num))

    return options

def quantityInclude(state):
    if 'resource' not in state or state['resource'] not in theJar['resources']:
        return False

    return True

class TransferResourceMenu(Menu):
    def __init__(self):
        super().__init__('transferitemmenu')

    def render(self, state):
        if 'src_type' not in state or 'dest_type' not in state:
            raise StateError

        src, dest = getSrcAndDest(state)

        srcInv, srcName = src
        destInv, destName = dest

        return ('What resource and how many do you want to move from ' + srcName + ' inventory to ' + destName + ' inventory?', [])

    @UnlimitedSelect(id='resource', optionsFun=resourceOptions)
    async def resource(self, state, interaction: Interaction):
        state['resource'] = interaction.data['values'][0]
        
        if 'quantity' in state:
            del state['quantity']
            
        return True

    @UnlimitedSelect(id='quantity', optionsFun=quantityOptions, includeFun=quantityInclude)
    async def quantity(self, state, interaction: Interaction):
        state['quantity'] = int(interaction.data['values'][0])
        return False

    @Button(id='confirm', label='Confirm', style=ButtonStyle.success)
    async def confirm(self, state, interaction: Interaction):
        if 'resource' not in state or state['resource'] not in theJar['resources']:
            return False

        if 'quantity' not in state:
            return False

        resource = state['resource']
        quantity = state['quantity']

        src, dest = getSrcAndDest(state)

        srcInv, srcName = src
        destInv, destName = dest

        report = srcInv.giveres(resource, quantity, destInv.inv_owner)
        await interaction.edit_original_message(content=report, view=MenuView())

        return False