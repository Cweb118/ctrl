from _00_cogs.mechanics._cards_class import Card

class Unit(Card):
    def __init__(self, owner, title, description, inv_args, traits, play_cost, stats, input_dict, output_dict, cat_dict):
        inv_args = [owner]+inv_args
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

        self.input = input_dict
        self.output = output_dict
        self.catalyst = cat_dict

        input = {}
#Inherits from: Card

#Name: Str
#Description: Str

#Attack: Int
#Defence: Int
#Size: Int
#Age: Str
#Affinity: Str

#input_quantity: Int
#input_obj: Item/Unit instance

#output_quantity: Int
#output_obj: Item/Unit instance

#catylist_quantity: Int
#catylist_obj: Item/Unit instance

