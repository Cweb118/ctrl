import random

def roll_dice(quantity, sides, success):
    i = 1
    rolls = []
    while i <= quantity:
        roll = random.randint(1,sides)
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
        'hits':hits,
        'hit_count':hit_count,
        'result':s
    }

    return report

