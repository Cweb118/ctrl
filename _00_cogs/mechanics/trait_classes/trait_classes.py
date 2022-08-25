import random

from _01_functions import say
from _02_global_dicts import theJar

#----------unit arguement guide----------

# act(self, args):
# play(self, self_unit, location):
# work(self, subject_building, self_unit, subject_units):
# move(self, self_unit, from_location, to_location):
# battle(self, attack_squad, defense_squad):
# attack(self, attack_unit, defense_unit):
# defend(self, defense_unit, attack_unit, dmg):
# death(self, ???):
# harvest(self, self_unit, def_lost, hit_status):
# refresh(self, self_unit)


#----------unit classes----------


class Architect():
    def __init__(self):
        self.triggers = ['on_act', 'on_harvest']
        self.subject = None

        # Action Info
        self.act_id = 'Architect'
        self.act_name = 'Survey'
        self.act_params = [
            ['Local Building',
                ['current_location'],
                ['building']
            ]
        ]

    def act(self, self_unit, local_target_building):
        can_copy = True
        if self_unit.stats['Endurance'] < self_unit.statcaps['Endurance']:
            report = 'Your **'+str(self_unit)+'** is not fully rested...'
            can_copy = False
        c = 0
        for cert in local_target_building.certs:
            if cert not in self_unit.certs:
                 c += 1
        if c < len(local_target_building.certs)/2:
            report = 'Your **'+str(self_unit)+'** lacks the knowledge required...'
            can_copy = False
        if can_copy:
            self_unit.setStat('Endurance', -self_unit.statcaps['Endurance'])
            self.subject = local_target_building
            report = 'Your **'+str(self_unit)+'**  begins their study...'
            self.report = "**Action: Survey**\n"+\
                     "Player: "+str(self_unit.owner)+"\n"+\
                     "Unit: "+str(self_unit)+"\n"+\
                     "Building: "+local_target_building+"\n"
        return report

    async def harvest(self, self_unit, def_lost, hit):
        #TODO: This is broken!
        if self.subject:
            await say(None, self.report, channel=theJar['control']['explore-log'])
            if self_unit.stats['Endurance'] != 0:
                if self_unit.location == self.subject.location:
                    status, bldg = self_unit.addBuildingToUnitOwnerInv(self.subject.title)
                    print(status, bldg)



class Pathfinder():
    def __init__(self):
        self.triggers = ['on_act', 'on_harvest']
        self.report = None

        # Action Info
        self.act_id = 'Pathfinder'
        self.act_name = 'Explore'
        self.act_params = [
            ['Current District', 
                ['current_location']
            ],
            ['Direction',
                ['select', [
                    ('North', 'North'), 
                    ('Northeast', 'Northeast'),
                    ('East', 'East'),
                    ('Southeast', 'Southeast'),
                    ('South', 'South'),
                    ('Southwest', 'Southwest'),
                    ('West', 'West'),
                    ('Northwest', 'Northwest')
                ]]
            ]
        ]

    def act(self, self_unit, from_location, direction):
        self.report = "**Action: Explore**\n"+\
                 "Player: "+str(self_unit.owner)+"\n"+\
                 "From Location: "+str(from_location)+"\n"+\
                 "Direction: "+direction+"\n"
        return self.report

    async def harvest(self, self_unit, def_lost, hit):
        can_go = True
        if self_unit.stats['Endurance'] < self_unit.statcaps['Endurance']:
            can_go = False
            report = '**Your '+str(self_unit) + '** lacks the Endurance to Explore...'
        if can_go:
            await say(None, self.report, channel=theJar['control']['explore-log'])
            report = '**Your '+str(self_unit) + '** ventures out...'
        return report

class Scout():
    def __init__(self):
        self.triggers = ['on_act', 'on_daybreak', 'on_harvest']
        self.target_location = None
        self.can_go = False

        # Action Info
        self.act_id = 'Scout'
        self.act_name = 'Scout'
        self.act_params = [
            ['Adjacent Location',
                ['current_location'],
                ['adjacent_location']
            ]
        ]

    def act(self, self_unit, adjacent_target_location):
        self.target_location = adjacent_target_location
        report = 'Scouting expedition planned for '+str(adjacent_target_location)+'...'
        return report

    def harvest(self, self_unit, def_lost, hit):
        self.can_go = True
        if not self.target_location:
            self.can_go = False
        if self_unit.stats['Endurance'] < 2:
            self.can_go = False
        if self.target_location:
            if self.target_location.name not in self_unit.location.paths:
                self.can_go = False

    async def daybreak(self, self_unit):
        if self.can_go:
            player = self_unit.owner
            report, title, fields = self.target_location.report()
            await say(None, report, title=title, fields=fields, channel=player.channel)
        else:
            if self.target_location:
                player = self_unit.owner
                report = "[Scout] **"+str(self_unit)+'** was unable to scout '+str(self.target_location)
                await say(None, report, channel=player.channel)


class Sentry():
    #Shouldn't this be a passive vision of adj interfaces?
    def __init__(self):
        self.triggers = ['on_harvest']

    async def harvest(self, self_unit, f, hit):
        player = self_unit.owner
        if self_unit.stats['Endurance'] >= self_unit.statcaps['Endurance']:
            location = self_unit.location
            adj_locs = [theJar['districts'][x] for x in location.paths]
            report = "[Sentry] Your **"+str(self_unit)+"** watches as night falls, making the following observations..."
            for adj_loc in adj_locs:
                locrep, title, fields = adj_loc.report()
                await say(None, locrep, title=title, fields=fields, channel=player.channel)
        else:
            report = "[Sentry] Your **"+str(self_unit)+"** is not fully rested for their watch..."
        return report


class Recon():
    def __init__(self):
        self.triggers = ['on_move', 'on_death']

    async def move(self, self_unit, from_location, to_location):
        player = self_unit.owner
        #check if unit was the last recon unit in from_loc
        print('Unit Movement, Analyzing: '+str(from_location))
        old_chat, old_inf = from_location.canChat(player)
        if not old_chat:
            await from_location.channel.removePlayer(player.member)
        if not old_inf:
            await from_location.interfaceChannel.removePlayer(player.member)
        #check if unit is the first recon unit in to_loc
        print('Unit Movement, Analyzing: '+str(to_location))
        new_chat, new_inf = to_location.canChat(self_unit.owner)
        if new_chat:
             await to_location.channel.addPlayer(player.member)
        if new_inf:
            await to_location.interfaceChannel.addPlayer(player.member)

    async def death(self, self_unit):
        player = self_unit.owner
        old_location = theJar['districts'][self_unit.location]
        #check if unit was the last recon unit in old_loc
        old_chat, old_inf = old_location.canChat(player)
        if not old_chat:
            await old_location.channel.removePlayer(player.member)
        if not old_inf:
            await old_location.interfaceChannel.removePlayer(player.member)


class Warrior():
    def __init__(self):
        self.triggers = ['on_attack']

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
        self.triggers = ['on_attack', 'on_defend']
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
    def __init__(self):
        self.triggers = ['on_attack']

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


class Knight():
    def __init__(self):
        self.triggers = ['on_attack', 'on_defend']

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
    def __init__(self):
        self.triggers = ['on_battle', 'on_attack']

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
    def __init__(self):
        self.triggers = ['on_attack']

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
    def __init__(self):
        self.triggers = ['on_attack', 'on_refresh']

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
    def __init__(self):
        self.triggers = ['on_play']

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

    #TODO: Gotta think about this a bit more, not sure if every defense move can be compatible with this love triangle thing going on (fixed maybe?)
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
    def __init__(self):
        self.triggers = ['on_attack']

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
    def __init__(self):
        self.triggers = ['on_act']

        # Action Info
        self.act_id = 'Automata'
        self.act_name = 'Overclock'
        self.act_params = []

    def act(self, self_unit):
        inv = self_unit.inventory

        if inv.resources['Steam'] >= 3:
            inv.addResource('Steam', -3)
            self_unit.stats['Endurance'] += self_unit.statcaps['Endurance']
            report = "The "+str(self_unit)+" whistles as its Endurance grows."
        else:
            report = "The "+str(self_unit)+" lacks steam!"
        return report

class Barheim():
    def __init__(self):
        self.triggers = ['on_play', 'on_act', 'on_move']
        self.reduced = False

        # Action Info
        self.act_id = 'Barheim'
        self.act_name = 'Inspire'
        self.act_params = [
            ['Local Industrialist Unit',
                ['current_location'],
                ['industrialist_unit']
            ]
        ]

    def reduce(self, building):
        if len(building.inventory.slots['unit']) < building.inventory.slotcap['unit']-1:
            self.reduced = True
            building.inventory.slotcap['unit'] += -1

    def unreduce(self, building):
        if self.reduced:
            building.inventory.slotcap['unit'] += 1

    def play(self, self_unit, location):
        if type(location).__name__.lower() == 'building':
            self.reduce(location)

    def move(self, self_unit, from_location, to_location):
        if type(to_location).__name__.lower() == 'building':
            self.reduce(to_location)
        if type(from_location).__name__.lower() == 'building':
            self.unreduce(from_location)

    def act(self, self_unit, local_industrialist_target_unit):
        if not local_industrialist_target_unit.hasTrait('Charged'):
            if self_unit.stats['Endurance'] == self_unit.statcaps['Endurance']:
                self_unit.setStat('Endurance', -self_unit.statcaps['Endurance'])
                local_industrialist_target_unit.addTrait('Charged')
                report = str(local_industrialist_target_unit)+' has become Charged.'
            else:
                report = str(self_unit)+' lacks endurance!'
        else:
            report = str(local_industrialist_target_unit)+' is already charged!'
        return report

class Eelaki():
    def __init__(self):
        self.triggers = []
    #PASS
    #Somehow decide a target; they get a big buff (defence or dodge idk)

class Loyavasi():
    def __init__(self):
        self.triggers = ['on_refresh']

    def refresh(self, self_unit):
        self_unit.stats['Endurance'] = self_unit.statcaps['Endurance']+2

class Otavan():
    def __init__(self):
        self.triggers = []

class Prismari():
    def __init__(self):
        self.triggers = ['on_defend']

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
    def __init__(self):
        self.triggers = ['on_play', 'on_refresh']

    def play(self, self_unit, location):
        if not self_unit.hasTrait('Charged'):
            self_unit.addTrait('Charged')
    def refresh(self, self_unit):
        if not self_unit.hasTrait('Charged'):
            self_unit.addTrait('Charged')


class Tevaru():
    def __init__(self):
        self.triggers = []

class Xinn():
    def __init__(self):
        self.triggers = []


class Yavari():
    def __init__(self):
        self.triggers = ['on_play', 'on_act']

        # Action Info
        self.act_id = 'Yavari'
        self.act_name = 'Harmonize'
        self.act_params = [
            ['Local Unit',
                ['current_location'],
                ['unit']
            ]
        ]

    def play(self, self_unit, location):
        if not self_unit.hasTrait('Harmony'):
            self_unit.addTrait('Harmony')

    def act(self, self_unit, local_target_unit):
        effect_trait_names = None
        if self_unit.hasTraitType('effect'):
            effect_trait_names = self_unit.getTraitbyType('effect')
        if effect_trait_names:
            if self_unit.stats['Endurance'] == self_unit.statcaps['Endurance']:
                self_unit.setStat('Endurance', -self_unit.statcaps['Endurance'])
                for effect_trait in effect_trait_names:
                    if not local_target_unit.hasTrait(effect_trait):
                        local_target_unit.addTrait(effect_trait)
                        report = str(local_target_unit)+' was given '+str(effect_trait)+' successfully.'
                    else:
                        report = str(local_target_unit)+' already has '+str(effect_trait)+'...'
            else:
                report = "**"+str(self_unit)+'** is not fully rested...'
        else:
            report = str(self_unit)+' does not possess any effect traits...'
        return report


#----------effects----------

class Harmony():
    def __init__(self):
        self.triggers = ['on_harvest']

    def harvest(self, self_unit, def_lost, hit_status):
        health_rep = "[Harmony] The "+str(self_unit)+" rests in revelries."
        if def_lost > 0:
            print(def_lost)
            def_regen = int(round(def_lost/2-0.1, 0))
            print(def_regen)
            self_unit.setStat('Defense', def_regen)
            health_rep = "[Harmony] The **"+str(self_unit)+"** steels itself. "+str(def_regen)+" defense was regained."
        return health_rep


class Charged():
    def __init__(self):
        self.triggers = ['on_harvest']

    def harvest(self, self_unit, def_lost, hit_status):
        if self_unit.hasTrait('Charged'):
            self_unit.delTrait('Charged')
            report = '[Charged] **'+str(self_unit)+"** rests."
            return report


class Morale():
    def __init__(self):
        self.triggers = ['on_work']

    #TODO: TEST
    def work(self, subject_building, self_unit, subject_units):
        for output in subject_building.outputs.keys():
            resource = theJar['resources'][output]
            subject_building.inventory.addResource(self, resource, 1)
        subject_building.delTrait('Good Morale')

#TODO: Thorns?


# unit skills

class Gatherer():
    def __init__(self):
        self.triggers = ['on_move']
        self.loot = 'Food'

    def move(self, self_unit, from_location, to_location):
        #self_unit.owner.updatePerms(from_location, to_location

        loc_size_pass_bars = {
            'tiny': 2,
            'small': 3,
            'medium': 4,
            'large': 5,
            'huge': 6,
        }

        res_per_hit = {
            0:0,
            1:1,
            2:3,
            3:5,
            4:7,
            5:9,
        }
        to_loc_bar = loc_size_pass_bars[to_location.size]
        s, report = self_unit.die_set.roll_math(to_loc_bar)
        hits = report['hit_count']
        if hits > 5:
            hits = 5
        res_yield = res_per_hit[hits]
        self_unit.inventory.addResource(self.loot,res_yield)

        food_ct = self_unit.inventory.resources['Food']
        water_ct = self_unit.inventory.resources['Water']
        if food_ct > water_ct:
            self.loot = 'Water'
        else:
            self.loot = 'Food'

        report = "[Gather] **"+str(self_unit)+"** has found "+str(res_yield)+" "+str(self.loot)+" upon entering "+str(to_location)+"."
        return report


class Colonist():
    def __init__(self):
        self.triggers = ['on_harvest']

    #TODO: TEST
    def harvest(self, self_unit, def_lost, hit_status):
        health_rep = None
        if hit_status:
            hit, report_dict = self_unit.die_set.roll_math(self_unit.stats['Defense']+self_unit.stats['Fortitude'])
            if not hit:
                self_unit.setHealth(1)
                health_rep = "[Colonist] The "+str(self_unit)+" steels itself, negating loss of health."
        return health_rep


#----------building arguement guide----------

# act(self, args*):
# play(self, self_unit, location):
# work(self, subject_building, subject_units, logic_args*):
# move(self, self_unit, from_location, to_location):
# battle(self, attack_squad, defense_squad):
# attack(self, attack_unit, defense_unit):
# defend(self, defense_unit, attack_unit, dmg):
# death(self, ???):
# harvest(self, self_unit, def_lost, hit_status):
# refresh(self, self_unit):


#----------building_logic----------

class Transport():
    #TODO: TEST
    def __init__(self):
        self.triggers = ['on_act', 'on_refresh']
        self.link_slots = 1
        self.links = []

        # Action Info
        self.act_id = 'Transport'
        self.act_name = 'Transport'
        self.act_params = [
            [
                'Local Building (Sender)',
                ['current_location'],
                ['building']
            ],
            [
                'Local Building (Receiver)',
                ['current_location'],
                ['building']
            ],
            [
                'Operation (Expends/Restores full Endurance)',
                ['select', [('add', 'Add'), ('del', 'Delete')]]
            ]
        ]

    #Designates the buildings to link up (or unlink)
    def act(self, self_card, sender, receiver, operation):
        if operation == 'add':
            pair = (sender, receiver)
            if len(self.links) < self.link_slots:
                try:
                    if self_card.stats['Endurance'] == self_card.statcaps['Endurance']:
                        self_card.setStat('Endurance', -self_card.statcaps['Endurance'])
                        can_add = True
                    else:
                        can_add = False
                except:
                    can_add = True
                if can_add:
                    self.links.append(pair)
                    sender = pair[0]
                    receiver = pair[1]
                    if self_card.location == sender.location == receiver.location:
                        sender.addLink(receiver)
                    report = 'Link Established: '+str(pair[0])+" > "+str(pair[1])
                else:
                    report = "**"+str(self_card)+'** is not fully rested...'
            else:
                report = 'Link Failed: This unit already has an assignment'

        if operation == 'del':
            pair = (sender, receiver)
            if pair in self.links:
                try:
                    if self_card.stats['Endurance'] == 0:
                        self_card.setStat('Endurance', self_card.statcaps['Endurance'])
                except:
                    pass
                self.links.remove(pair)
                sender = pair[0]
                receiver = pair[1]
                if self_card.location == sender.location == receiver.location:
                    sender.delLink(receiver)
                report = 'Link Decommissioned: '+pair[0]+" > "+pair[1]
            else:
                report = 'Error: Link not found'
        return report

    #This engages the links
    #OOP: It does it too late in the order of operations lol. Moved to above
    # def harvest(self, self_card, def_lost, hit_status):
    #     for link in self.links:
    #         sender = link[0]
    #         receiver = link[1]
    #         if self_card.location == sender.location == receiver.location:
    #             sender.addLink(receiver)

    #This cleanses them
    def refresh(self, self_card):
        for link in self.links:
            sender = link[0]
            receiver = link[1]
            if self_card.location == sender.location == receiver.location:
                sender.delLink(receiver)

class Mend():
    #TODO: TEST
    def __init__(self):
        self.triggers = ['on_work']

    def work(self, self_building, subject_units, stat, quantity):
        for unit in subject_units:
            unit.setStat(stat, quantity)

class Upkeep():
    #TODO: TEST
    def __init__(self):
        self.triggers = ['on_work']

    def work(self, self_building, subject_units):
        for unit in subject_units:
            if unit.upkeep:
                for resource in unit.upkeep.keys():
                    unit.inventory.addResource(resource, unit.upkeep[resource])

class Speed():
    #TODO: TEST
    def __init__(self):
        self.triggers = ['on_work']

    def work(self, self_building, subject_units):
        for unit in subject_units:
            unit.stats['Endurance'] = unit.statcaps['Endurance']*2

class Sacrifice():
    #TODO: TEST
    def __init__(self):
        self.triggers = ['on_work']

    def work(self, self_building, subject_units, stat, quantity):
        for unit in subject_units:
            unit.setHealth(-unit.statcaps['Health'])

class Defense():
    #TODO: Figure out defense mechanics :)
    #Done: It just counts the Combatant certs lol
    def __init__(self):
        self.triggers = ['on_work']

    def work(self, self_building, subject_units, def_modifier):
        district = self_building.location


class Ward():
    #TODO: TEST
    #Should show adj location interfaces?
    def __init__(self):
        self.triggers = ['on_work']

    def work(self, self_building, subject_units, range):
        report = "**Action: Ward**\n"+\
                 "Player: "+self_building.owner+"\n"+\
                 "Current Location: "+self_building.location.name+"\n"
        if range > 0:
            report += "Adj Locations: "+self_building.location.paths+"\n"
        #say to explore channel(report)
        print(report)


class Train():
    #TODO: TEST
    def __init__(self):
        self.triggers = ['on_work']

    def work(self, self_building, subject_units, new_trait):
        for unit in subject_units:
            print(unit)
            if new_trait['type'] == 'class':
                class_traits = unit.getTraitbyType('class')
                print("traits pre delete: "+class_traits)
                unit.delTrait(class_traits[0])
            unit.addTrait(new_trait)

class WorkerBoon():
    #TODO: TEST
    def __init__(self):
        self.triggers = ['on_work']

    def work(self, self_building, subject_units, trait):
        for unit in subject_units:
            unit.addTrait(trait)

class DistrictBoon():
    #TODO: TEST
    def __init__(self):
        self.triggers = ['on_work']

    def work(self, self_building, subject_units, trait):
        district = subject_units[0].location.location
        for building in district.inventory['building']:
            building.addTrait(trait)

class Reproduce():
    #TODO: TEST
    def __init__(self):
        self.triggers = ['on_work']

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

class Mentor():
    #TODO: TEST
    def __init__(self):
        self.triggers = ['on_work']

    def work(self, self_building, subject_units):
        mentor = subject_units[0]
        traits = mentor.trait_list
        status, man = self_building.addUnitToBuildingInv()
        if man:
            for trait in traits:
                man.addTrait(trait)


#----------building_effects----------


#TODO: Thorns?


