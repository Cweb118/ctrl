from _00_cogs.architecture.inventory_class import Inventory
from _02_global_dicts import theJar

#-----attributes-----
class Card():
    def __init__(self, title, description, inv_args=None, play_cost=None):
        self.title = title
        self.description = description

        self.status = "Held"
        self.location = None
        self.play_cost = play_cost
        #Item:quantity

        if inv_args:
            self.inventory = Inventory(*inv_args)

        self.uniqueID = str(theJar['nextUniqueID'])
        theJar['nextUniqueID'] += 1

    def updateInterface(self):
        pass

    def toggleStatus(self):
        if self.status == "Held":
            self.status = "Played"
        elif self.status == "Played":
            self.status = "Held"

    def toggleLife(self):
        if self.status == "DEAD":
            self.status = "Held"

    def playerPlayCheck(self, player, target_obj):
        report = '...'
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
                        if player.inventory.resources[theJar['resources'][key]] < cost:
                            report = "Error: You lack the required resources to play this card."
                            can_play = False
                if player._stats['Influence'] == 0:
                    report = "Error: You lack the required influence."
                    can_play = False
                if card_type == 'building':
                    loc_gov_faction = None
                    loc_occ_faction = None
                    if target_type == 'district':
                        loc_civics = target_obj.civics
                    else:
                        loc_civics = target_obj.location.civics

                    if loc_civics.governance:
                        loc_gov_faction = loc_civics.governance
                    if loc_civics.occupance:
                        loc_occ_faction = loc_civics.occupance
                    if len(loc_civics.factions) > 0:
                        for faction in loc_civics.factions:
                            if faction:
                                if self.owner.relationCheck(faction) < -1:
                                    report = "Error: There is a Hostile party at present at this location."
                                    can_play = False
                        if can_play:
                            if not loc_occ_faction or loc_occ_faction == loc_gov_faction != None:
                                #Gov in charge
                                if self.owner.relationCheck(loc_gov_faction) < 3:
                                    #Player is neutral or hostile to local government
                                    report = "Error: You are not Allied with the ruling governance."
                                    can_play = False
                            elif loc_occ_faction and loc_occ_faction != loc_gov_faction:
                                #There is an occupation which is not the local government
                                if self.owner.relationCheck(loc_occ_faction) < 2:
                                    #Player is neutral or hostile to local occupance
                                    report = "Error: You are not Cooperative with the ruling occupance."
                                    can_play = False

                if target_type == 'district':
                    if player.location != str(target_obj):
                        report = "Error: You are not currently present at the designated location."
                        can_play = False
                else:
                    if player.location != target_obj.location:
                        report = "Error: You are not currently present at the designated location."
                        can_play = False
                if target_type == 'building':
                    if target_obj.certs:
                        for cert in target_obj.certs:
                            if cert not in self.certs:
                                report = "Error: This unit does not meet all requirements for the destination."
                                can_play = False
            else:
                report = "Error: This destination lacks the required number of slots available."
        else:
            report = "Error: This card is not in your hand."
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
                    for cert in target_obj.certs:
                        if cert not in self.certs:
                            report = "Error: This unit does not meet all requirements for the destination."
                            can_play = False
        return can_play, report


    async def playCard(self, player, target_obj):
        card_type = type(self).__name__.lower()
        player_type = type(player).__name__.lower()
        if player_type == 'player':
            can_play, report = self.playerPlayCheck(player, target_obj)
        else:
            can_play, report = self.fabPlayCheck(player, target_obj)

        if can_play:
            self.toggleStatus()
            if player_type == 'player':
                player.modStat('Influence', -1)
            if self.play_cost:
                for key in self.play_cost.keys():
                    player.inventory.addResource(theJar['resources'][key], -self.play_cost[key])
            target_obj.inventory.addCardToSlot(self, card_type)
            self.location = target_obj
            theJar['played_cards'][card_type].append(self)
            if card_type == 'building':
                self.location.civics.getGovernor(player.faction)
            self.title += " ("+str(self.owner)+")"

            play_report = None
            play_arg_list = [self, target_obj]
            play_report = await self.triggerSkill('on_play', play_arg_list)
            report = str(player)+"\'s **"+str(self)+'** has been played to '+str(target_obj)
            if play_report:
                report += "\n"+play_report
        return can_play, report

    def unplayCard(self, player):
        card_type = type(self).__name__.lower()
        player_type = type(player).__name__.lower()
        #if player_type == 'player':
        can_unplay, report = self.playerUnplayCheck(player)

        if can_unplay:
            target_obj = self.location
            self.toggleStatus()
            self.location.inventory.removeCardFromSlot(self, card_type)
            self.location = None
            theJar['played_cards'][card_type].append(self)
            report = str(self)+' has been unplayed from '+str(target_obj)
        return report

