from _02_global_dicts import region_dict, district_dict

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
    def __init__(self, name, region, paths=None):
        self.name = name
        self.region = region
        self.paths = []
        self.buildings = []

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
