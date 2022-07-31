import copy

from _00_cogs.mechanics.building_classes._building_kits import building_kits_dict
from _00_cogs.mechanics.dice_class import Dice
from _00_cogs.mechanics._cards_class import Card
from _00_cogs.mechanics.trait_classes.trait_kits import trait_kits_dict
from _02_global_dicts import theJar

class Unit(Card):
    def __init__(self):

        inv_args = [self]+[0, 0, None, None, None, None]
        super().__init__('Tim', 'Civilian', inv_args=inv_args, play_cost=None)
        self.nick = None

        self.stats = {
            'Attack':0,
            'Health':0,
            'Defense':0,
            'Endurance':0,
            'Fortitude':0,
            'Initiative':0,
            'Taunt':0
        }
        self.statcaps = {
            'Attack':0,
            'Health':0,
            'Defense':0,
            'Endurance':0,
            'Fortitude':0,
            'Initiative':0,
            'Taunt':0
        }

        self.upkeep = {}
        self.die_list = []
        self.die_set = None
        self.squad = None

        self.traits = []
        self.skillsets = []
        self.effects = []
        self.certs = []
        self.race = None
        self.job = None


    def addUnit(self, card_kit_id, inv_owner, owner_type):
        #I think this is now defunct?
        inv = theJar[owner_type][inv_owner].inventory
        can_add = inv.capMathCard('unit')
        if can_add == True:
            card = Unit()
            if card:
                inv.cards['unit'].append(card)
            else:
                can_add = False
        return can_add, card


    def setNick(self, nick):
        self.nick = nick
        self.regenName()

    def regenName(self):
        nameParts = []
        if self.race:
            nameParts.append(str(self.race))
        if self.job:
            nameParts.append(str(self.job))
        if self.nick:
            nameParts.append('\"'+self.nick+'\"')
        if self.owner:
            nameParts.append('('+str(self.owner)+')')

        name = ''

        for namePart in nameParts:
            if name != '':
                name += ' '

            name += namePart

        self.title = name

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
            self.status = "LOST"
            report = "The **"+str(self)+'** has been lost.'
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

    # 'TraitName':{
        #     'title':'TITLE',
        #     'description':'DESC',
        #     'type':'TYPE',
        #     'certs':'CERTS',
        #     'skillsets':'SKILLSET_LIST',
        #     'inv_args':'INV_ARGS_DICT',
        #     'play_cost':'PLAY_COST_DICT',
        #     'stats':'STATS_DICT',
        #     'upkeep':'UPKEEP_DICT',
        #     'die_set':'DIE_SET_LIST'
        # },


    def addTrait(self, trait_name):
        if not self.hasTrait(trait_name):
            trait = trait_kits_dict[trait_name]
            #rework to be modular
            if trait['title'] not in self.title:
                if trait['trait'] != 'effect':
                    if trait.trait_type == 'class':
                        self.job = trait_name
                        self.regenName()
                    elif trait.trait_type == 'race':
                        self.race = trait_name
                        self.regenName()
                else:
                    self.effects.append(trait.trait_title)
            if trait['certs']:
                for cert in trait['certs']:
                    self.addCert(cert)
            if trait['stats']:
                for mod_stat in trait['stats'].keys():
                    value = trait['stats'][mod_stat]
                    self.stats[mod_stat] += value
                    self.statcaps[mod_stat] += value
                    if self.statcaps[mod_stat] < 0:
                        self.stats[mod_stat] = 0
                        self.statcaps[mod_stat] = 0
            if trait['play_cost']:
                for mod_res in trait['play_cost'].keys():
                    mod_res_obj = theJar['resources'][mod_res]
                    value = trait['play_cost'][mod_res_obj]
                    try:
                        self.play_cost[mod_res_obj] += value
                    except:
                        self.play_cost[mod_res_obj] = value
            if trait['upkeep']:
                for mod_upkeep in trait['upkeep'].keys():
                    resource = theJar['resources'][mod_upkeep]
                    value = trait['upkeep'][mod_upkeep]
                    try:
                        self.upkeep[resource] += value
                    except:
                        self.upkeep[resource] = value
                    if self.upkeep[resource] < 0:
                        self.upkeep[resource] = 0
            if trait['inv_args']:
                inv = self.inventory
                for key in trait['inv_args'].keys():
                    value = trait['inv_args'][key]
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
            if trait['die_set']:
                new_set = self.die_list + trait['die_set']
                self.die_list = new_set
                self.die_set = Dice(new_set)
            if trait['skillsets']:
                self.skillsets[trait_name] = trait['skillsets']
            self.traits.append(trait_name)

    def delTrait(self, trait_name):
        if self.hasTrait(trait_name):
            trait = trait_kits_dict[trait_name]
            if trait['title'] not in self.title:
                if trait['type'] != 'effect':
                    if trait['type'] == 'class':
                        self.job = None
                        self.regenName()
                    elif trait['type'] == 'race':
                        self.race = None
                        self.regenName()
                else:
                    self.effects.remove(trait['title'])
            if trait['certs']:
                for cert in trait['certs']:
                    self.delCert(cert)
            if trait['stats']:
                for mod_stat in trait['stats'].keys():
                    value = trait['stats'][mod_stat]
                    self.stats[mod_stat] += -value
                    self.statcaps[mod_stat] += -value
                    if self.statcaps[mod_stat] < 0:
                        self.stats[mod_stat] = 0
                        self.statcaps[mod_stat] = 0
            if trait['play_cost']:
                for mod_res in trait['play_cost'].keys():
                    mod_res_obj = theJar['resources'][mod_res]
                    value = trait['play_cost'][mod_res_obj]
                    try:
                        self.play_cost[mod_res_obj] += -value
                    except:
                        self.play_cost[mod_res_obj] = -value
            if trait['upkeep']:
                for mod_upkeep in trait.trait_upkeep_dict.keys():
                    resource = theJar['resources'][mod_upkeep]
                    value = trait['upkeep'][mod_upkeep]
                    try:
                        self.upkeep[resource] += -value
                    except:
                        self.upkeep[resource] = -value
                    if self.upkeep[resource] < 0:
                        self.upkeep[resource] = 0
            if trait['inv_args']:
                inv = self.inventory
                for key in trait['inv_args'].keys():
                    value = trait['inv_args'][key]
                    if key == 'cont':
                        inv.cont += -value
                    elif key == "cap":
                        for type in value.keys():
                            mod = value[type]
                            inv.cap[type] += -mod
                    elif key == "slotcap":
                        for type in value.keys():
                            mod = value[type]
                            inv.slotcap[type] += -mod

                    else:
                        print("Error: Invalid inventory constraint.")
            if trait['die_set']:
                for die in trait['die_set']:
                    self.die_list.remove(die)
                self.die_set = Dice(self.die_list)
            if trait['skillsets']:
                del self.skillsets[trait_name]
            self.traits.remove(trait_name)

    def hasTrait(self, trait_name):
        has = False
        if trait_name in self.traits:
            has = True
        return has

    def getTrait(self, trait_name):
        trait = trait_kits_dict[trait_name]
        return trait

    def hasTraitType(self, type):
        has = False
        for trait_name in self.traits:
            trait = self.getTrait(trait_name)
            if trait['type'] == type:
                has = True
        return has

    def getTraitbyType(self, type):
        trait_name_list = []
        for trait_name in self.traits:
            trait = self.getTrait(trait_name)
            if trait['type'] == type:
                trait_name_list.append(trait_name)
        return trait_name_list

    def hasCert(self, cert_name):
        has = False
        if cert_name in self.certs:
            has = True
        return has

    def addCert(self, cert_name):
        if not cert_name in self.certs:
            self.certs.append(cert_name)

    def delCert(self, cert_name):
        if cert_name in self.certs:
            remove = True
            for trait_name in self.traits:
                trait = self.getTrait(trait_name)
                if cert_name in trait['certs']:
                    remove = False
            if remove:
                self.certs.remove(cert_name)

    def triggerSkill(self, trigger, arg_list):
        if self.skillsets:
            for skillset in self.skillsets:
                if trigger in skillset.triggers:
                    report = None
                    if trigger == 'on_act':
                       report = skillset.act(arg_list)
                    if trigger == 'on_play':
                       report = skillset.play(arg_list)
                    if trigger == 'on_work':
                       report = skillset.work(arg_list)
                    if trigger == 'on_move':
                       report = skillset.move(arg_list)
                    if trigger == 'on_battle':
                       report = skillset.battle(arg_list)
                    if trigger == 'on_attack':
                       report = skillset.attack(arg_list)
                    if trigger == 'on_defend':
                       report = skillset.defend(arg_list)
                    if trigger == 'on_death':
                       report = skillset.death(arg_list)
                    if trigger == 'on_harvest':
                       report = skillset.harvest(arg_list)
                    if trigger == 'on_refresh':
                       report = skillset.refresh(arg_list)
                    if report:
                        return report


    def unitCanMove(self, dest_type, destination):
        can_move = False
        report = ''
        if self.status == 'Played':
            if self.stats['Endurance'] > 0:
                if dest_type == 'district':
                    if destination in self.location.paths:
                        can_move = True
                if dest_type == 'unit':
                    if self.location == destination.location:
                        can_move = True
                if dest_type == 'building':
                    if self.location == destination.location:
                        can_move = True
            else:
                report = "Error: This unit does not have the Endurance."
        else:
            report = "Error: This unit has not yet been played."
        return can_move, report

    def moveUnit(self, dest_type, destination):
        move_report = None
        can_move, report = self.unitCanMove(dest_type, destination)
        if can_move:
            slot_count = len(destination.inventory.slots['unit'])
            slotcap = destination.inventory.slotcap['unit']
            if slot_count < slotcap:
                move_arg_list = [self, self.location, destination]
                move_report = self.triggerSkill('on_move', move_arg_list)

                destination.inventory.addCardToSlot(self, 'unit')
                self.location.inventory.removeCardFromSlot(self, 'unit')
                self.location = destination
                self.setStat('Endurance', -1)

                report = "Unit moved successfully."
            else:
                report = "Error: This destination does not have the required space."
        else:
            report = "Error: This destination is too far."
        if move_report:
            report += +"\n"+move_report
        return can_move, report

    def harvest(self):
        if self.status == "Played":
            #player = player_dict[self.owner.id]
            def_dinged = 0
            for resource in self.upkeep.keys():
                quantity = self.upkeep[resource]
                i = 0
                while i < quantity:
                    if not self.inventory.addResource(resource, -1):
                        def_dinged += 1
                    i += 1

            if def_dinged > 0:
                self.setStat('Defense', -def_dinged)

            if self.stats['Defense'] > 0:
                def_report = "Your **"+str(self)+'** has lost '+str(def_dinged)+' Defense due to lacking required resources.'
            else:
                def_report = "Your **"+str(self)+'** has no Defense remaining.'
            hit, report_dict = self.die_set.roll_math(self.stats['Defense']+self.stats['Fortitude'])

            harvest_arg_list = [self, def_dinged, hit]
            harvest_report = self.triggerSkill('on_harvest', harvest_arg_list)

            if hit:
                health_report = self.setHealth(-1)
            else:
                health_report = "Your **"+str(self)+'** has sustained no damage.'

            title = "-----"+str(self)+" Upkeep Results-----"
            report = "- Rolled: "+str(self.die_set)+" ("+str(self)+")\n"+\
                     "- Rolls: "+str(report_dict['rolls'])+"\n"+\
                     "- Defense + Fortitude: "+str(report_dict['threshold'])+"\n"+\
                     "- Damage Taken: "+str(report_dict['hit_count'])+"\n\n"+\
                     def_report+"\n"+health_report
            if harvest_report:
                report += "\n"+harvest_report


            return report, title


    def refresh(self):
        if self.status == "Played":
            self.setStat('Endurance', self.statcaps['Endurance'])
            refresh_arg_list = [self]
            refresh_report = self.triggerSkill('on_refresh', refresh_arg_list)
            return refresh_report


    def addBuildingToUnitInv(self, kit_title):
        can_add = self.inventory.capMathCard('building')
        if can_add == True:
            kit = [k for k, v in building_kits_dict.items() if v['title'] == kit_title]
            bldg = self.inventory.cards['building'].append(Building(*building_kits_dict[kit]))
        return can_add, bldg

    def __str__(self):
        return self.title

    def drop_rep(self):
        location = str(self.location)
        if location == 'None':
            location = 'Hand'

        rep = self.title+" ("+location+")\n"
        rep += '  '

        first = True

        for key in self.stats.keys():
            value = self.stats[key]
            cap = self.statcaps[key]
            if not first:
                rep += ', '

            rep += str(key)[0]+" "+str(value)+"/"+str(cap)+", "
            first = False
            
        return rep


    def report(self):
        fields = []
        title = "-----"+self.title+"-----"

        report = self.description

        info_rep = {'inline':True}
        info_rep['title'] = '-- Info:'
        info_rep['value'] =  "\n- Status: "+str(self.status)+\
                             "\n- Location: "+str(self.location)+\
                             "\n- Traits: "+str(self.traits)
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


class Squad():
    def __init__(self, units):
        self.units = None

        if len(units) < 5:
            self.units = units

            self.location = self.units[0].location

            for unit in self.units:
                unit.squad = self

            self.priority = 1
            self.rank = None
            self.owner = self.units[0].owner
            self.owner.squads.append(self)
            self.allegiance = self.owner.allegiance
            self.location.civics.squad_list.append(self)
            self.location.civics.addPlayer(self.owner)
            self.setPriority(self.priority)

            self.nick = self.units[0].title +"'s Squad"

            self.uniqueID = str(theJar['nextUniqueID'])
            theJar['nextUniqueID'] += 1
        else:
            print('Units list too long!')

    def addUnit(self, unit):
        if len(self.units) < 4:
            self.units.append(unit)
            unit.squad = self

    def setNick(self, nick):
        self.nick = nick

    def setPriority(self, priority):
        priority = int(priority)
        if priority > 99:
            priority = 99
        if priority < 0:
            priority = 1
        self.setRank(priority)
        self.priority = priority

    def setRank(self, newpriority):
        try:
            loc = self.location.civics.squads_ranked[self.allegiance]
        except:
            loc = self.location.civics.squads_ranked[self.allegiance] = {}
        if self.rank:
            try:
                loc[self.priority].remove(self)
            except:
                pass
        try:
            loc[newpriority].append(self)
        except:
            loc[newpriority] = [self]
        self.rank = newpriority+loc[newpriority].index(self)
        self.location.civics.getCommander(self.allegiance)

    def moveSquad(self, dest_type, destination):
        squad_move = True
        checks = []
        for unit in self.units:
            can_move, report = unit.unitCanMove(dest_type, destination)
            checks.append(can_move)

        if False in checks:
            squad_move = False
        slot_count = len(destination.inventory.slots['unit'])
        slotcap = destination.inventory.slotcap['unit']
        if slotcap-slot_count < len(self.units):
            squad_move = False

        if squad_move:
            for unit in self.units:
                unit.moveUnit(dest_type, destination)
            self.location.civics.delPlayer(self.owner)
            self.location.civics.delSquad(self)
            self.location = self.units[0].location
            self.location.civics.addPlayer(self.owner)
            self.location.civics.addSquad(self)
            report = self.nick+" has moved successfully."
        else:
            report = self.nick+" is unable to move."

        return report

    def __str__(self):
        return self.nick

    def drop_rep(self):
        strng = self.nick+"("+str(len(self.units))+"/4)"
        return strng

    def report(self):
        fields = []
        title = "-----"+self.nick+"-----"
        report = ''
        info_rep = {'inline':True}
        info_rep['title'] = '-- Info:'
        info_rep['value'] =  "\n- Name: "+str(self.nick)+\
                             "\n- Location: "+str(self.location)+\
                             "\n- Priority: "+str(self.priority)+\
                             "\n- Rank: "+str(self.rank)
        info_rep['value'] += "\n- Units: "
        for unit in self.units:
            value = unit.title
            info_rep['value'] += str(value)+"\n"
        info_rep['value'] = info_rep['value'][:-2]
        fields.append(info_rep)
        return report, title, fields

from _00_cogs.mechanics.building_classes.__building_parent_class import Building
