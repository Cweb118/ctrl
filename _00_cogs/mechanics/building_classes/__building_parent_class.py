from _00_cogs.mechanics._cards_class import Card
from _00_cogs.mechanics.building_classes._building_kits import building_kits_dict
from _02_global_dicts import theJar

class Building(Card):
    def __init__(self, owner, title, description, inv_args, traits, logic_args, play_cost, stats, worker_req, input_dict, output_dict, cat_dict, priority=0):
        inv_args = [self]+inv_args
        super().__init__(owner, title, description, inv_args=inv_args, play_cost=play_cost)

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

        self.trait_list = traits
        self.traits = {
            'on_play': [],
            'on_work': [],
            'on_move': [],
            'on_battle': [],
            'on_attack': [],
            'on_defend': [],
            'on_death': [],
            'on_act': [],
        }
        for trait_name in traits:
            self.addTrait(trait_name)

        self.logic_args = logic_args
        self.worker_req = worker_req
        self.input = input_dict
        self.output = output_dict
        self.catalyst = cat_dict

        self.links = []
        self.priority = priority

    #TODO: ADD addTrait and delTrait

    def addBuilding(self, card_kit_id, inv_owner, owner_type):
        inv = theJar[owner_type][inv_owner].inventory
        can_add = inv.capMathCard('building')
        if can_add == True:
            kit = [inv_owner]+building_kits_dict[card_kit_id]
            card = Building(*kit)
            if card:
                inv.cards['building'].append(card)
            else:
                can_add = False
        return can_add, card


    def checkReqs(self):
        can_run = True
        report = "**"+str(self)+"** has run successfully."
        if self.input:
            for res in self.input:
                res_obj = theJar['resources'][res]
                needed = self.input[res]
                have = self.inventory.resources[res_obj]
                if have < needed:
                    can_run = False
                    report = "Error: **"+str(self)+"** lacks required input resources."

        if self.output:
            for res in self.output:
                res_obj = theJar['resources'][res]
                given = self.output[res]
                have = self.inventory.resources[res_obj]
                max = self.inventory.cap['resource']
                if have + given > max:
                    can_run = False
                    report = "Error: **"+str(self)+"** has insufficient space for output."

        if self.catalyst:
            for res in self.catalyst:
                res_obj = theJar['resources'][res]
                needed = self.catalyst[res]
                have = self.inventory.resources[res_obj]
                if have < needed:
                    can_run = False
                    report = "Error: **"+str(self)+"** lacks required catalytic resources."

        if self.inventory.slotcap['unit'] > 0:
            if len(self.inventory.slots['unit']) != self.inventory.slotcap['unit']:
                can_run = False
                report = "Error: **"+str(self)+"** lacks required workers."
        return can_run, report

    def doInput(self):
        if self.input:
            for res in self.input:
                res_obj = theJar['resources'][res]
                needed = self.input[res]
                self.inventory.addResource(res_obj, -needed)

    def doOutput(self):
        for res in self.output:
            res_obj = theJar['resources'][res]
            gain = self.output[res]
            if len(self.links) > 0:
                link_give = self.links[0].inventory.addResource(res_obj, gain)
                if not link_give:
                    self.inventory.addResource(res_obj, gain)
            else:
                self.inventory.addResource(res_obj, gain)

    def run(self):
        if self.output:
            can_run, req_report = self.checkReqs()
            if can_run:
                self.doInput()
                self.doOutput()
                if len(self.traits['on_work']) > 0:
                    for trait in self.traits['on_work']:
                        workers = self.inventory.slots['units']
                        args = [self, workers]+self.logic_args
                        trait.action.work(*args)
                report = "**"+str(self) + "** has run successfully."
            else:
                report = req_report
            return report

    def addLink(self, receiver_building):
        if len(self.links) == 0:
            self.links.append(receiver_building)
            if self.priority <= receiver_building.priority:
                self.priority = receiver_building.priority + 1

    def delLink(self, receiver_building):
        if receiver_building in self.links:
            self.links.remove(receiver_building)

    def harvest(self):
        report = ''
        if len(self.traits['on_harvest']) > 0:
            for trait in self.traits['on_harvest']:
                action_report = trait.action.harvest()
                if action_report:
                    report += action_report
        return report

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
            self.status = "DESTROYED"
            report = "The **"+str(self)+'** has been destroyed.'
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
        str = self.title+"("+self.location+")\n"
        str += "Workers: x/x, Input: xy/xy, Output: xy/xy, Catalyst: xy"
        return str

    def report(self):
        title = "-----"+self.title+"-----"
        report = self.description
        fields = []
        info_rep = {'inline':True}
        info_rep['title'] = '-- Info:'
        info_rep['value'] = "- Status: "+str(self.status)+\
                 "\n- Location: "+str(self.location)+\
                 "\n- Traits: "+str(self.trait_list)
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
        if self.worker_req:
            for req in self.worker_req:
                req_rep['value'] += "- "+str(req)+"\n"
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

