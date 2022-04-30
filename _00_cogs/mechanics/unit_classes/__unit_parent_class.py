from _00_cogs.mechanics.dice_class import Dice
from _00_cogs.mechanics._cards_class import Card
from _00_cogs.mechanics.trait_classes.__trait_parent_class import Trait
from _00_cogs.mechanics.trait_classes._trait_kits import trait_kits_dict
from _00_cogs.mechanics.unit_classes._unit_kits import unit_kits_dict

from _02_global_dicts import theJar


class Unit(Card):
    def __init__(self, owner, title, description, inv_args, traits, play_cost, stats, upkeep_dict, initv, threat, dice_stats):
        inv_args = [self]+inv_args
        super().__init__(owner, title, description, inv_args=inv_args, play_cost=play_cost)

        self.stats = {
            'Attack':stats['attack'],
            'Health':stats['health'],
            'Defense':stats['defense'],
            'Endurance':stats['endurance'],
            'Fortitude':stats['fortitude']
        }
        self.statcaps = {
            'Attack':stats['attack'],
            'Health':stats['health'],
            'Defense':stats['defense'],
            'Endurance':stats['endurance'],
            'Fortitude':stats['fortitude']
        }

        self.initiative = initv
        self.threat = threat
        self.upkeep = {}
        self.die_list = dice_stats
        self.die_set = Dice(dice_stats)

        for key in upkeep_dict.keys():
            resource = theJar['resources'][key]
            self.upkeep[resource] = upkeep_dict[key]

        self.trait_list = traits
        self.traits = {
            'on_play': [],
            'on_work': [],
            'on_move': [],
            'on_battle':[],
            'on_attack': [],
            'on_defend': [],
            'on_death': [],
            'on_act': [],
        }
        for trait_name in traits:
            self.addTrait(trait_name)


    def addUnit(self, card_kit_id, inv_owner, owner_type):
        inv = theJar[owner_type][inv_owner].inventory
        can_add = inv.capMathCard('unit')
        if can_add == True:
            kit = [self]+unit_kits_dict[card_kit_id]
            card = Unit(*kit)
            if card:
                inv.cards['unit'].append(card)
            else:
                can_add = False
        return can_add, card


    def setNick(self, nick):
        self.title = self.title+" \""+nick+"\""

    def setStat(self, stat, quantity):
        self.stats[stat] += quantity
        if self.stats[stat] < 0:
            self.stats[stat] = 0
        if self.stats[stat] > self.statcaps[stat]:
            self.stats[stat] = self.statcaps[stat]
        return self.stats[stat]

    def setHealth(self, quantity):
        self.setStat('Health', quantity)
        if self.stats['Health'] <= 0:
            self.status = "DEAD"
            report = "The **"+str(self)+'** has died.'
        else:
            report = "The **"+str(self)+'** now has '+str(self.stats['Health'])+' Health.'
        return report

    def dmg(self, attack_value):
        if self.stats['Defense'] > 0:
            self.setStat('Defense', -attack_value)
            health_rep = "The **"+str(self)+"'s** Defense is now "+str(self.stats['Defense'])
        else:
            health_rep = self.setHealth(-attack_value)
        return health_rep

    def addTrait(self, trait_name):
        if not self.hasTrait(trait_name):
            trait = Trait(*trait_kits_dict[trait_name])
            if trait.trait_title not in self.title:
                if trait.trait_type != 'effect':
                    if trait.trait_type == 'class':
                        self.title =  self.title+" "+trait.trait_title
                    else:
                        self.title = trait.trait_title+" "+self.title
        if trait.trait_stats_dict:
            for mod_stat in trait.trait_stats_dict.keys():
                value = trait.trait_stats_dict[mod_stat]
                self.stats[mod_stat] += value
                self.statcaps[mod_stat] += value
                if self.stats[mod_stat] < 0:
                    self.stats[mod_stat] = 0
                    self.statcaps[mod_stat] = 0
        if trait.trait_play_cost:
            for mod_cost in trait.trait_play_cost.keys():
                value = trait.trait_play_cost[mod_cost]
                try:
                    self.upkeep[mod_cost] += value
                except:
                    self.upkeep[mod_cost] = value
        if trait.trait_upkeep_dict:
            for mod_upkeep in trait.trait_upkeep_dict.keys():
                resource = resource_dict[mod_upkeep]
                value = trait.trait_upkeep_dict[mod_upkeep]
                try:
                    self.upkeep[resource] += value
                except:
                    self.upkeep[resource] = value
                if self.upkeep[resource] < 0:
                    self.upkeep[resource] = 0

        if trait.trait_inv_args:
            inv = self.inventory
            for key in trait.trait_inv_args.keys():
                value = trait.trait_inv_args[key]
                if key == 'cont':
                    try:
                        inv.cont += value
                    except:
                        inv.cont = value
                elif key == "cap":
                    for type in value.keys():
                        mod = value[type]
                        try:
                            inv.cap[type] += mod
                        except:
                            inv.cap[type] = mod
                elif key == "slotcap":
                    for type in value.keys():
                        mod = value[type]
                        try:
                            inv.slotcap[type] += mod
                        except:
                            inv.slotcap[type] = mod
                else:
                    print("Error: Invalid inventory constraint.")
        if trait.trait_initiative:
            self.initiative += trait.trait_initiative
        if trait.trait_threat:
            self.threat += trait.trait_threat
        if trait.trait_dice_stats:
            new_set = self.die_list + trait.trait_dice_stats
            self.die_list = new_set
            self.die_set = Dice(new_set)
        for trig in trait.trigger:
            self.traits[trig].append(trait)

    def hasTrait(self, trait_name):
        trait = Trait(*trait_kits_dict[trait_name])
        triggers = trait.trigger
        has = False
        for trigger in triggers:
            for current_trait in self.traits[trigger]:
                if trait.trait_title == current_trait.trait_title:
                    has = True
        return has

    def getTrait(self, trait_name):
        trait = Trait(*trait_kits_dict[trait_name])
        return trait

    def hasTraitType(self, type):
        has = False
        for trigger in self.traits.keys():
            for current_trait in self.traits[trigger]:
                if current_trait.trait_type == type:
                    has = True
        return has

    def getTraitbyType(self, type):
        trait_name_list = []
        for trigger in self.traits.keys():
            for current_trait in self.traits[trigger]:
                if current_trait.trait_type == type:
                    trait_name_list.append(current_trait.trait_title)
        return trait_name_list

    def hasTraitCert(self, cert_name):
        has = False
        certs = self.getTraitCerts()
        if cert_name in certs:
            has = True
        return has

    def getTraitCerts(self):
        cert_list = []
        for trigger in self.traits.keys():
            for current_trait in self.traits[trigger]:
                if current_trait.trait_certs:
                    for cert in current_trait.trait_certs:
                        if cert not in cert_list:
                            cert_list.append(cert)
        return cert_list

    def delTraitCert(self, cert_name):
        for trigger in self.traits.keys():
            for current_trait in self.traits[trigger]:
                if current_trait.trait_certs:
                    if cert_name in current_trait.trait_certs:
                        current_trait.trait_certs.remove(cert_name)

    def moveUnit(self, dest_type, destination):
        if self.status == 'Played':
            if self.stats['Endurance'] > 0:
                can_move = False
                if dest_type == 'district':
                    if destination in self.location.paths:
                        can_move = True
                if dest_type == 'unit':
                    if self.location == destination.location:
                        can_move = True
                if can_move:
                    slot_count = len(destination.inventory.slots['unit'])
                    slotcap = destination.inventory.slotcap['unit']
                    if slot_count < slotcap:
                        destination.inventory.slots['unit'].append(self)
                        self.location.inventory.slots['unit'].remove(self)
                        self.location = destination
                        self.setStat('Endurance', -1)
                        report = "Unit moved successfully."
                    else:
                        report = "Error: This destination does not have the required space."
                else:
                    report = "Error: This destination is too far."
            else:
                report = "Error: This unit does not have the Endurance."
        else:
            report = "Error: This unit has not yet been played."
        return report

    def harvest(self):
        if self.status == "Played":
            #player = player_dict[self.owner.id]
            f = 0
            for resource in self.upkeep.keys():
                quantity = self.upkeep[resource]
                i = 0
                while i < quantity:
                    if not self.inventory.addResource(resource, -1):
                        f += 1
                    i += 1

            if f > 0:
                self.setStat('Defense', -f)

            if self.stats['Defense'] > 0:
                def_report = "Your **"+str(self)+'** has lost '+str(f)+' Defense due to lacking required resources.'
            else:
                def_report = "Your **"+str(self)+'** has no Defense remaining.'
            hit, report_dict = self.die_set.roll_math(self.stats['Defense']+self.stats['Fortitude'])
            if hit:
                health_report = self.setHealth(-1)
            else:
                health_report = "Your **"+str(self)+'** has sustained no damage.'

            #TODO: HARVEST TRAIT ACTIVATE

            title = "-----"+str(self)+" Upkeep Results-----"
            report = "- Rolled: "+str(self.die_set)+" ("+str(self)+")\n"+\
                     "- Rolls: "+str(report_dict['rolls'])+"\n"+\
                     "- Defense + Fortitude: "+str(report_dict['threshold'])+"\n"+\
                     "- Damage Taken: "+str(report_dict['hit_count'])+"\n\n"+\
                     def_report+"\n"+\
                     health_report

            return report, title

    def __str__(self):
        return self.title

    def report(self):
        fields = []
        title = "-----"+self.title+"-----"

        report = self.description

        info_rep = {'inline':True}
        info_rep['title'] = '-- Info:'
        info_rep['value'] =  "\n- Status: "+str(self.status)+\
                             "\n- Location: "+str(self.location)+\
                             "\n- Traits: "+str(self.trait_list)
        info_rep['value'] += "\n- Die Set: "+str(self.die_set)
        info_rep['value'] += "\n- Upkeep: "
        for key in self.upkeep.keys():
            value = self.upkeep[key]
            info_rep['value'] += str(value)+" "+str(key) +", "
        info_rep['value'] = info_rep['value'][:-2]
        fields.append(info_rep)

        stats_rep = {'inline':True}
        stats_rep['title'] = "-- Stats:"
        stats_rep['value'] = ''
        for key in self.stats.keys():
            value = self.stats[key]
            cap = self.statcaps[key]
            stats_rep['value'] += "- "+str(key)+" "+str(value)+"/"+str(cap)+"\n"
        stats_rep['value'] = stats_rep['value'][:-1]
        fields.append(stats_rep)

        inv_report, inv_title, inv_fields = self.inventory.report()
        fields += inv_fields
        return report, title, fields
