import random
from _01_functions import *

class Dice():
    def __init__(self, quantity, sides):
        self.quantity = quantity
        self.sides = sides


    def __str__(self):
        report = str(self.quantity)+"d"+str(self.sides)
        return report


    def roll_math(self, success):
        i = 1
        rolls = []
        while i <= self.quantity:
            roll = random.randint(1,self.sides)
            rolls.append(roll)
            i+=1

        hits = [e for e in rolls if e >= success]
        hit_count = len(hits)
        if hit_count > 0:
            s = True
        else:
            s = False

        report = {
            'rolls':rolls,
            'threshold':success,
            'hits':hits,
            'hit_count':hit_count,
            'result':s
        }
        return report


    async def roll(self, ctx, success_int):
        report_dict = self.roll_math(int(success_int))
        if report_dict['result']:
            status = "-------HIT-------"
        else:
            status = "------MISS-------"
        report_str = status+"\n\n-----Results-----\n\n"+"Rolled: "+str(self)+"\n"+"Rolls: "+str(report_dict['rolls'])+"\n"+"Threshold: "+str(report_dict['threshold'])+"\n"+"Hits: "+str(report_dict['hit_count'])
        await say(ctx, str(report_str))
