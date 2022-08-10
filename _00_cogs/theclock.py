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
            self.need_battle = False
            self.need_harvest = True
            self.need_refresh = True


    @slash_command(name="daystart", guild_ids=guilds)
    async def day_start_c(self, ctx: Interaction):
        await self.day_start_f(ctx)

    async def day_start_f(self, ctx):
        if not self.is_day:
            await say(ctx, "Day begins, initiating protocols.")
            #for region in theJar['regions']:
                #region.channel.unmuteChannel()
            for district in theJar['districts'].keys():
                await theJar['districts'][district].channel.unmuteChannel()
            for faction in theJar['factions'].keys():
                await theJar['factions'][faction].channel.muteChannel()

            self.is_day = True
            self.need_production = True
            self.need_battle = False
            self.need_harvest = True
            self.need_refresh = True

            for unit in theJar['played_cards']['unit']:
                daybreak_report, title = await unit.triggerSkill('on_daybreak', [unit])
                pm = unit.owner.channel
                await say(ctx, daybreak_report, title=title, channel = pm)

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
            #for region in theJar['regions']:
                #region.channel.muteChannel()
            for district in theJar['districts'].keys():
                await theJar['districts'][district].channel.muteChannel()
            for faction in theJar['factions'].keys():
                await theJar['factions'][faction].channel.unmuteChannel()
        await say(ctx, "Night start protocol complete.")


    @slash_command(name="harvest", guild_ids=guilds)
    async def harvest_c(self, ctx: Interaction):
        await self.harvest_f(ctx)

    async def harvest_f(self, ctx):
        for unit in theJar['played_cards']['unit']:
            if unit.status == "Played":
                report, title = await unit.harvest()
                pm = unit.owner.channel
                if report:
                    await say(ctx, report, title=title, channel = pm)
        for building in theJar['played_cards']['building']:
            if building.status == "Played":
                report, title = await building.harvest()
                pm = building.owner.channel
                if report:
                    await say(ctx, report, title=title, channel = pm)


    @slash_command(name="refresh", guild_ids=guilds)
    async def refresh_c(self, ctx: Interaction):
        await self.refresh_f(ctx)

    async def refresh_f(self, ctx):
        for unit in theJar['played_cards']['unit']:
            if unit.status == "Played":
                report, title = await unit.refresh()
                pm = unit.owner.channel
                if report:
                    await say(ctx, report, title=title, channel = pm)
        for building in theJar['played_cards']['building']:
            if building.status == "Played":
                report, title = await building.refresh()
                pm = building.owner.channel
                if report:
                    await say(ctx, report, title=title, channel = pm)
        for player_id in theJar['players'].keys():
            player = theJar['players'][player_id]
            player.modStatCap('Influence', 1)
            player.modStat('Influence',player._statcaps['Influence']-player._stats['Influence'])
        for district_id in theJar['districts'].keys():
            district = theJar['districts'][district_id]
            if len(district.inventory.slots['unit']) or len(district.inventory.slots['building']) > 0:
                report, title = district.civics.strReport()
                dm = district.channel
                await say(ctx, report, title=title, channel = dm)


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
                report = await building.run()
                if report:
                    pm = building.owner.channel
                    print(pm)
                    await say(ctx, report, channel=pm)


def setup(bot):
    bot.add_cog(TheClock(bot))
