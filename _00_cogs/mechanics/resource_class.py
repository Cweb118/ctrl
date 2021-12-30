from _02_global_dicts import resource_dict

class Resource():
    def __init__(self, title, description, type):
        self.title = title
        self.description = description
        self.type = type #Fluid, Solid, Energy, Abstract

    def report(self):
        report = "Resource: "+self.title+\
                "\nType: "+self.type+\
                 "\nDescription: "+self.description
        return report

    def __str__(self):
        return self.title

resource_kits_dict = {
    'influence':("Influence", "A representation of your favor with the people.", "Abstract"),
    'water':("Water", "Its wet and refreshing.", "Fluid"),
    'food':("Food", "A mere morsel, but it will do.", "Solid"),
    'metal':("Metal", "Scrap metal. Its hard to work with, but durable.", "Solid"),
}

for key in resource_kits_dict.keys():
    kit = resource_kits_dict[key]
    res = Resource(*kit)
    resource_dict[key] = res
