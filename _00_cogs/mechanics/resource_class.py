from _02_global_dicts import resource_dict

class Resource():
    def __init__(self, title, description, type):
        self.title = title
        self.description = description
        self.type = type #Fluid, Solid, Energy, Abstract

        resource_dict[title] = self

    def report(self):
        report = "Resource: "+self.title+\
                "\nType: "+self.type+\
                 "\nDescription: "+self.description
        return report

    def __str__(self):
        return str(self.title)

resource_kits_dict = {
    'Influence':("Influence", "A representation of your favor with the people.", "Abstract"),
    'Water':("Water", "Its wet and refreshing.", "Fluid"),
    'Food':("Food", "A mere morsel, but it will do.", "Solid"),
    'Metal':("Metal", "Scrap metal. Its hard to work with, but durable.", "Solid"),
    'Wood':("Wood", "Hardwood. Its easy to work with, but not as strong.", "Solid"),
}

for key in resource_kits_dict.keys():
    kit = resource_kits_dict[key]
    res = Resource(*kit)
