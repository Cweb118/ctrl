import asyncio
from code import interact
from nextcord import Interaction, InteractionType
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import os
import nextcord
import time
import datetime
from _00_cogs.architecture.player_class import Player
from keys import prime_token, prefix
from nextcord.ext import commands
from _00_cogs.frontend.menu import menus
from _00_cogs.frontend.modal import modals
from _02_global_dicts import theJar

intents = nextcord.Intents.all()
client = nextcord.Client(intents=intents)
bot = commands.Bot(command_prefix=prefix, intents=intents)

cogsDir = os.path.join(os.path.dirname(__file__), "_00_cogs")

loadedCogs = []
 
#reload method for FileWatcher
def reloadFW(extension):
    try:
        try:
            bot.unload_extension(f'_00_cogs.{extension[:-3]}')
            bot.load_extension(f'_00_cogs.{extension[:-3]}')
            print(f'Reloaded cog {extension} automatically due to modification.')

        except:
            bot.load_extension(f'_00_cogs.{extension[:-3]}')
            print(f'Reloaded cog {extension} automatically due to modification.')

    except Exception as e:
        print("Automatic Reload Error.")
        print(str(e))

class FileWatch(FileSystemEventHandler):
    def __init__(self):
        self.lastReload = -1

    def on_modified(self, event):
        filename = event.src_path.split("\\")
        filename = filename[len(filename)-1]

        if(time.time() - self.lastReload > 1):
            for file in loadedCogs:
                if(filename == file and event.is_directory == False):
                    reloadFW(filename)
                    self.lastReload = time.time()

@bot.command(name='loaded')
@commands.has_role('control')
async def loaded(ctx):
    cogs = ""
    for cog in loadedCogs:
        cogs = cogs + f"{cog}\n"
    await ctx.send(cogs)


@bot.command(name='loadext')
@commands.has_role('control')
async def load(ctx, extension):
    global loadedCogs

    try:
        bot.load_extension(f'_00_cogs.{extension}')
        loadedCogs.append(extension)
        await ctx.send(f'Loaded cog {extension}')
    except:
        await ctx.send("Extension not found.")

@bot.command(name='unloadext')
@commands.has_role('control')
async def unload(ctx, extension):
    global loadedCogs

    try:
        bot.unload_extension(f'_00_cogs.{extension}')
        loadedCogs.remove(str(extension)+".py")
        await ctx.send(f'Unloaded cog {extension}')
    except Exception as e:
        await ctx.send("Extension not found.")
        print(e)

@bot.event
async def on_ready():
    theJar['client'] = bot.user.id
    print('Bot is ready at: ' + str(datetime.datetime.now()))

@bot.event
async def on_interaction(interaction: Interaction):
    if interaction.type == InteractionType.component:
        id = interaction.data['custom_id']
        (menuid, elementid) = id.split(':')

        if menuid in menus:
            menu = menus[menuid]
            
            if menu.shouldDefer(elementid, interaction):
                await interaction.response.defer()

            await menu.onInteraction(elementid, interaction)
    elif interaction.type == InteractionType.modal_submit:
        id = interaction.date['custom_id']

        if id in modals:
            modal = modals[id]
            await interaction.response.defer()
            await modal.onSubmit(interaction)

    else:
        await bot.process_application_commands(interaction) 

    allInterfaceUpdates = []

    for id, player in theJar['players'].items():
        if player.interfaceDirty:
            allInterfaceUpdates.append(player.doInterfaceUpdate())

    for id, district in theJar['districts'].items():
        if district.interfaceDirty:
            allInterfaceUpdates.append(district.doInterfaceUpdate())

    await asyncio.gather(*allInterfaceUpdates)

handler = FileWatch()
observer = Observer()
observer.schedule(handler, path=cogsDir, recursive=False)
observer.start()

for filename in os.listdir(cogsDir):
    if filename.endswith('.py'):
        bot.load_extension(f'_00_cogs.{filename[:-3]}')
        loadedCogs.append(filename)
        print(f'Loaded cog {filename}')

bot.run(prime_token)
