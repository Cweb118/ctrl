import asyncio
from _01_functions import say

async def battle(ctx, location_obj):
    defense_buildings = location_obj.inventory.slots['building']
    attack_units = location_obj.inventory.slots['unit']

    defense_units = []
    for building in defense_buildings:
        if 'Defense' in building.trait_list:
            for unit in building.inventory.slots['unit']:
                defense_units.append(unit)

    attack_units = sort_targets(attack_units)
    defense_units = sort_targets(defense_units)
    wave_ints = sort_inititative(attack_units+defense_units)
    attack_units_waves = sort_waves(attack_units, wave_ints)
    defense_units_waves = sort_waves(defense_units, wave_ints)

    i = 1
    cont = True
    while cont:
        cont, final_strike = await round(ctx, i, attack_units_waves, defense_units_waves, attack_units, defense_units)
        await battle_report(ctx, attack_units, defense_units)
        await asyncio.sleep(10)
        i += 1

    if final_strike:
        await say(ctx, "-----Final Strike-----")
        for attack_wave in attack_units_waves:
            await wave(ctx, attack_wave, defense_buildings)
    await say(ctx, "----End of Battle----")


async def round(ctx, rn, attack_units_waves, defense_units_waves, attack_units_targets, defense_units_targets):
    i = 0
    while i < len(attack_units_waves) or i < len(defense_units_waves):
        await say(ctx, "--------Round "+str(rn)+" | Wave "+str(i+1)+"--------")
        if len(attack_units_waves[i]) > 0:
            if alive_check(attack_units_waves[i]):
                await say(ctx, "--------Attackers--------")
                await wave(ctx, attack_units_waves[i], defense_units_targets)

        if len(defense_units_waves[i]) > 0:
            if alive_check(defense_units_waves[i]):
                await say(ctx, "--------Defenders--------")
                await wave(ctx, defense_units_waves[i], attack_units_targets)
        i += 1
    if alive_check(attack_units_targets) and alive_check(defense_units_targets):
        cont = True
    else:
        cont = False
    return cont, alive_check(attack_units_targets)


async def wave(ctx, attackers, defenders):
    for att_unit in attackers:
        if att_unit.status == 'Played':
            i = 0
            def_unit = None
            while i < len(defenders):
                def_unit = defenders[i]
                if def_unit.status == 'Played':
                    break
                else:
                    def_unit = None
                    i += 1
            if def_unit:
                await fight(ctx, att_unit, def_unit)
                await asyncio.sleep(4)
            else:
                report = str(att_unit) +" has no opposing units to attack."
                await say(ctx, report)


async def fight(ctx, attack_unit, defense_unit):
    att_att = attack_unit.stats['Attack']

    report = "------ATTACK------\n\n"+str(attack_unit)+" has attacked "+str(defense_unit)+" for "+str(att_att)+" damage."

    if defense_unit.traits:
        if len(defense_unit.traits['on_defend']) > 0:
            for trait in defense_unit.traits['on_defend']:
                action_report = trait.action.defend(defense_unit, attack_unit, att_att)
                if action_report:
                    report += action_report

    health_rep = defense_unit.dmg(att_att)
    report += "\n"+health_rep

    if len(attack_unit.traits['on_attack']) > 0:
        for trait in attack_unit.traits['on_attack']:
            action_report = trait.action.attack(attack_unit, defense_unit)
            if action_report:
                report += action_report



    await say(ctx, report)

def sort_inititative(all_units):
    wave_ints = []
    for unit in all_units:
        initiative = unit.initiative
        if initiative not in wave_ints:
            wave_ints.append(initiative)
    wave_ints = sorted(wave_ints)
    return wave_ints

def sort_waves(unit_list, wave_ints):
    waves = []
    for num in wave_ints:
        wave = []
        for unit in unit_list:
            if unit.initiative == num:
                wave.append(unit)
        waves.append(wave)
    return waves

def sort_targets(unit_list):
    target_ints = []
    for unit in unit_list:
        threat = unit.threat
        if threat not in target_ints:
            target_ints.append(threat)
    wave_ints = sorted(target_ints, reverse = True)
    targets = []
    for num in wave_ints:
        for unit in unit_list:
            if unit.threat == num:
                targets.append(unit)
    return targets


def alive_check(units):
    alive = False
    for unit in units:
        if unit.status == 'Played':
            alive = True
    return alive

async def battle_report(ctx, attackers, defenders):
    report = "===== BATTLE REPORT =====\n\n"
    report += "==== ATTACKERS ====\n"
    for unit in attackers:
        report += "TITLE: "+str(unit)+"\n"
        report += "STATUS: "+unit.status+"\n"
        report += "ATTACK: "+str(unit.stats['Attack'])+"/"+str(unit.statcaps['Attack'])+"\n"
        report += "DEFENSE: "+str(unit.stats['Defense'])+"/"+str(unit.statcaps['Defense'])+"\n"
        report += "HEALTH: "+str(unit.stats['Health'])+"/"+str(unit.statcaps['Health'])+"\n\n"

    report += "==== DEFENDERS ====\n"
    for unit in defenders:
        report += "TITLE: "+str(unit)+"\n"
        report += "STATUS: "+unit.status+"\n"
        report += "ATTACK: "+str(unit.stats['Attack'])+"/"+str(unit.statcaps['Attack'])+"\n"
        report += "DEFENSE: "+str(unit.stats['Defense'])+"/"+str(unit.statcaps['Defense'])+"\n"
        report += "HEALTH: "+str(unit.stats['Health'])+"/"+str(unit.statcaps['Health'])+"\n\n"

    await say(ctx, report)
