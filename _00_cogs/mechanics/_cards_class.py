from _00_cogs.architecture.inventory_class import Inventory
from _02_global_dicts import resource_dict

#-----attributes-----
class Card():
    def __init__(self, owner, title, description, inv_args=None, play_cost=None):
        self.title = title
        self.description = description
        self.owner = owner

        self.status = "Held"

        self.play_cost = play_cost
        #Item:quantity


        if inv_args:
            self.inventory = Inventory(*inv_args)


    def toggleStatus(self):
        if self.status == "Held":
            self.status = "Played"
        elif self.status == "Played":
            self.status = "Held"

    def toggleLife(self):
        if self.status == "DEAD":
            self.status = "Held"

    def playCard(self, player, target_obj):
        can_play = False
        card_type = type(self).__name__.lower()
        card_status = self.status
        slot_count = len(target_obj.inventory.slots[card_type])
        slotcap = target_obj.inventory.slotcap[card_type]
        if card_status == 'Held':
            if slot_count < slotcap:
                influence = player.inventory.resources[resource_dict['Influence']]
                played_cards = 0
                for key in player.inventory.cards:
                    for pcard in player.inventory.cards[key]:
                        if pcard.status == 'Played':
                            played_cards += 1
                if played_cards < influence:
                    can_play = True
                    if self.play_cost:
                        for key in self.play_cost.keys():
                            cost = self.play_cost[key]
                            if player.inventory.resources[key] < cost:
                                can_play = False
        if can_play:
            self.toggleStatus()
            target_obj.inventory.slots[card_type].append(self)
        return can_play
