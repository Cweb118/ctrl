from nextcord import slash_command, Interaction
from nextcord.ext import commands

from _00_cogs.commands import Commands, guilds
from _00_cogs.mechanics.unit_classes.__unit_parent_class import Unit
from _00_cogs.mechanics.battle_logic import battle

from _01_functions import say
from _02_global_dicts import theJar
from _00_cogs.architecture.locations_class import District, Region

class TheClock(commands.Cog):
    def __init__(self, bot, day_status = True):
        self.bot = bot
        self.is_day = day_status
        if self.is_day:
            self.need_production = True
            self.need_battle = True
            self.need_harvest = True
            self.need_refresh = True


    @slash_command(name="daystart", guild_ids=guilds)
    async def day_start_c(self, ctx: Interaction):
        await self.day_start_f(ctx)

    async def day_start_f(self, ctx):
        if not self.is_day:
            await say(ctx, "Day begins, initiating protocols.")
            for player in theJar['players'].keys():
                #TODO: Made before the location class was changed, will need to be checked
                location_channel = theJar['channels'][player.location.channel_id]
                region_channel = theJar['channels'][player.location.region.channel_id]
                #group_channel = theJar['factions'][player.faction]

                #location_channel.permissions(player can read = yes, can chat = yes)
                #region_channel.permissions(player can read = yes, can chat = yes)
                #group_channel.permissions(player can read = yes, can chat = no)
            self.is_day = True
            self.need_production = True
            self.need_battle = True
            self.need_harvest = True
            self.need_refresh = True
        await say(ctx, "Day start protocol complete.")


    @slash_command(name="dayend", guild_ids=guilds)
    async def day_end_c(self, ctx: Interaction):
        await self.day_end_f(ctx)

    async def day_end_f(self, ctx):
        if self.is_day:
            await say(ctx, "Day end, initiating protocols.")
        if self.need_production:
            await self.produce_f(ctx)
            await say(ctx, "Production Complete.")
            self.need_production = False
        if self.need_battle:
            await self.battle_f(ctx)
            await say(ctx, "Combat Complete.")
            self.need_battle = False
        if self.need_harvest:
            await self.harvest_f(ctx)
            await say(ctx, "Harvest Complete.")
            self.need_harvest = False
        if self.need_refresh:
            await self.refresh_f(ctx)
            await say(ctx, "Refresh Complete.")
            self.need_refresh = False
        self.is_day = False
        await say(ctx, "Day end protocol complete.")
        await self.night_start_f(ctx)


    @slash_command(name="nightstart", guild_ids=guilds)
    async def night_start_c(self, ctx: Interaction):
        await self.night_start_f(ctx)

    async def night_start_f(self, ctx):
        if not self.is_day:
            await say(ctx, "Night begins, initiating protocols.")
            for player in theJar['players'].keys():
                #TODO: Made before the location class was changed, will need to be checked
                location_channel = theJar['channels'][player.location.channel_id]
                region_channel = theJar['channels'][player.location.region.channel_id]
                #group_channel = theJar['factions'][player.faction]

                #location_channel.permissions(player can read = yes, can chat = no)
                #region_channel.permissions(player can read = yes, can chat = no)
                #group_channel.permissions(player can read = yes, can chat = yes)
        await say(ctx, "Night start protocol complete.")


    @slash_command(name="harvest", guild_ids=guilds)
    async def harvest_c(self, ctx: Interaction):
        await self.harvest_f(ctx)

    async def harvest_f(self, ctx):
        for unit in theJar['units']:
            if unit.status == "Played":
                report, title = unit.harvest()
                #send to players private channel instead (as cn)
                await say(ctx, report, title=title)


    @slash_command(name="refresh", guild_ids=guilds)
    async def refresh_c(self, ctx: Interaction):
        await self.refresh_f(ctx)

    async def refresh_f(self, ctx):
        for unit in theJar['units']:
            if unit.status == "Played":
                report, title = unit.refresh()
                #send to players private channel instead (as cn)
                await say(ctx, report, title=title)
        for player_id in theJar['players'].keys():
            player = theJar['players'][player_id]
            player.modStatCap(theJar['resources']['Influence'], 1)


    @slash_command(name="battle", guild_ids=guilds)
    async def battle_c(self, ctx: Interaction):
        await self.battle_f(ctx)

    async def battle_f(self, ctx):
        for loc_name in theJar['districts'].keys():
            location = theJar['districts']['loc_name']
            await battle(ctx, location)


    @slash_command(name="produce", guild_ids=guilds)
    async def produce_c(self, ctx: Interaction):
        await self.produce_f(ctx)

    async def produce_f(self, ctx):
        wave_ints = []
        for building in theJar['played_cards']['building']:
            priority = building.priority
            if priority not in wave_ints:
                wave_ints.append(priority)
        wave_ints = sorted(wave_ints, reverse=True)

        waves = {}
        for num in wave_ints:
            wave = []
            for building in theJar['played_cards']['building']:
                if building.priority == num:
                    wave.append(building)
            waves[num] = wave

        for num in wave_ints:
            for building in waves[num]:
                report = building.run()
                if report:
                    await say(ctx,report)


def setup(bot):
    bot.add_cog(TheClock(bot))
