from code import interact
from email.message import Message
from xmlrpc.client import Boolean
from discord import TextChannel
from nextcord import Interaction
import nextcord
from _00_cogs.frontend.elements import Button
from _00_cogs.frontend.state_error import StateError
from _02_global_dicts import theJar

menus = {}

class MenuView(nextcord.ui.View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def interaction_check(self, interaction: Interaction) -> bool:
        return False

class Menu:
    def __init__(self, id: str):
        self.id = id
        menus[id] = self

        self.elements = {}

        for name, method in self.__class__.__dict__.items():
            if hasattr(method, 'is_element'):
                self.elements[method.id] = method

    async def show(self, interaction: Interaction, ephemeral=True, reply=False, newState=None):
        state = {}

        if interaction.message == None or reply:
            if newState != None:
                state = newState

            try:
                content, embeds = self.render(state)
                view = MenuView()

                for name, element in self.elements.items():
                    item = element.render(element, state)

                    if item != None:
                        item.custom_id = self.id + ':' + item.custom_id
                        view.add_item(item)
            except StateError:
                content, embeds = (':warning: State Error :warning:', [])
                view = MenuView()

            if (interaction.response.is_done()):
                newMessage = await interaction.followup.send(content=content, embeds=embeds, ephemeral=ephemeral, view=view)
                theJar['states'][newMessage.id] = state
            else:
                await interaction.response.send_message(content=content, embeds=embeds, ephemeral=ephemeral, view=view)
                newMessage = await interaction.original_message()
                theJar['states'][newMessage.id] = state
        else:
            messagid = interaction.message.id

            if newState == None and messagid in theJar['states']:
                state = theJar['states'][messagid]
            else:
                if newState != None:
                    state = newState
                theJar['states'][messagid] = state

            try:
                content, embeds = self.render(state)
                view = MenuView()

                for name, element in self.elements.items():
                    item = element.render(element, state)

                    if item != None:
                        item.custom_id = self.id + ':' + item.custom_id
                        view.add_item(item)
            except StateError:
                content, embeds = (':warning: State Error :warning:', [])
                view = MenuView()

            await interaction.edit_original_message(content=content, embeds=embeds, view=view)

    async def send(self, channel: TextChannel, state={}):
        try:
            content, embeds = self.render(state)
            view = MenuView()

            for name, element in self.elements.items():
                item = element.render(element, state)

                if item != None:
                    item.custom_id = self.id + ':' + item.custom_id
                    view.add_item(item)
        except StateError:
            content, embeds = (':warning: State Error :warning:', [])
            view = MenuView()       

        message = await channel.send(content=content, embeds=embeds, view=view)
        theJar['states'][message.id] = state

        return message

    async def update(self, message: Message, newState=None):
        messageid = message.id
        state = {}

        if newState == None and messageid in theJar['states']:
            state = theJar['states'][messageid]
        else:
            if newState != None:
                state = newState
            theJar['states'][messageid] = state

        try:
            content, embeds = self.render(state)
            view = MenuView()

            for name, element in self.elements.items():
                item = element.render(element, state)

                if item != None:
                    item.custom_id = self.id + ':' + item.custom_id
                    view.add_item(item)
        except StateError:
            content, embeds = (':warning: State Error :warning:', [])
            view = MenuView()        

        await message.edit(content=content, embeds=embeds, view=view)

    async def onInteraction(self, elementid: str, interaction: Interaction):
        if elementid in self.elements:
            messageid = interaction.message.id
            method = self.elements[elementid]
            state = {}            

            if messageid in theJar['states']:
                state = theJar['states'][messageid]
            else:
                theJar['states'][messageid] = state

            try:
                refresh = await method(self, state, interaction)
            except StateError:
                refresh = False
                content, embeds = (':warning: State Error :warning:', [])
                view = MenuView()

                await interaction.edit_original_message(content=content, embeds=embeds, view=view)

            if (refresh):
                await self.show(interaction)