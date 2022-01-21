
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
    def action(self):
        print('action!')

class Barheim():
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
    def action(self):
        print('action!')

class Xinn():
    def action(self):
        print('action!')

class Yavari():
    def action(self):
        print('action!')


