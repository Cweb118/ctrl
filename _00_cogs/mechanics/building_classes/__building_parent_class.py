from _00_cogs.mechanics._cards_class import Card
from _00_cogs.mechanics.building_classes._building_kits import building_kits_dict
from _00_cogs.mechanics.dice_class import Dice
from _00_cogs.mechanics.trait_classes.trait_kits import trait_kits_dict
from _02_global_dicts import theJar

class Building(Card):
    def __init__(self, bk, priority=0):

        inv_args = [self]+bk['inv_args']
        super().__init__(bk['title'], bk['description'], inv_args=inv_args, play_cost=bk['play_cost'])
        stats = bk['stats']
        self.stats = {
            'Attack':stats['attack'],
            'Health':stats['health'],
            'Defense':stats['defense'],
            'Size':stats['size'],

        }
        self.statcaps = {
            'Attack':stats['attack'],
            'Health':stats['health'],
            'Defense':stats['defense'],
            'Size':stats['size'],
        }

        self.traits = []
        self.skillsets = {}
        #This is a hot mess because its trying to do this by trait but it only gets one singular mechanics arg from the kit
        self.operations = bk['mechanics']
        self.certs = bk['worker_req']

        self.input = bk['input_dict']
        self.output = bk['output_dict']
        self.catalyst = bk['cat_dict']

        self.links = []
        self.priority = priority

        if bk['mechanics']:
            for trait_name in bk['mechanics'].keys():
                self.addTrait(trait_name)

    # def addBuilding(self, card_kit_id, inv_owner, owner_type):
    #     #defunct?
    #     inv = theJar[owner_type][inv_owner].inventory
    #     can_add = inv.capMathCard('building')
    #     if can_add == True:
    #         kit = [inv_owner]+building_kits_dict[card_kit_id]
    #         card = Building(*kit)
    #         if card:
    #             inv.cards['building'].append(card)
    #         else:
    #             can_add = False
    #     return can_add, card

    def addUnitToBuildingInv(self):
        can_add = self.inventory.capMathCard('unit')
        if can_add == True:
            unit = self.inventory.cards['unit'].append(Unit())
        return can_add, unit

    def checkReqs(self):
        can_run = True
        report = "**"+str(self)+"** has run successfully."
        if self.input:
            for res in self.input:
                res_obj = res
                needed = self.input[res]
                have = self.inventory.resources[res_obj]
                if have < needed:
                    can_run = False
                    report = "Error: **"+str(self)+"** lacks required input resources."

        if self.output:
            for res in self.output:
                res_obj = res
                given = self.output[res]
                have = self.inventory.resources[res_obj]
                max = self.inventory.cap['resource']
                if have + given > max:
                    can_run = False
                    report = "Error: **"+str(self)+"** has insufficient space for output."

        if self.catalyst:
            for res in self.catalyst:
                res_obj = res
                needed = self.catalyst[res]
                have = self.inventory.resources[res_obj]
                if have < needed:
                    if res == 'Vessel':
                        for unit in self.inventory.slots['units']:
                            if not unit.hasTrait('Charged'):
                                can_run = False
                    else:
                        can_run = False
                    report = "Error: **"+str(self)+"** lacks required catalytic resources."
        if self.inventory.slotcap['unit']:
            if self.inventory.slotcap['unit'] > 0:
                if len(self.inventory.slots['unit']) != self.inventory.slotcap['unit']:
                    can_run = False
                    report = "Error: **"+str(self)+"** lacks required workers."
        return can_run, report

    def doInput(self):
        if self.input:
            for res in self.input:
                res_obj = res
                needed = self.input[res]
                self.inventory.addResource(res_obj, -needed)

    def doOutput(self):
        if self.output:
            for res in self.output:
                res_obj = res
                gain = self.output[res]
                if len(self.links) > 0:
                    link_give = self.links[0].inventory.addResource(res_obj, gain)
                    if not link_give:
                        self.inventory.addResource(res_obj, gain)
                else:
                    self.inventory.addResource(res_obj, gain)

    async def run(self):
        can_run, req_report = self.checkReqs()
        if can_run:
            self.doInput()
            self.doOutput()
            report = "**"+str(self) + "** has run successfully."

            for trait in self.traits:
                print(trait)
                self_work_report = await self.triggerWorkSkill(trait)
                report += '\n\n' +self_work_report

            for worker in self.inventory.slots['unit']:
                workers = self.inventory.slots['unit']
                work_arg_list = [self, worker, workers]
                worker_work_report = await worker.triggerSkill('on_work', work_arg_list)
                if worker_work_report:
                    report += '\n\n' +worker_work_report

        else:
            report = req_report
        return report

    async def triggerWorkSkill(self, trait_name):
        skillset = self.skillsets[trait_name]
        print(skillset)
        if 'on_work' in skillset.triggers:
            logic_args = self.operations[trait_name]
            work_args = [self, self.inventory.slots['units']]+logic_args
            try:
                report = await skillset.work(work_args)
            except:
                report = skillset.work(work_args)
            return report


    def addLink(self, receiver_building):
        if len(self.links) == 0:
            self.links.append(receiver_building)
            if self.priority <= receiver_building.priority:
                self.priority = receiver_building.priority + 1

    def delLink(self, receiver_building):
        if receiver_building in self.links:
            self.links.remove(receiver_building)

    def addTrait(self, trait_name):
        if not self.hasTrait(trait_name):
            trait = trait_kits_dict[trait_name]
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
                    mod_res_obj = mod_res
                    value = trait['play_cost'][mod_res_obj]
                    try:
                        self.play_cost[mod_res_obj] += value
                    except:
                        self.play_cost[mod_res_obj] = value
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
                self.operations[trait_name] = trait['skillsets']

    def delTrait(self, trait_name):
        if self.hasTrait(trait_name):
            trait = trait_kits_dict[trait_name]
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
                    mod_res_obj = mod_res
                    value = trait['play_cost'][mod_res_obj]
                    try:
                        self.play_cost[mod_res_obj] += -value
                    except:
                        self.play_cost[mod_res_obj] = -value
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


    async def harvest(self):
        report = ''
        title = ''
        harvest_arg_list = [self, None, None]
        harvest_report = await self.triggerSkill('on_harvest', harvest_arg_list)
        if harvest_report:
            report += harvest_report
        else:
            report = None
        return report, title

    async def refresh(self):
        report = ''
        title = ''
        refresh_arg_list = [self]
        refresh_report = await self.triggerSkill('on_refresh', refresh_arg_list)
        if refresh_report:
            report += refresh_report
        else:
            report = None
        return report, title

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
            new_def_def = self.setStat('Defense', -attack_value)
            health_rep = "The **"+str(self)+"'s** Defense has been lowered to "+str(new_def_def)
        else:
            health_rep = self.setHealth(-attack_value)
        return health_rep

    def __str__(self):
        return self.title

    def drop_rep(self):
        location = str(self.location)
        if location == 'None':
            location = 'Hand'

        rep = self.title+" ("+location+")\n  "
        rep += "Workers: "+str(len(self.inventory.slots['unit']))+"/"+str(self.inventory.slotcap['unit'])
        return rep

    def report(self):
        title = "-----"+self.title+"-----"
        report = self.description
        fields = []
        info_rep = {'inline':True}
        info_rep['title'] = '-- Info:'
        info_rep['value'] = "- Status: "+str(self.status)+\
                 "\n- Location: "+str(self.location)
        if self.operations:
             info_rep['value'] +="\n- Operations: "+str(self.operations.keys())
        else:
            info_rep['value'] +="\n- Operations: None"
        fields.append(info_rep)

        stats_rep = {'inline':True}
        stats_rep['title'] = "-- Stats:"
        stats_rep['value'] = ''
        for key in self.stats.keys():
            value = self.stats[key]
            cap = self.statcaps[key]
            stats_rep['value'] += "- "+str(key)+": "+str(value)+"/"+str(cap)+"\n"
        stats_rep['value'] = stats_rep['value'][:-1]
        fields.append(stats_rep)

        req_rep = {'inline':False}
        req_rep['title'] = "-- Worker Requirements:"
        req_rep['value'] = ''
        if self.certs:
            for cert in self.certs():
                req_rep['value'] += "- "+str(cert)+"\n"
            req_rep['value'] = req_rep['value'][:-1]
        else:
            req_rep['value'] = "- None"
        fields.append(req_rep)

        input_rep = {'inline':False}
        input_rep['title'] = "-- Input:"
        input_rep['value'] = ''
        if self.input:
            for key in self.input.keys():
                value = self.input[key]
                input_rep['value'] += "- "+str(value)+" "+str(key) +"\n"
            input_rep['value'] = input_rep['value'][:-1]
        else:
            input_rep['value'] = "- None"
        fields.append(input_rep)

        if self.catalyst:
            cat_rep = {'inline':False}
            cat_rep['title'] = "-- Required Catalyst:"
            cat_rep['value'] = ''
            for key in self.catalyst.keys():
                value = self.catalyst[key]
                cat_rep['value'] += "- "+str(value)+" "+str(key) +"\n"
            cat_rep['value'] = cat_rep['value'][:-1]
            fields.append(cat_rep)

        output_rep = {'inline':False}
        output_rep['title'] = "-- Output:"
        output_rep['value'] = ''
        if self.output:
            for key in self.output.keys():
                value = self.output[key]
                output_rep['value'] += "- "+str(value)+" "+str(key) +"\n"
            output_rep['value'] = output_rep['value'][:-1]
        else:
            output_rep['value'] = "- None"
        fields.append(output_rep)

        if len(self.links) > 0:
            links_rep = {'inline':False}
            links_rep['title'] = "-- Production Receptacles:"
            links_rep['value'] = ''
            for link in self.links:
                links_rep['value'] += "- "+str(link)
            fields.append(links_rep)

        inv_report, inv_title, inv_fields = self.inventory.report()
        fields += inv_fields
        return report, title, fields

from _00_cogs.mechanics.unit_classes.__unit_parent_class import Unit
