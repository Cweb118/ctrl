import random
from _01_functions import *

class Dice():
    def __init__(self, die):
        self.set = die

    def __str__(self):
        report = str(self.set)
        return report

    def addDice(self, dice):
        self.set.append(dice)

    def roll_math(self, success):
        rolls = []
        for dice in self.set:
            split_list = dice.split('d')
            quantity = int(split_list[0])
            sides = int(split_list[1])
            i = 1
            while i <= quantity:
                roll = random.randint(1,sides)
                rolls.append(roll)
                i+=1

        hits = [e for e in rolls if e >= success]
        hit_count = len(hits)
        if hit_count > 0:
            s = True
            r = 'HIT'
        else:
            s = False
            r = 'MISS'

        report = {
            'rolls':rolls,
            'threshold':success,
            'hits':hits,
            'hit_count':hit_count,
            'result':r
        }
        return s, report


    async def roll(self, success_int):
        result, report_dict = self.roll_math(int(success_int))
        if report_dict['result']:
            status = "-------HIT-------"
        else:
            status = "------MISS-------"
        report_str = status+"\n\n-----Results-----\n\n"+"Rolled: "+str(self)+"\n"+"Rolls: "+str(report_dict['rolls'])+"\n"+"Threshold: "+str(report_dict['threshold'])+"\n"+"Hits: "+str(report_dict['hit_count'])
        return result, report_str
