from _02_global_dicts import region_dict, district_dict
from _00_cogs.architecture.inventory_class import Inventory
from _00_cogs.mechanics.unit_classes.__unit_parent_class import Unit
#from _00_cogs.mechanics.unit_classes.__building_parent_class import Building

class Region():
    def __init__(self, name):
        self.name = name
        self.districts = []
        region_dict[name] = self

    def addDistrict(self, district):
        self.districts.append(district)

    def __str__(self):
        return self.name

    def report(self):
        report = "-----"+str(self)+"-----\n\n"
        report += "--Districts:\n"
        for district in self.districts:
            report += "-"+str(district)+"\n"

        return report

class District():
    def __init__(self, name, region_name, size, paths=None):
        self.name = name
        self.region = region_name
        self.paths = []
        self.players = []

        sizes = {
            #inv_args: [r_cap=None, r_cont=None, u_cap=None, b_cap=None, u_slotcap=None, b_slotcap=None]
            'tiny': [self, 1000, None, 100, 100, 2, 0],
            'small': [self, 1000, None, 100, 100, 5, 2],
            'medium': [self, 1000, None, 100, 100, 8, 4],
            'large': [self, 1000, None, 100, 100, 13, 8],
            'huge': [self, 1000, None, 100, 100, 20, 14],
        }
        self.inventory = Inventory(*sizes[size])

        if paths:
            paths = paths.split(',')
            paths = [i for i in paths if i != '']
            for path in paths:
                district = district_dict[path]
                self.setPath(district)

        region_dict[region_name].addDistrict(self)
        district_dict[name] = self

    def setPath(self, target):
        if target not in self.paths:
            self.paths.append(target)
        if self not in target.paths:
            target.paths.append(self)

    def __str__(self):
        return self.name

    def addCard(self, card_kit, card_type):
        inv = self.inventory
        can_add = inv.capMathCard(card_type)
        if can_add == True:
            card = None
            kit = [self]+card_kit
            if card_type == 'unit':
                card = Unit(*kit)
            elif card_type == 'building':
                #card = Building(*kit)
                print("no")
            if card:
                inv.cards[card_type].append(card)
            else:
                can_add = False
        return can_add

    def report(self):
        report = "-----"+str(self)+"-----\n"
        report += "---"+str(self.region)+"\n\n"
        report += "--Paths:\n"
        for district in self.paths:
            report += "-"+str(district)+"\n"
        report+"\n\n"+self.inventory.report()
        return report
