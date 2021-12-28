from watchdog.events import FileSystemEventHandler  
from watchdog.observers import Observer
import os
import nextcord
import time
from keys import prime_token
from nextcord.ext import commands

intents = nextcord.Intents.all()
client = nextcord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

cogsDir = ".\\_00_cogs\\"

loadedCogs = []

#reload method for FileWatcher
def reloadFW(extension):
    try:
        try:
            bot.unload_extension(f'cogs.{extension[:-3]}')
            bot.load_extension(f'cogs.{extension[:-3]}')
            print(f'Reloaded cog {extension} automatically due to modification.')

        except:
            bot.load_extension(f'cogs.{extension[:-3]}')
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

@bot.command(name='load')
@commands.has_role('control')
async def load(ctx, extension):
    try:
        bot.load_extension(f'_00_cogs.{extension}')
        loadedCogs.append(extension)
        await ctx.send(f'Loaded cog {extension}')
    except:
        await ctx.send("Extension not found.")

@bot.command(name='unload')
@commands.has_role('control')
async def unload(ctx, extension):
    try:
        bot.unload_extension(f'_00_cogs.{extension}')
        loadedCogs.remove(extension)
        await ctx.send(f'Unloaded cog {extension}')
    except:
        await ctx.send("Extension not found.")


handler = FileWatch()
observer = Observer()
observer.schedule(handler, path=cogsDir, recursive=False)
observer.start()

for filename in os.listdir(cogsDir):
    if filename.endswith('.py'):
        print(filename)
        bot.load_extension(f'_00_cogs.{filename[:-3]}')
        loadedCogs.append(filename)
        print(f'Loaded cog {filename}')

bot.run(prime_token)