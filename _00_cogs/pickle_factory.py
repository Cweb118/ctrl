from importlib.metadata import files
from stat import ST_CTIME
from nextcord import slash_command
from nextcord.ext import commands
from numpy import equal
from _02_global_dicts import theJar
import pickle
import shutil
from datetime import datetime, timezone, timedelta
import time
import os

class PickleFactory(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        #make path for pickle jar
        if not os.path.isdir(f"{os.getcwd()}\\_01_pickle_jar\\"):
            os.makedirs(f"{os.getcwd()}\\_01_pickle_jar\\")
        
        #make path for backups
        if not os.path.isdir(f"{os.getcwd()}\\_01_pickle_jar\\backups"):
            os.makedirs(f"{os.getcwd()}\\_01_pickle_jar\\backups")
    
    def autosave():
        BACKUP_FREQUENCY = 5 #in minutes
        LATEST_SAVE = f"{os.getcwd()}\\_01_pickle_jar\\latest.pkl"
        BACKUP_DIR = f"{os.getcwd()}\\_01_pickle_jar\\backups"

        with open(LATEST_SAVE, "wb") as file:
            pickle.dump(theJar, file)
        
        #Automatic Backup.
        files = os.scandir(BACKUP_DIR)
        date = datetime.now().strftime('%m-%d-%y %H-%M')

        if len(os.listdir(BACKUP_DIR)) == 0:
            shutil.copyfile(LATEST_SAVE, f'{BACKUP_DIR}\\{date}.pkl')
        else:
            latest = max(files, key=os.path.getctime)
            if time.time() - latest.stat().st_ctime > (BACKUP_FREQUENCY*60):
                shutil.copyfile(LATEST_SAVE, f'{BACKUP_DIR}\\{date}.pkl')


    @commands.command(name='save')
    async def save(self, ctx):
        with open(f"{os.getcwd()}\\_01_pickle_jar\\latest.pkl", "wb") as file:
            pickle.dump(theJar, file)
        await ctx.send("Saved!")

    @commands.command(name='load')
    async def load(self, ctx):
        with open(f"{os.getcwd()}\\_01_pickle_jar\\theJar.pkl", "rb") as file:
            loadJar = pickle.load(file)
            for entry in loadJar.keys():
                    if entry == "districts":
                        for district in loadJar['districts'].values():
                            district.reconstruct(self.bot)
                    elif entry == "regions":
                        for region in loadJar['regions'].values():
                            region.reconstruct(self.bot)
                    elif entry == 'players':
                        for player in loadJar['players'].values():
                            player.reconstruct(self.bot)
                    elif entry == 'factions':
                        for faction in loadJar['factions'].values():
                            faction.reconstruct(self.bot)
            loadJar['control']['explore-log'].reconstruct(self.bot.get_guild(778448646642728991))
            for entry in loadJar.keys():
                theJar[entry] = loadJar[entry]
        await ctx.send("Loaded!")

def setup(bot):
    bot.add_cog(PickleFactory(bot))
