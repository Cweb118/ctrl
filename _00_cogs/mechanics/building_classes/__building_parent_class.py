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
            kit = [self]+building_kits_dict[card_kit_id]
            card = Building(*kit)
            if card:
                inv.cards['building'].append(card)
            else:
                can_add = False
        return can_add, card


    def checkReqs(self):
        can_run = True
        if self.input:
            for res in self.input:
                res_obj = theJar['resources'][res]
                needed = self.input[res]
                have = self.inventory.resources[res_obj]
                if have < needed:
                    can_run = False
                    report = "Error: "+str(self)+" lacks required input resources."

        if self.output:
            for res in self.output:
                res_obj = theJar['resources'][res]
                given = self.output[res]
                have = self.inventory.resources[res_obj]
                max = self.inventory.cap['resource']
                if have + given > max:
                    can_run = False
                    report = "Error: "+str(self)+" has insufficient space for output."

        if self.catalyst:
            for res in self.catalyst:
                res_obj = theJar['resources'][res]
                needed = self.catalyst[res]
                have = self.inventory.resources[res_obj]
                if have < needed:
                    can_run = False
                    report = "Error: "+str(self)+" lacks required catalytic resources."

        if self.inventory.slotcap['unit'] > 0:
            if len(self.inventory.slots['unit']) != self.inventory.slotcap['unit']:
                can_run = False
                report = "Error: "+str(self)+" lacks required workers."
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
                report = str(self) + " has run successfully."
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
            report = "The "+str(self)+' has been destroyed.'
        else:
            report = "The "+str(self)+' now has '+str(self.stats['Health'])+' Health.'
        return report

    def dmg(self, attack_value):
        if self.stats['Defense'] > 0:
            new_def_def = self.setStat('Defense', -attack_value)
            health_rep = "The "+str(self)+"'s Defense has been lowered to "+str(new_def_def)
        else:
            health_rep = self.setHealth(-attack_value)
        return health_rep

    def __str__(self):
        return self.title

    def report(self):
        report = "-----Building Report-----\n"+\
                 "\nTitle: "+self.title+\
                 "\nDescription: "+self.description+\
                 "\nStatus: "+str(self.status)+\
                 "\nLocation: "+str(self.location)+\
                 "\nTraits: "+str(self.trait_list)+\
                 "\nStats: "
        for key in self.stats.keys():
            value = self.stats[key]
            cap = self.statcaps[key]
            report += str(value)+"/"+str(cap)+" "+str(key)+", "
        report = report[:-2]
        report += "\n"


        if self.worker_req:
            report += "\nWorker Requirements: " + str(self.worker_req)

        if self.input:
            report += "\nInput: "
            for key in self.input.keys():
                value = self.input[key]
                report += str(value)+" "+str(key) +", "
            report = report[:-2]

        if self.output:
            report += "\nOutput: "
            for key in self.output.keys():
                value = self.output[key]
                report += str(value)+" "+str(key) +", "
            report = report[:-2]

        if self.catalyst:
            report += "\nRequired Catalyst: "
            for key in self.catalyst.keys():
                value = self.catalyst[key]
                report += str(value)+" "+str(key) +", "
            report = report[:-2]

        if len(self.links) > 0:
            report += "\nProduction Receptacles: " + str(self.links[0])

        report += "\n\n"+self.inventory.report()
        return report

