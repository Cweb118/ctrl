import random

from _02_global_dicts import theJar
from _00_cogs.mechanics.unit_classes._unit_kits import unit_kits_dict
#----------unit classes----------

class Worker():
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
    def action(self):
        print('action!')

class Knight():
    def attack(self, attack_unit, defense_unit):
        def_def = defense_unit.stats['Defense']
        hit, report_dict = attack_unit.die_set.roll_math(def_def)
        if hit:
            dam = 1
            health_rep = defense_unit.dmg(-1)
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

        report = "\n\n-------BLOCK-------\n\n"+\
                 "Rolled: "+str(defense_unit.die_set)+"\n"+\
                 "Rolls: "+str(report_dict['rolls'])+"\n"+\
                 "Defense: "+str(report_dict['threshold'])+"\n"+\
                 "Damage Blocked: "+str(blocked)+"\n\n"+\
                 "---"+str(report_dict['result'])+"---\n"+health_rep
        self.charged = False
        return report

class Alchemist():
    def attack(self, attack_unit, defense_unit):
        def_att = defense_unit.stats['Attack']
        hit, report_dict = attack_unit.die_set.roll_math(def_att)
        succs = len(report_dict['rolls']) - int(report_dict['hit_count'])
        if succs > 0:
            defense_unit.setStat('Attack', -succs)
            act_rep = "The potion weakens "+str(defense_unit)+" by "+str(succs)+"."
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

#----------races----------

class Aratori():
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
    #NOTE: PASSIVE (no upkeep)
    def action(self):
        print('action!')

class Barheim():
    #NOTE: On work (double worked)
    def action(self):
        print('action!')

class Eelaki():
    def action(self):
        print('action!')

class Loyavasi():
    def action(self):
        print('action!')

class Otavan():
    def action(self):
        print('action!')

class Prismari():
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
            return report

class Rivenborne():
    def action(self):
        print('action!')

class Tevaru():
    #NOTE: PASSIVE (can have a 'partner' played to them')
    def action(self):
        print('action!')

class Xinn():
    def action(self):
        print('action!')

class Yavari():
    #TODO: Add influence cost (1)
    #TODO: TEST
    def act(self, self_unit, target_unit):
        effect_trait_names = None
        if self_unit.hasTraitType('effect'):
            effect_trait_names = self_unit.getTraitbyType('effect')
        if effect_trait_names:
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


#----------building_logic----------

class Mend():
    #TODO: TEST
    def work(self, self_building, subject_units, stat, quantity):
        for unit in subject_units:
            unit.setStat(stat, quantity)

class Train():
    #TODO: This actually wont work :( You need to make a brand new unit and transfer the stuff over (then delete old?)
    #TODO: TEST
    def work(self, self_building, subject_units, trait):
        for unit in subject_units:
            if 'Novice' in unit.getTraitCerts():
                unit.title = unit.title.replace(' Worker', '')
                unit.addTrait(trait)
                unit.delTraitCert('Novice')

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

    def act(self, sender, receiver, operation):
        if operation == 'add':
            pair = (sender, receiver)
            if len(self.links) < self.link_slots:
                self.links.append(pair)
        if operation == 'del':
            pair = (sender, receiver)
            if pair in self.links:
                self.links.remove(pair)

    def work(self, self_building, subject_units):
        i = 0
        while i < len(subject_units)/2:
            sender = self.links[i][0]
            receiver = self.links[i][1]
            sender.dellink(receiver)
            i += 1

    def harvest(self):
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
        race_pick = random.randint(0,1)
        class_pick = random.randint(0,2)

        picked_race = races[race_pick]
        picked_class = classes[class_pick]

        status, man = self_building.inventory.addCard(unit_kits_dict[picked_class], 'unit')
        man.addTrait(picked_race)



