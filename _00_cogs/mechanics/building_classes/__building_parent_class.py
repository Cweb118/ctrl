from _00_cogs.mechanics._cards_class import Card
from _02_global_dicts import resource_dict

class Building(Card):
    def __init__(self, owner, title, description, inv_args, traits, play_cost, stats, worker_req, input_dict, output_dict, cat_dict):
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

        self.worker_req = worker_req
        self.input = input_dict
        self.output = output_dict
        self.catalyst = cat_dict


    def checkReqs(self):
        can_run = True
        if self.input:
            for res in self.input:
                res_obj = resource_dict[res]
                needed = self.input[res]
                have = self.inventory.resources[res_obj]
                if have < needed:
                    can_run = False

        if self.catalyst:
            for res in self.catalyst:
                res_obj = resource_dict[res]
                needed = self.catalyst[res]
                have = self.inventory.resources[res_obj]
                if have < needed:
                    can_run = False

        if self.inventory.slotcap['unit'] > 0:
            if len(self.inventory.slots['unit']) != self.inventory.slotcap['unit']:
                can_run = False
        print(can_run)
        return can_run

    def doInput(self):
        if self.input:
            for res in self.input:
                res_obj = resource_dict[res]
                needed = self.input[res]
                self.inventory.addResource(res_obj, -needed)

    def doOutput(self):
        for res in self.output:
            res_obj = resource_dict[res]
            gain = self.output[res]
            self.inventory.addResource(res_obj, gain)

    def run(self):
        if self.output:
            if self.checkReqs():
                self.doInput()
                self.doOutput()
                report = str(self) + " has run successfully."
            else:
                report = "Error: " +str(self)+ " lacked one or more requirements."
            return report


    def setStat(self, stat, quantity):
        self.stats[stat] += quantity
        if self.stats[stat] < 0:
            self.stats[stat] = 0
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

        report += "\n\n"+self.inventory.report()
        return report

