import random
from _02_global_dicts import theJar
import _00_cogs.mechanics.resource_class
#----------unit classes----------

class Worker():
    def mmmm(self):
        print('mmmm')

class Warrior():
    def attack(self, attack_unit, defense_unit):
        def_def = defense_unit.stats['Defense']
        hit, report_dict = attack_unit.die_set.roll_math(def_def)
        if hit:
            health_rep = defense_unit.setHealth(-int(report_dict['hit_count']))
        else:
            health_rep = "The "+str(defense_unit)+' has evaded taking damage.'

        report = "\n\n-------CRIT-------\n\n"+\
                 "Rolled: "+str(attack_unit.die_set)+"\n"+\
                 "Rolls: "+str(report_dict['rolls'])+"\n"+\
                 "Opponent Defense: "+str(report_dict['threshold'])+"\n"+\
                 "Damage Inflicted: "+str(report_dict['hit_count'])+"\n\n"+\
                 "---"+str(report_dict['result'])+"---\n"+health_rep
        return report

class Guardian():
    def __init__(self):
        self.charged = True

    def attack(self, attack_unit, defense_unit):
        self.charged = True

    def defend(self, defense_unit, attack_unit, dmg):
        if self.charged == True:
            def_def = defense_unit.stats['Defense']
            hit, report_dict = defense_unit.die_set.roll_math(def_def)
            succs = len(report_dict['rolls'])-int(report_dict['hit_count'])
            if succs > 0:
                if dmg > 0:
                    new_dmg = dmg - succs
                    if new_dmg < 0:
                        new_dmg = 0
                    blocked = dmg - new_dmg
                    defense_unit.setStat('Defense', blocked)
                    health_rep = "The "+str(defense_unit)+" has blocked "+str(blocked)+" damage."
                else:
                    blocked = 0
                    health_rep = "The "+str(defense_unit)+' took no damage.'
            else:
                blocked = 0
                health_rep = "The "+str(defense_unit)+' has failed to block any damage.'

            report = "\n\n-------BLOCK-------\n\n"+\
                     "Rolled: "+str(defense_unit.die_set)+"\n"+\
                     "Rolls: "+str(report_dict['rolls'])+"\n"+\
                     "Opponent Defense: "+str(report_dict['threshold'])+"\n"+\
                     "Damage Blocked: "+str(blocked)+"\n\n"+\
                     "---"+str(report_dict['result'])+"---\n"+health_rep
            self.charged = False
            return report

class Ranger():
    def attack(self, attack_unit, defense_unit):
        def_def = defense_unit.stats['Defense']
        hit, report_dict = attack_unit.die_set.roll_math(def_def)
        if hit:
            new_def_def = defense_unit.setStat('Defense', -int(report_dict['hit_count']))
            health_rep = "The "+str(defense_unit)+"'s Defense has been lowered to "+str(new_def_def)
        else:
            health_rep = "The "+str(defense_unit)+' has evaded taking damage.'

        report = "\n\n-------BARRAGE-------\n\n"+\
                 "Rolled: "+str(attack_unit.die_set)+"\n"+\
                 "Rolls: "+str(report_dict['rolls'])+"\n"+\
                 "Opponent Defense: "+str(report_dict['threshold'])+"\n"+\
                 "Damage Inflicted: "+str(report_dict['hit_count'])+"\n\n"+\
                 "---"+str(report_dict['result'])+"---\n"+health_rep
        return report

class Scout():
    #TODO: TEST
    def __init__(self):
        self.loot = theJar['resources']['Food']

    def act(self, self_unit, from_location, direction):
        #explore!
        print('explore!')
        explore_channel = "get the explore channel from the jar which was made on game start"
        squad = self_unit.squad

        report = "Player: "+self_unit.owner+"\n"+\
                 "From Location: "+from_location+"\n"+\
                 "Direction: "+direction+"\n"+\
                 "Squad: \n"+squad.report()+"\n"

        #say to explore channel(report)


    def move(self, self_unit, from_location, to_location):
        #self_unit.owner.updatePerms(from_location, to_location

        loc_size_pass_bars = {
            'tiny': 1,
            'small': 2,
            'medium': 3,
            'large': 4,
            'huge': 5,
        }

        res_per_hit = {
            0:0,
            1:2,
            2:5,
            3:8,
            4:11,
            5:14,
        }
        to_loc_bar = loc_size_pass_bars[to_location.size]
        s, report = self_unit.dice.roll_math(to_loc_bar)
        hits = report['hit_count']
        if hits > 5:
            hits = 5
        res_yield = res_per_hit[hits]
        self_unit.inventory.addResource(self.loot,res_yield)

        food_ct = self_unit.inventory.resources[theJar['resources']['Food']]
        water_ct = self_unit.inventory.resources[theJar['resources']['Water']]
        if food_ct > water_ct:
            self.loot = theJar['resources']['Water']
        else:
            self.loot = theJar['resources']['Food']

        report = str(self_unit)+" has found "+str(res_yield)+" "+str(self.loot)+" upon entering "+str(to_location)+"."
        return report



class Knight():
    def attack(self, attack_unit, defense_unit):
        def_def = defense_unit.stats['Defense']
        hit, report_dict = attack_unit.die_set.roll_math(def_def)
        if hit:
            dam = 1
            health_rep = defense_unit.dmg(-1)
            if attack_unit.hasTrait('Charged'):
                attack_unit.setStat('Defense', 1)
                health_rep = "The "+str(attack_unit)+' has regained some strength.'
        else:
            dam = 0
            health_rep = "The "+str(defense_unit)+' has evaded taking damage.'

        report = "\n\n-------MINOR CRIT-------\n\n"+\
                 "Rolled: "+str(attack_unit.die_set)+"\n"+\
                 "Rolls: "+str(report_dict['rolls'])+"\n"+\
                 "Opponent Defense: "+str(report_dict['threshold'])+"\n"+\
                 "Damage Inflicted: "+str(dam)+"\n\n"+\
                 "---"+str(report_dict['result'])+"---\n"+health_rep
        return report

    def defend(self, defense_unit, attack_unit, dmg):
        def_def = defense_unit.stats['Defense']
        #Rolls against own defence, success for each non-hit
        hit, report_dict = defense_unit.die_set.roll_math(def_def)
        succs = len(report_dict['rolls'])-int(report_dict['hit_count'])
        if succs > 0:
            if dmg > 0:
                new_dmg = dmg - 1
                if new_dmg < 0:
                    new_dmg = 0
                blocked = dmg - new_dmg
                defense_unit.setStat('Defense', blocked)
                health_rep = "The "+str(defense_unit)+" has blocked "+str(blocked)+" damage."
            else:
                blocked = 0
                health_rep = "The "+str(defense_unit)+' took no damage.'
        else:
            blocked = 0
            health_rep = "The "+str(defense_unit)+' has failed to block any damage.'

        report = "\n\n-------MINOR BLOCK-------\n\n"+\
                 "Rolled: "+str(defense_unit.die_set)+"\n"+\
                 "Rolls: "+str(report_dict['rolls'])+"\n"+\
                 "Defense: "+str(report_dict['threshold'])+"\n"+\
                 "Damage Blocked: "+str(blocked)+"\n\n"+\
                 "---"+str(report_dict['result'])+"---\n"+health_rep
        self.charged = False
        return report

class Witch():
    #TODO: TEST
    def battle(self, attack_squad, defense_squad):
        self.allies = attack_squad
        self.enemies = defense_squad
        self.channeling = 0

    def attack(self, attack_unit, defense_unit):

        if attack_unit.hasTrait('Charged'):
            self.channeling += 2

        candidates = [x for x in self.allies if x.target_unit.hasTrait('Charged') == False or x.target_unit.hasTrait('Thorns') == False and x.status == 'Played']
        if len(candidates) > 0:
            target_unit = candidates[random.randint(0,len(candidates))]
            threshold = target_unit.stats['Fortitude']+target_unit.stats['Defense']
            combo = threshold - self.channeling
            if combo < 0:
                combo = 0
            hit, report_dict = attack_unit.die_set.roll_math(combo)
            succs = len(report_dict['rolls']) - int(report_dict['hit_count'])
            if succs > 0:
                if target_unit.hasTrait('Charged'):
                    effect = 'Thorns'
                else:
                    effect = 'Charged'
                target_unit.addTrait(effect)
                act_rep = str(target_unit)+" has been empowered with the "+str(effect)+" effect."
                rep = 'SUCCESS'
            else:
                act_rep = "The "+str(attack_unit)+" continues to channel their strength."
                self.channeling += 1
                rep = 'FAILURE'
            report = "\n\n-------ARCANAE-------\n\n"+\
                     "Rolled: "+str(attack_unit.die_set)+"\n"+\
                     "Rolls: "+str(report_dict['rolls'])+"\n"+\
                     "Ally Defense+Fortitude: "+str(threshold)+"\n"+\
                     "Casting Strength: "+str(self.channeling)+"\n\n"+\
                     "---"+rep+"---\n"+act_rep

        else:
            act_rep = "The "+str(attack_unit)+" tears into their opponent, inflicting "+str(self.channeling)+" damage."
            defense_unit.dmg(self.channeling)
            self.channeling = int(self.channeling/2)
            report = "\n\n-------ARCANAE-------\n\n"+\
             "Casting Strength: "+str(self.channeling)+"\n\n"+\
             "---SUCCESS---\n"+act_rep
        return report

class Alchemist():
    def attack(self, attack_unit, defense_unit):
        def_att = defense_unit.stats['Attack']
        hit, report_dict = attack_unit.die_set.roll_math(def_att)
        succs = len(report_dict['rolls']) - int(report_dict['hit_count'])
        if succs > 0:
            if not attack_unit.hasTrait('Charged'):
                defense_unit.setStat('Attack', -succs)
                act_rep = "The potion weakens "+str(defense_unit)+" by "+str(succs)+"."
                rep = 'SUCCESS'
            else:
                succs += 1
                defense_unit.setStat('Attack', -succs)
                act_rep = "The potion weakens "+str(defense_unit)+" by "+str(succs)+" (+1 due to Charged)."
                rep = 'SUCCESS'
        else:
            act_rep = "The potion has no effect on "+str(defense_unit)+"."
            rep = 'FAILURE'

        report = "\n\n-------ALCHEMY-------\n\n"+\
                 "Rolled: "+str(attack_unit.die_set)+"\n"+\
                 "Rolls: "+str(report_dict['rolls'])+"\n"+\
                 "Opponent Attack: "+str(report_dict['threshold'])+"\n"+\
                 "Weaken: "+str(succs)+"\n\n"+\
                 "---"+rep+"---\n"+act_rep
        return report

class Technophant():
    def attack(self, attack_unit, defense_unit):
        att_att = attack_unit.stats['Attack']
        hit, report_dict = attack_unit.die_set.roll_math(att_att)
        if attack_unit.hasTrait('Charged'):
            hit += 1
        if hit:
            attack_unit.setStat('Attack', int(report_dict['hit_count']))
            act_rep = "The "+str(attack_unit)+"'s power grows."
        else:
            act_rep = "The "+str(attack_unit)+"'s power wains."

        report = "\n\n-------SURGE-------\n\n"+\
                 "Rolled: "+str(attack_unit.die_set)+"\n"+\
                 "Rolls: "+str(report_dict['rolls'])+"\n"+\
                 "Current Attack: "+str(report_dict['threshold'])+"\n"+\
                 "Growth: "+str(report_dict['hit_count'])+"\n\n"+\
                 "---"+str(report_dict['result'])+"---\n"+act_rep
        return report

    def refresh(self, self_unit):
        self_unit.setStat('Attack', self_unit.statcaps['Attack'])
        self_unit.setStat('Fortitude', self_unit.statcaps['Fortitude'])


#----------vehicles----------
class Vehicle():
    def attack(self, attack_unit, defense_unit):
        report = str(attack_unit)+" has attacked "+str(defense_unit)+". Others follow suit:"
        subunit_list = attack_unit.inventory.slots['units']
        for subunit in subunit_list:
            if len(subunit.traits['on_attack']) > 0:
                for trait in subunit.traits['on_attack']:
                    action_report = trait.action.attack(subunit, defense_unit)
                    if action_report:
                        report += action_report
        return report

    #TODO: Gotta think about this a bit more, not sure if every defense move can be compatible with this love triangle thing going on
    def defend(self, defense_unit, attack_unit, dmg):
        report = str(defense_unit)+" has been attacked by"+str(attack_unit)+". Others come to defend:"
        subunit_list = attack_unit.inventory.slots['units']
        for subunit in subunit_list:
            if len(subunit.traits['on_defend']) > 0:
                for trait in subunit.traits['on_defend']:
                    action_report = trait.action.attack(defense_unit, attack_unit, dmg, bystander=subunit)
                    if action_report:
                        report += action_report
        return report



#----------races----------

class Aratori():
    #DONE
    def attack(self, attack_unit, defense_unit):
        def_def = defense_unit.stats['Defense']
        att_att = attack_unit.stats['Attack']
        hit, report_dict = attack_unit.die_set.roll_math(def_def)
        if hit:
            health_rep = defense_unit.dmg(-int(att_att))
        else:
            health_rep = "The "+str(defense_unit)+' has evaded taking damage.'

        report = "\n\n-------MAJOR CRIT-------\n\n"+\
                 "Rolled: "+str(attack_unit.die_set)+"\n"+\
                 "Rolls: "+str(report_dict['rolls'])+"\n"+\
                 "Opponent Defense: "+str(report_dict['threshold'])+"\n"+\
                 "Damage Inflicted: "+str(report_dict['hit_count'])+"\n\n"+\
                 "---"+str(report_dict['result'])+"---\n"+health_rep
        return report

class Automata():
    #DONE
    #NOTE: PASSIVE (no upkeep)
    def action(self):
        print('action!')

class Barheim():
    #NOTE: On work, reduce unit cap by 1
    def reduce(self, building):
        if len(building.inventory.slots['unit']) < building.inventory.slotcap['unit']:
            building.inventory.slotcap['unit'] += -1

    def unreduce(self, building):
        building.inventory.slotcap['unit'] += 1

    def play(self, self_unit, location):
        if type(location).__name__.lower() == 'building':
            self.reduce(location)

    def move(self, self_unit, from_location, to_location):
        if type(to_location).__name__.lower() == 'building':
            self.reduce(to_location)
        if type(from_location).__name__.lower() == 'building':
            self.unreduce(from_location)


class Eelaki():
    #PASS
    #Somehow decide a target; they get a big buff (defence or dodge idk)
    def action(self):
        print('action!')

class Loyavasi():
    #REFRESH: +2 Endurance over cap
    def refresh(self, self_unit):
        self_unit.stats['Endurance'] = self_unit.statcaps['Endurance']+2

class Otavan():
    #DONE
    #PASSIVE: Stealth (-2 Taunt)
    def action(self):
        print('action!')

class Prismari():
    #DONE
    def defend(self, defense_unit, attack_unit, dmg):
        if attack_unit.threat >= 0:
            att_def = attack_unit.stats['Defense']
            hit, report_dict = defense_unit.die_set.roll_math(att_def)
            if hit:
                health_rep = attack_unit.dmg(-1)
            else:
                health_rep = "The "+str(attack_unit)+' has evaded taking damage.'

            report = "\n\n-------PARRY-------\n\n"+\
                     "Rolled: "+str(defense_unit.die_set)+"\n"+\
                     "Rolls: "+str(report_dict['rolls'])+"\n"+\
                     "Defense: "+str(report_dict['threshold'])+"\n"+\
                     "Damage Inflicted: "+str(1)+"\n\n"+\
                     "---"+str(report_dict['result'])+"---\n"+health_rep
        else:
            report = "The "+str(attack_unit)+' was too quick and could not be parried.'

        return report

class Rivenborne():
    #PASSIVE: Has Charged (renews)
    def play(self, self_unit):
        if not self_unit.hasTrait('Charged'):
            self_unit.addTrait('Charged')
    def refresh(self, self_unit):
        if not self_unit.hasTrait('Charged'):
            self_unit.addTrait('Charged')


class Tevaru():
    #PASS
    #NOTE: PASSIVE (can have a 'partner' played to them)
    def action(self):
        print('action!')

class Xinn():
    #DONE
    #PASSIVE: Has the Harvest cert by default
    def action(self):
        print('action!')

class Yavari():
    #TODO: TEST
    def act(self, self_unit, target_unit):
        effect_trait_names = None
        if self_unit.hasTraitType('effect'):
            effect_trait_names = self_unit.getTraitbyType('effect')
        if effect_trait_names:
            if self_unit.owner._stats[theJar['resources']['Influence']] > 0:
                self_unit.owner.modStat(theJar['resources']['Influence'], -1)
                for effect_trait in effect_trait_names:
                    if not target_unit.hasTrait(effect_trait):
                        target_unit.addTrait(effect_trait)
                        print('Target was given '+effect_trait+' successfully.')
                    else:
                        print('Target already has '+effect_trait+'!')
        else:
            print('User unit does not possess any effect traits!')


#----------effects----------

class Harmony():
    #TODO: TEST
    def harvest(self, self_unit, def_lost, hit_status):
        health_rep = "The "+str(self_unit)+" rests in revelries."
        if def_lost > 0:
            def_regen = int(round(def_lost/2-0.1, 0))
            self_unit.setStat('Defense', def_regen)
            health_rep = "The "+str(self_unit)+" steels itself. "+str(def_regen)+" defence was regained."
        return health_rep


class Charged():
    #TODO: TEST
    def harvest(self, self_unit, def_lost, hit_status):
        if self_unit.hasTrait('Charged'):
            self_unit.delTrait('Charged')

#TODO: Thorns?
#----------building_logic----------

class Mend():
    #TODO: TEST
    def work(self, self_building, subject_units, stat, quantity):
        for unit in subject_units:
            unit.setStat(stat, quantity)

class Train():
    #TODO: TEST
    def work(self, self_building, subject_units, new_trait):
        for unit in subject_units:
            class_traits = unit.getTraitbyType('class')
            unit.delTrait(class_traits[0])
            unit.addTrait(new_trait)


class Boon():
    #TODO: TEST
    def work(self, self_building, subject_units, trait):
        district = subject_units[0].location.location
        for building in district.inventory.slots['building']:
            building.addTrait(trait)

class Carry():
    #TODO: TEST
    def __init__(self):
        self.link_slots = 3
        self.links = []

    #Designates the buildings to link up (or unlink)
    def act(self, sender, receiver, operation):
        if operation == 'add':
            pair = (sender, receiver)
            if len(self.links) < self.link_slots:
                self.links.append(pair)
        if operation == 'del':
            pair = (sender, receiver)
            if pair in self.links:
                self.links.remove(pair)

    #This does... something
    def work(self, self_building, subject_units):
        i = 0
        while i < len(subject_units)/2:
            sender = self.links[i][0]
            receiver = self.links[i][1]
            sender.dellink(receiver)
            i += 1

    #This re-engages the links (probably)
    def refresh(self):
        for link in self.links:
            sender = link[0]
            receiver = link[1]
            sender.addlink(receiver)


#TODO: Thorns,

#----------building_effects----------

class Morale():
    #TODO: TEST
    def work(self, self_building, subject_units, quantity):
        for output in self_building.outputs.keys():
            resource = theJar['resources'][output]
            self_building.inventory.addResource(self, resource, quantity)
        self_building.delTrait('Good Morale')

class Reproduce():
    #TODO: TEST
    def work(self, self_building, subject_units):
        races = [x.getTraitbyType('race') for x in subject_units]
        classes = [x.getTraitbyType('class') for x in subject_units] + ['Worker']
        race_pick = random.randint(0,len(races))
        class_pick = random.randint(0,len(classes))

        picked_race = races[race_pick]
        picked_class = classes[class_pick]

        status, man = self_building.addUnitToBuildingInv()
        man.addTrait(picked_race)
        man.addTrait(picked_class)



