from _02_global_dicts import theJar


class Inventory():
    def __init__(self, owner, r_cap=None, r_cont=None, u_cap=None, b_cap=None, u_slotcap=None, b_slotcap=None):
        self.inv_owner = owner #Player/Location/Card instance

        self.cont = r_cont #int
        self.cap = {
            "resource":r_cap, #int
            "unit":u_cap, #int
            "building":b_cap #int
        }
        self.cards = {
            'unit':[], #list
            'building':[]#list
        }
        self.slotcap = {
            "unit":u_slotcap, #int
            "building":b_slotcap #int
        }
        self.slots = {
            "unit":[],#list
            "building":[]#list
        }

        self.resources = {
            #instance:quantity
        }
        for key in theJar['resources'].keys():
            resource = theJar['resources'][key]
            try:
                self.resources[resource]
            except:
                self.resources[resource] = 0

    def capMathCard(self, card_type):
        can_add = False
        if len(self.cards[card_type]) < self.cap[card_type]:
                can_add = True
        return can_add

    def addCard(self, card, card_type):
        can_add = self.capMathCard(card_type)
        if can_add == True:
            self.cards[card_type].append(card)
        return can_add, card

    def delCard(self, t, card_number):
        del self.cards[t][card_number-1]

    def moveCard(self, t, card_number, new_owner_name, new_owner_id):
        card = self.cards[t][card_number-1]
        new_player = theJar['players'][new_owner_id]
        status = new_player.inventory.addCard(card, t)
        if status:
            del self.cards[card_number-1]
            report = "Your "+str(card)+"("+t+") has been given to "+new_owner_name+"!"
        else:
            report = "Error: Recipient lacks capacity for this item."
        return report


    def capMathRes(self):
        i = 0
        for key in self.resources.keys():
            if self.resources[key] > 0:
                i += 1
        return i

    def canAddMath(self, resource, quantity): #resource here is an INSTANCE
        new_val = self.resources[resource] + quantity
        can_add = False
        if self.cap['resource']:
            if new_val >= 0:
                if new_val <= self.cap['resource']:
                    if self.cont:
                        if self.resources[resource] > 0:
                            can_add = True
                        else:
                            i = self.capMathRes()
                            if i < self.cont:
                                can_add = True
                    else:
                        can_add = True
        return can_add

    def addResource(self, resource, quantity): #resource here is an INSTANCE
        new_val = self.resources[resource] + quantity
        can_add = self.canAddMath(resource, quantity)
        if can_add == True:
            self.resources[resource] = new_val
        return can_add

    def giveResource(self, resource, quantity, taker_inv):
        if quantity > 0:
            status = self.canAddMath(resource, -quantity)
            if status:
                status2 = taker_inv.canAddMath(resource, quantity)
                if status2:
                    self.addResource(resource, -quantity)
                    taker_inv.addResource(resource, quantity)
                    report = str(taker_inv.inv_owner)+" has recieved "+str(quantity)+" "+str(resource)+' from '+str(self.inv_owner)
                else:
                    report = "Error: Destination has insufficient space."
            else:
                report = "Error: Insufficient quantity of resource."
        else:
            report = "Error: Input less than zero."
        return report

    def dropres(self, resource, quantity, target_type, target):
        taker = None
        if target_type == 'district':
            if self.inv_owner.location == theJar['districts'][target]:
                taker = theJar['districts'][target]
            else:
                report = "Error: Not at present location."
        elif target_type == 'unit':
            taker = self.getCard(target_type, int(target))
            if self.inv_owner.location != taker.location:
                report = "Error: Not at present location."
                taker = None
        elif target_type == 'building':
            taker = self.getCard(target_type, int(target))
            if self.inv_owner.location != taker.location:
                report = "Error: Not at present location."
                taker = None
        else:
            report = "Error: Invalid target."
        if taker:
            report = self.giveResource(resource, quantity, taker.inventory)
        return report

    def takeres(self, resource, quantity: int, target_type, target):
        giver = None
        if target_type == 'district':
            if self.inv_owner.location == theJar['districts'][target]:
                giver = theJar['districts'][target]
            else:
                report = "Error: Not at present location."
        elif target_type == 'unit':
            giver = self.getCard(target_type, int(target))
            if self.inv_owner.location != giver.location:
                report = "Error: Not at present location."
                giver = None
        elif target_type == 'building':
            giver = self.getCard(target_type, int(target))
            if self.inv_owner.location != giver.location:
                report = "Error: Not at present location."
                giver = None
        else:
            report = "Error: Invalid target."
        if giver:
            report = giver.inventory.giveResource(resource, quantity, self)
        return report


    def __str__(self):
        report = str(self.inv_owner)+"'s Inventory"
        return report

    def report(self):
        title = "-----"+str(self)+"-----\n"
        fields = []
        report = ''
        if self.cap['resource']:
            res_field = {'inline':False}
            if self.cont:
                res_field['title'] = "-- Resources: ("+str(self.capMathRes())+"/"+str(self.cont)+")"
            else:
                res_field['title'] = "-- Resources:"
            i = 0
            res_rep = ''
            for resource in self.resources.keys():
                if self.resources[resource] > 0:
                    res_rep += "- "+str(resource)+" ("+str(self.resources[resource])+"/"+str(self.cap['resource'])+")\n"
                    i += 1
            if i == 0:
                res_rep += "- None (0/"+str(self.cap['resource'])+")\n"
            res_field['value'] = res_rep
            fields.append(res_field)

        #if self.cap['unit'] or self.cap['building']:
            #report += "\n---Cards:\n"
        if self.cap['unit']:
            unit_field = {'inline':False}
            unit_field['title'] = "-- Units (Inventory): ("+str(len(self.cards['unit']))+"/"+str(self.cap['unit'])+")\n"
            unit_field['value'] = ''
            for card in self.cards['unit']:
                unit_field['value'] += "- "+str(card)+" ("+card.status+")\n"
            if len(unit_field['value']) == 0:
                unit_field['value'] = '- Empty'
            fields.append(unit_field)

        if self.cap['building']:
            building_field = {'inline':False}
            building_field['title'] = "-- Buildings (Inventory): ("+str(len(self.cards['building']))+"/"+str(self.cap['building'])+")\n"
            building_field['value'] = ''
            for card in self.cards['building']:
                building_field['value'] += "- "+str(card)+" ("+card.status+")\n"
            if len(building_field['value']) == 0:
                building_field['value'] = '- Empty'
            fields.append(building_field)

        #if self.slotcap['unit'] or self.slotcap['building']:
            #report += "\n---Slots:\n"
        if self.slotcap['unit']:
            uslot_field = {'inline':False}
            uslot_field['title'] =  "-- Unit Slots: ("+str(len(self.slots['unit']))+"/"+str(self.slotcap['unit'])+")\n"
            uslot_field['value'] = ''
            for card in self.slots['unit']:
                uslot_field['value'] += "- "+str(card)+" ("+card.status+")\n"
            if len(uslot_field['value']) == 0:
                uslot_field['value'] = '- Empty'
            fields.append(uslot_field)

        if self.slotcap['building']:
            bslot_field = {'inline':False}
            bslot_field['title'] = "-- Building Slots: ("+str(len(self.slots['building']))+"/"+str(self.slotcap['building'])+")\n"
            bslot_field['value'] = ''
            for card in self.slots['building']:
                bslot_field['value'] += "- "+str(card)+" ("+card.status+")\n"
            if len(bslot_field['value']) == 0:
                bslot_field['value'] = '- Empty'
            fields.append(bslot_field)

        return report, title, fields

    def getCard(self, card_type, card_number):
        card = self.cards[card_type][int(card_number)-1]
        return card

    def cardReport(self, t, card_number):
        card = self.getCard(t, int(card_number))
        return card.report()

    def cardNick(self, t, card_number, nick):
        card = self.getCard(t, int(card_number))
        card.setNick(nick)
        return card.report()
