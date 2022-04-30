from _00_cogs.architecture.inventory_class import Inventory
from _02_global_dicts import theJar

#-----attributes-----
class Card():
    def __init__(self, owner, title, description, inv_args=None, play_cost=None):
        self.title = title
        self.description = description
        self.owner = owner

        self.status = "Held"
        self.location = None
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

    def playerPlayCheck(self, player, target_obj):
        report = ''
        can_play = False
        card_type = type(self).__name__.lower()
        card_status = self.status
        target_type = type(target_obj).__name__.lower()
        slot_count = len(target_obj.inventory.slots[card_type])
        slotcap = target_obj.inventory.slotcap[card_type]
        if card_status == 'Held':
            if slot_count < slotcap:
                can_play = True
                if self.play_cost:
                    for key in self.play_cost.keys():
                        cost = self.play_cost[key]
                        if player._inventory.resources[theJar['resources'][key]] < cost:
                            report = "Error: You lack the required resources to play this card."
                            can_play = False
                if card_type == 'unit':
                    if player._stats[theJar['resources']['Influence']] == 0:
                        report = "Error: You lack the required influence."
                        can_play = False
                if target_type == 'district':
                    if player.location != target_obj:
                        report = "Error: You are not currently present at the designated location."
                        can_play = False
                else:
                    if player.location != target_obj.location:
                        report = "Error: You are not currently present at the designated location."
                        can_play = False
                if target_type == 'building':
                    if target_obj.worker_req:
                        certs = self.getTraitCerts()
                        for req in target_obj.worker_req:
                            if req not in certs:
                                report = "Error: This unit does not meet all requirements for the destination."
                                can_play = False
        return can_play, report

    def playerUnplayCheck(self, player):
        report = ''
        can_unplay = False
        card_status = self.status
        target_obj = self.location
        target_type = type(target_obj).__name__.lower()
        if card_status == 'Played':
            can_unplay = True
            if target_type == 'district':
                if player.location != target_obj:
                    report = "Error: You are not currently present at the designated location."
                    can_unplay = False
            else:
                if player.location != target_obj.location:
                    report = "Error: You are not currently present at the designated location."
                    can_unplay = False
        return can_unplay, report


    def fabPlayCheck(self, player, target_obj):
        report = ''
        can_play = False
        card_type = type(self).__name__.lower()
        card_status = self.status
        target_type = type(target_obj).__name__.lower()
        slot_count = len(target_obj.inventory.slots[card_type])
        slotcap = target_obj.inventory.slotcap[card_type]
        if card_status == 'Held':
            if slot_count < slotcap:
                can_play = True
                if target_type == 'building':
                    for tag in target_obj.worker_req:
                        if tag not in self.trait_list:
                            report = "Error: This unit does not meet all requirements for the destination."
                            can_play = False
        return can_play, report


    def playCard(self, player, target_obj):
        card_type = type(self).__name__.lower()
        player_type = type(player).__name__.lower()
        if player_type == 'player':
            can_play, report = self.playerPlayCheck(player, target_obj)
        else:
            can_play, report = self.fabPlayCheck(player, target_obj)

        if can_play:
            self.toggleStatus()
            if card_type == 'unit':
                if player_type == 'player':
                    player.modStat(theJar['resources']['Influence'], -1)
            if self.play_cost:
                for key in self.play_cost.keys():
                    player._inventory.addResource(theJar['resources'][key], -self.play_cost[key])
            target_obj.inventory.slots[card_type].append(self)
            self.location = target_obj
            theJar['played_cards'][card_type].append(self)
            report = str(player)+"\'s **"+str(self)+'** has been played to '+str(target_obj)
        return report

    def unplayCard(self, player):
        card_type = type(self).__name__.lower()
        player_type = type(player).__name__.lower()
        #if player_type == 'player':
        can_unplay, report = self.playerUnplayCheck(player)

        if can_unplay:
            target_obj = self.location
            self.toggleStatus()
            if card_type == 'unit':
                if player_type == 'player':
                    player.modStat(theJar['resources']['Influence'], 1)
            self.location.inventory.slots[card_type].remove(self)
            self.location = None
            theJar['played_cards'][card_type].append(self)
            report = str(self)+' has been unplayed from '+str(target_obj)
        return report

