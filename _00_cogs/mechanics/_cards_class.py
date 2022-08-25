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

    async def triggerPlaySkill(self, arg_list):
        if self.skillsets:
            report = None
            played_skills = []
            play_skills = ['doot']
            while play_skills != played_skills:
                try:
                    play_skills.remove('doot')
                except:
                    pass
                for skillset_name in self.skillsets.keys():
                    skillsets = self.skillsets[skillset_name]
                    for skillset in skillsets:
                        if 'on_play' in skillset.triggers:
                            play_skills.append(skillset)
                if len(play_skills) > 0:
                    for skill in play_skills:
                        if skill not in played_skills:
                            try:
                                report = await skill.play(*arg_list)
                            except:
                                report = skill.play(*arg_list)
                            played_skills.append(skill)
            if report:
                return report

    async def triggerSkill(self, trigger, arg_list):
        report = None
        if self.skillsets:
            for skillset_name in self.skillsets.keys():
                skillsets = self.skillsets[skillset_name]
                for skillset in skillsets:
                    if trigger in skillset.triggers:
                        report = None
                        if trigger == 'on_act':
                            try:
                                report = await skillset.act(*arg_list)
                            except:
                                report = skillset.act(*arg_list)
                        if trigger == 'on_work':
                            try:
                                report = await skillset.work(*arg_list)
                            except:
                                report = skillset.work(*arg_list)
                        if trigger == 'on_move':
                            try:
                                report = await skillset.move(*arg_list)
                            except:
                                report = skillset.move(*arg_list)
                        if trigger == 'on_battle':
                            try:
                                report = await skillset.battle(*arg_list)
                            except:
                                report = skillset.battle(*arg_list)
                        if trigger == 'on_attack':
                            try:
                                report = await skillset.attack(*arg_list)
                            except:
                                report = skillset.attack(*arg_list)
                        if trigger == 'on_defend':
                            try:
                                report = await skillset.defend(*arg_list)
                            except:
                                report = skillset.defend(*arg_list)
                        if trigger == 'on_death':
                            try:
                                report = await skillset.death(*arg_list)
                            except:
                                report = skillset.death(*arg_list)
                        if trigger == 'on_harvest':
                            try:
                                report = await skillset.harvest(*arg_list)
                            except:
                                report = skillset.harvest(*arg_list)
                        if trigger == 'on_refresh':
                            try:
                                report = await skillset.refresh(*arg_list)
                            except:
                                report = skillset.refresh(*arg_list)
            if report:
                return report


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
                        if player.inventory.resources[key] < cost:
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
                    player.inventory.addResource(key, -self.play_cost[key])
            target_obj.inventory.addCardToSlot(self, card_type)
            self.location = str(target_obj)
            theJar['played_cards'][card_type].append(self)
            if card_type == 'building':
                target_obj.civics.getGovernor(player.faction)
            self.title += " ("+str(self.owner)+")"

            play_report = None
            play_arg_list = [self, target_obj]
            play_report = await self.triggerPlaySkill(play_arg_list)
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

