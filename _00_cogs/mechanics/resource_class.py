from _02_global_dicts import theJar

class Resource():
    def __init__(self, title, description, type):
        self.title = title
        self.description = description
        self.type = type #Fluid, Solid, Energy, Abstract

        #theJar['resources'][title] = self

    def report(self):
        report = "Resource: "+self.title+\
                "\nType: "+self.type+\
                 "\nDescription: "+self.description
        return report

    def __str__(self):
        return str(self.title)

resource_kits_dict = {
    'Water':("Water", "Its wet and refreshing.", "Fluid"),
    'Food':("Food", "A mere morsel, but it will do.", "Solid"),
    'Wood':("Wood", "Hardwood. Its easy to work with, but not as strong.", "Solid"),
    'Stone':("Stone", "Scrap metal. Its hard to work with, but durable.", "Solid"),
    'Coal':("Coal", "Scrap metal. Its hard to work with, but durable.", "Solid"),
    'Ore':("Ore", "Scrap metal. Its hard to work with, but durable.", "Solid"),
    'Metal':("Metal", "Scrap metal. Its hard to work with, but durable.", "Solid"),
    'Silver':("Silver", "A mere morsel, but it will do.", "Solid"),

    'Steam':("Steam", "The angriest form of water.", "Fluid"),
    'Energy':("Energy", "Pure Energy.", "Energy"),

    'Woodland Gear':("Woodland Gear", "A mere morsel, but it will do.", "Solid"),
    'Survivalist Gear':("Survivalist Gear", "A mere morsel, but it will do.", "Solid"),
    'Vessel':("Vessel", "A glowing glass box resembling a lantern, containing the most valuable thing in all of Aporia.", "Solid"),
    'Heart':("Heart", "A clockwork heart, keeping time in order to stabilize its anomalous purpose.", "Solid"),
    'Hive':("Hive", "A swarm of particles bound to The Interface.", "Solid"),
}

for key in resource_kits_dict.keys():
    if key not in theJar['resources']:
        theJar['resources'].append(key)
        #kit = resource_kits_dict[key]
        #res = Resource(*kit)
