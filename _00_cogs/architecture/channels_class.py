import operator
from _02_global_dicts import theJar
import nextcord
import time, asyncio
from nextcord.ext import tasks
from _00_cogs.architecture.inventory_class import Inventory
import _00_cogs.frontend.menus.menus as Menus

class Channel():
    def __init__(self, channel_name, channel_id, guild = None, guildID = None):
        self.name = channel_name
        self.id = channel_id

