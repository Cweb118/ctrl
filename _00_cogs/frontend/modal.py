from code import interact
from email.message import Message
from xmlrpc.client import Boolean
from discord import TextChannel
from nextcord import Interaction
import nextcord
from _00_cogs.frontend.elements import Button
from _00_cogs.frontend.state_error import StateError
from _02_global_dicts import theJar

modals = {}

class MenuModal(nextcord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Modal:
    def __init__(self, id: str, name: str):
        self.id = id
        modals[id] = self

        self.name = name

        self.elements = {}

        for methodName, method in self.__class__.__dict__.items():
            if hasattr(method, 'is_element'):
                self.elements[method.id] = method

    async def show(self, interaction: Interaction, state):
        modal = MenuModal(self.name)
        modal.custom_id = self.id + ':' + str(interaction.id)

        for name, element in self.elements.items():
            item = element.render(element)
            modal.add_item(item)

        theJar['modalStates'][str(interaction.id)] = state
        await interaction.response.send_modal(modal)

    async def handleSubmit(self, stateid: str, interaction: Interaction):
        state = {}       

        if stateid in theJar['modalStates']:
            state = theJar['modalStates'][stateid]
        else:
            theJar['modalStates'][stateid] = state

        components = interaction.data['components'][0]['components']
        values = {}

        for component in components:
            id = component['custom_id']
            value = component['value']

            values[id] = value

        try:
            await self.onSubmit(state, values, interaction)
        except StateError:
            pass                