import operator
from _02_global_dicts import theJar
import nextcord
import time, asyncio
from nextcord.ext import tasks
from _00_cogs.architecture.inventory_class import Inventory
import _00_cogs.frontend.menus.menus as Menus

class Channel():
    #on instantiation, create channel or check if it already exists.
    def __init__(self, guild, channel_name, category_name = None, VC_Mode = False, can_talk = True):
        self.name = channel_name.replace(' ', '-').lower()
        self.category_name = category_name
        self.guild = guild
        self.VC_Mode = VC_Mode
        self.can_talk = can_talk
        self.channel = nextcord.utils.get(self.guild.text_channels, name=self.name)
        self.VC_channel = nextcord.utils.get(self.guild.voice_channels, name=self.name)
        

    async def init(self):
        if self.channel and (self.VC_channel or not self.VC_Mode):
            return self

        overwrites = {
                self.guild.default_role: nextcord.PermissionOverwrite(read_messages=False, send_messages=self.can_talk, connect=False, speak=self.can_talk),
            }
        if self.category_name:
            category = nextcord.utils.get(self.guild.categories, name=self.category_name)
            if category:
                self.channel = await category.create_text_channel(self.name, overwrites=overwrites)
                if self.VC_Mode:
                    self.VC_channel = await category.create_voice_channel(self.name, overwrites=overwrites)
        else:
            self.channel = await self.guild.create_text_channel(self.name, overwrites=overwrites)
            if self.VC_Mode:
                self.VC_channel = await self.guild.create_voice_channel(self.name, overwrites=overwrites)

        return self

    async def delete(self):
        await self.channel.delete()
        if self.VC_channel:
            await self.VC_channel.delete()
    
    async def addPlayer(self, user):
        await self.channel.set_permissions(user, read_messages=True, send_messages=self.can_talk)
        if self.VC_channel:
            await self.VC_channel.set_permissions(user, connect=True, speak=self.can_talk)

    async def removePlayer(self, user):
        await self.channel.set_permissions(user, read_messages=False)
        if self.VC_channel:
            await self.VC_channel.set_permissions(user, connect=False)