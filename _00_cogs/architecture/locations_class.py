from _02_global_dicts import region_dict, district_dict
from _00_cogs.architecture.inventory_class import Inventory

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
    def __init__(self, name, region, size, paths=None):
        self.name = name
        self.region = region
        self.paths = []
        self.players = []

        sizes = {
            #inv_args: [r_cap=None, r_cont=None, u_cap=None, b_cap=None, u_slotcap=None, b_slotcap=None]
            'tiny': [self, 999, None, 99, 99, 2, 0],
            'small': [self, 999, None, 99, 99, 5, 2],
            'medium': [self, 999, None, 99, 99, 8, 4],
            'large': [self, 999, None, 99, 99, 13, 8],
            'huge': [self, 999, None, 99, 99, 20, 14],
        }
        self.inventory = Inventory(*sizes[size])

        if paths:
            paths = paths.split(',')
            paths = [i for i in paths if i != '']
            for path in paths:
                district = district_dict[path]
                self.setPath(district)

        district_dict[name] = self

    def setPath(self, target):
        if target not in self.paths:
            self.paths.append(target)
        if self not in target.paths:
            target.paths.append(self)

    def __str__(self):
        return self.name

    def report(self):
        report = "-----"+str(self)+"-----\n"
        report += "---"+str(self.region)+"\n\n"
        report += "--Paths:\n"
        for district in self.paths:
            report += "-"+str(district)+"\n"
        report += "\n--Buildings:\n"
        for building in self.buildings:
            report += "-"+str(building)+"\n"
        return report
