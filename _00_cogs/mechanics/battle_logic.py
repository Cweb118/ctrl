import asyncio
import operator

from _01_functions import say
from _02_global_dicts import theJar


#At start: Get main players
#Detrmine stance of other groups (aligned with attacker, defender, or neutral)
#Get squad ranks, shuffle between multiple allegiances in a side

async def battle(ctx, location_obj):
    civics = location_obj.civics
    loc_inv = location_obj.inventory
    #Intention: If attacking, gov is always defence. If no gov, occ is defence.
    defense = None
    if civics.governance:
        defense = civics.governance
    elif civics.occupance:
        defense = civics.occupance

    if defense:
        attacking_algs = [x for x in civics.allegiance_stances.keys()
                          if civics.allegiance_stances[x]['stance']=='Attack']
        defending_algs = [x for x in civics.allegiance_stances.keys()
                          if civics.allegiance_stances[x]['stance']=='Defend']
        defending_algs += [defense]
        if defense in attacking_algs:
            attacking_algs.remove(defense)

        defense_buildings = [x for x in loc_inv.slots['building'] if x.allegience == defense]
        defense_units = [x for x in loc_inv.slots['unit'] if x.squad == None and x.allegience in defending_algs]
        attack_units = [x for x in loc_inv.slots['unit'] if x.squad == None and x.allegience in attacking_algs]
        defense_units = sort_targets(defense_units)
        attack_units = sort_targets(attack_units)

        defense_squads = sort_squads(defending_algs)
        attack_squads = sort_squads(attacking_algs)

        while len(attack_squads) > 0 and len(defense_squads) > 0:

            sq = 0
            while sq < len(attack_squads) and sq < len(defense_squads):
                attacking_squad = attack_squads[sq]
                defending_squad = defense_squads[sq]
                squad_attack_units = sort_targets(attacking_squad.units)
                squad_defense_units = sort_targets(defending_squad.units)

                if len(squad_attack_units) > 0:
                    wave_ints = sort_inititative(squad_attack_units+squad_defense_units)
                    attack_units_waves = sort_waves(squad_attack_units, wave_ints)
                    defense_units_waves = sort_waves(squad_defense_units, wave_ints)

                    i = 1
                    cont = True
                    while cont:
                        cont = await round(ctx, i, attack_units_waves, defense_units_waves, squad_attack_units, squad_defense_units)
                        await battle_report(ctx, attack_units, defense_units)
                        await asyncio.sleep(10)
                        i += 1
                    await say(ctx, "----End of Skirmish, Attack Stands----")
                    defense_squads.remove(defending_squad)
                else:
                    await say(ctx, "----End of Skirmish, Defense Stands----")
                    attack_squads.remove(attacking_squad)
        if len(attack_squads) > 0:
            await final_strike(ctx, attack_squads, defense_buildings, defense_units)

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

async def final_strike(ctx, attack_squads, defense_buildings, defense_units):
    #TODO: Needs work. Can add the ability for units inside def buildings to attack back.
    attack_units = []
    for squad in attack_squads:
        attack_units += squad.units

    #might cause an issue if no defense units
    wave_ints = sort_inititative(attack_units+defense_units)
    attack_units_waves = sort_waves(attack_units, wave_ints)

    await say(ctx, "-----Final Strike-----")
    for attack_wave in attack_units_waves:
        #switch these around maybe? could allow for a final stand among remaining unsquaded units. could also be worker massacre
        if defense_buildings or len(defense_buildings) > 0:
            await wave(ctx, attack_wave, defense_buildings)
        elif defense_units or len(defense_units) > 0:
            await wave(ctx, attack_wave, defense_units)


def sort_squads(side_algs):
    squad_queue = []
    i = 0
    for alg in side_algs:
        i += 1
        alg_queue = []
        alg_squads = []
        for prio in alg.keys():
            alg_squads+=alg[prio]
        for sq in alg_squads:
            sq_placement = {'squad':sq, 'rank':alg_squads.index(sq), 'alg':i}
            alg_queue.append(sq_placement)
        squad_queue += alg_queue

    squad_queue.sort(key=operator.itemgetter('rank','alg'))
    squad_order = [x['squad'] for x in squad_queue]
    print(squad_order)
    return squad_order

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

    #------
def attack_check(attack_units_og, defense_units_og):
    attack_units = []
    for attacker in attack_units_og:
        att_alg = attacker.owner._allegiance
        hostiles = 0
        for defender in defense_units_og:
            def_alg = defender.owner._allegiance
            if theJar['alleigances'][att_alg][def_alg] == 'Hostile':
                hostiles += 1
                attack_units.append(attacker)
        if 0 < hostiles < len(defense_units_og)/2:
            attack_units.remove(attacker)
    return attack_units, defense_units_og
    #------
