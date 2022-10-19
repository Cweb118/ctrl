import operator
from _02_global_dicts import theJar
import nextcord
import time, asyncio
from _00_cogs.architecture.inventory_class import Inventory
import _00_cogs.frontend.menus.menus as Menus
from _00_cogs.sudo import sudo_profiles

class Channel():
    #on instantiation, create channel or check if it already exists.
    def __init__(self, guild, channel_name, category_name = None, VC_Mode = True, can_talk = True, has_webhook = True):
        self.name = channel_name.replace(' ', '-').lower()
        self.category_name = category_name
        self.guild = guild
        self.VC_Mode = VC_Mode
        self.can_talk = can_talk
        self.has_webhook = has_webhook
        self.channel = nextcord.utils.get(self.guild.text_channels, name=self.name)
        self.VC_channel = nextcord.utils.get(self.guild.voice_channels, name=self.name)
        self.webhook = None
        

    async def init(self):
        control_role = nextcord.utils.get(self.guild.roles, name="control")
        overwrites = {
            self.guild.default_role: nextcord.PermissionOverwrite(read_messages=False, send_messages=self.can_talk, connect=False, speak=self.can_talk),
            control_role: nextcord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True, speak=True),
        }

        channel_parent = None
        if self.category_name:
            channel_parent = nextcord.utils.get(self.guild.categories, name=self.category_name)
        else:
            channel_parent = self.guild

        if channel_parent:
            if self.channel is None:
                self.channel = await channel_parent.create_text_channel(self.name, overwrites=overwrites)

            if self.VC_Mode and self.VC_channel is None:
                self.VC_channel = await channel_parent.create_voice_channel(self.name, overwrites=overwrites)

            if self.has_webhook:
                if self.webhook is None:
                    self.webhook = nextcord.utils.get(await self.channel.webhooks(), name=self.name)

                if self.webhook is None:
                    self.webhook = await self.channel.create_webhook(name=self.name)

        return self

    def __getstate__(self):
        if (self.guild == None or self.channel == None):
            print('Has none: ' + self.name)
            print(self.guild)
            print(self.channel)

        state = (self.name, self.category_name, self.guild.id, self.VC_Mode, self.can_talk, self.has_webhook, self.channel.id)

        if self.VC_channel is not None:
            state += (self.VC_channel.id,)
        else:
            state += (self.VC_channel,)

        return state
    
    def __setstate__(self, state):
        self.name, self.category_name, self.guild, self.VC_Mode, self.can_talk, self.has_webhook, self.channel, self.VC_channel = state
        
    def reconstruct(self, guild):
        self.guild = guild
        self.channel = nextcord.utils.get(self.guild.text_channels, id=self.channel)
        self.VC_channel = nextcord.utils.get(self.guild.voice_channels, id=self.VC_channel)

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

    async def muteChannel(self):
        control_role = nextcord.utils.get(self.guild.roles, name="control")
        await self.channel.set_permissions(self.guild.default_role, read_messages=False, send_messages=False)
        if self.VC_channel:
            await self.VC_channel.set_permissions(self.guild.default_role, connect=False, speak=False)

    async def unmuteChannel(self):
        await self.channel.set_permissions(self.guild.default_role, read_messages=False, send_messages=self.can_talk)
        if self.VC_channel:
            await self.VC_channel.set_permissions(self.guild.default_role, connect=False, speak=self.can_talk)

    async def send(self, embed=None):
        await self.channel.send(embed=embed)

    async def sudoSend(self, message, embed=None, profile='cn'):
        if not self.webhook:
            return

        await self.webhook.send(message, embed=embed, username=sudo_profiles[profile]["name"], avatar_url=sudo_profiles[profile]["pfp"])
