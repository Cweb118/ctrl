info_dict = {
    'info': {'title':"-----Info-----",'info':'Type this command followed by a keyword to learn more about it.'},
    'Overclock': {'title':"-----Overclock (Automata)-----",'info':'Unit consumes 3 steam for a boost in Endurance equal to their cap.'},
    'Harmonize': {'title':"-----Harmonize (Yavari)-----",'info':'Pass your current effects to another unit (consumes all End)'},
    'Explore': {'title':"-----Explore (Pathfinder)-----",'info':'Submits a directional exploration request to control.'},
    'Scout': {'title':"-----Scout (Scout)-----",'info':'Scouts a location, requires 2 End'},
    'Inspire': {'title':"-----Inspire (Barheim)-----",'info':'Charges Industrialist unit (not relevant to this playtest)'},
    'Transport': {'title':"-----Transport (Various)-----",'info':'Links two buildings together, routing the output of one into the input of the other.'},
    'Sentry': {'title':"-----Sentry (Sentry)-----",'info':' Gets a report on adj districts (needs full End)'},
    'Recon': {'title':"-----Recon (Recon Units)-----",'info':'Provides access to chat if units are present'},
    'Barheim': {'title':"-----Overtime (Barheim)-----",'info':'Works two slots in a building instead of one'},
    'Inorganic': {'title':"-----Inorganic (Automata)-----",'info':'Does not have upkeep'},
    'Harmony': {'title':"-----Harmony (Harmonist)-----",'info':'Protects unit from defense loss at upkeep (known bug: triggers twice)'},
}




info_dict_master = {
    #Game Mechanics
    'info': {'title':"-----Info-----",'info':'Type this command followed by a keyword to learn more about it.'},
    'harvest':{'title':"-----Harvest-----",'info':'At the end of every day phase there is a harvest. This occurs after any **ERROR** take place. At this time units will consume their upkeep from resources in their inventory. They will then roll for upkeep with their **dice set**. A hit for this roll is a value greater than their defense + fortitude. Hits result in damage taken.'},
    'production': {'title':"-----Production-----",'info':'If at the end of the day a building is fully worked and has any required catalysts and inputs in its inventory, it will produce the designated outputs into its inventory during production.'},
    'battle': {'title':"-----Battle-----",'info':'ERROR'},
    'squad': {'title':"-----Squad-----",'info':'ERROR'},
    'commander': {'title':"-----Commander-----",'info':'A commander is a leader of a faction within a given location. They are permitted to set the **ERROR** of that faction at that location. They are determined by comparing the (maximum) **Influence** each player with presence there (combantant count breaking ties). The faction with the most combatants will become the **Occupance** of that location.'},
    'occupance': {'title':"-----Occupance-----",'info':'An occupance is a ruling force at a given location. The faction with the most **combatant**s will become the Occupance of that location. They will overrule any **government** also present. An Occupance will not occur if the existing occupance or governance are of a reputation standing greater than Neutral.'},
    'government': {'title':"-----Government-----",'info':'A government ruling body at a given location. They are determined by counting the buildings of each faction present. The ruling body of a given location will dictate who may build there.'},
    'governor': {'title':"-----Governor-----",'info':'A Governor is one who is in charge of an faction\'s local infrastructure. This position is determined by comparing the **Influence** of each player with representation (buildings or they themselves). The Governor with the most buildings across their faction will claim the location for their party.'},
    'build': {'title':"-----Build-----",'info':'To build a building you must play it to a location with available building slots in their inventory (typically a district). You may only build at a location where you are allied with the current Governance or cooperative with the current Occupance.'},
    'faction': {'title':"-----Faction-----",'info':'A faction is an organization which players or entities can be part of in order to gain certain permissions. Factions have standings with other factions (reputation). Individual players will also have **reputation** standings with each faction.'},
    'reputation': {'title':"-----Reputation-----",'info':'A player or faction\'s reputation runs along the following scale: Allied, Cooperative, Friendly, Neutral, Unfriendly, Hostile, Enemy.'},
    'influence': {'title':"-----Influence-----",'info':'Influence is a metric by which a player\'s power is measured. It is primarly used to play cards. Influence is refreshed at the end of each day.'},

    'upkeep': {'title':"-----Upkeep-----",'info':'Upkeep is required to keep units healthy. Failure to pay upkeep during the **harvest** will result in a loss of **Defense**. This occurs before the upkeep roll, which will result in damage taken if hit.'},
    'refresh': {'title':"-----Refresh-----",'info':'At the end of each **day**, each unit is refreshed. At this time their ERROR and endurance are restored.'},
    'day': {'title':"-----Day-----",'info':'The Day phase refers to a 24 hour period where players may speak openly and take actions freely. At the end of the day battles, production, the harvest, and the refresh (of units) will occur in that order.'},
    'night': {'title':"-----Night-----",'info':'The Night phase refers to a 24 hours period where chats are closed and players may not take actions.'},
    'district': {'title':"-----District-----",'info':'A district is a location housed within a **region**. Districts have different sizes which can support different numbers of units and buildings. A link to another nearby district is called a path.'},
    'region': {'title':"-----Region-----",'info':'A region houses several **districts**, which in turn can contain buildings and units.'},
    'stats': {'title':"-----Stats-----",'info':'Both units and buildings have stats. Units have ERROR, Defense, Health, Endurance, Fortitude, ERROR, and ERROR. Buildings have many of the same, with the addition of inputs, outputs, catalysts, and worker requirements.'},

    #Units
    'attack': {'title':"-----Attack-----",'info':'ERROR'},
    'defense': {'title':"-----Defense-----",'info':'A unit (or building)\'s capacity to receive damage before loosing Health.'},
    'health': {'title':"-----Health-----",'info':'A unit (or building)\'s capacity to receive damage before dying.'},
    'endurance': {'title':"-----Endurance-----",'info':'A unit\'s capacity to move to an adjacent district (1 point per move) or perform certain actions.'},
    'fortitude': {'title':"-----Fortitude-----",'info':'A unit\'s ability to endure going without an **upkeep** resource. This combines with Defense to provide a higher threshold when rolling for damage during the **harvest**.'},
    'initiative': {'title':"-----Initiative-----",'info':'ERROR.'},
    'taunt': {'title':"-----Taunt-----",'info':'ERROR'},
    'input': {'title':"-----Input-----",'info':'A list of items a building will need in its inventory prior to the Day\'s end in order to produce its output.'},
    'output': {'title':"-----Output-----",'info':'A list of items a building will produce at Day\'s end granted all prerequisites are met. Output items will go into the building\'s inventory unless they have a **Link** to another.'},
    'catalyst': {'title':"-----Catalyst-----",'info':'A list of items a building needs in its inventory to produce at Day\'s end (they will not be consumed)'},
    'link': {'title':"-----Link-----",'info':'A link is a one way routing of items from one building to another *during* production. Buildings on the receiving end of a link will not produce until all sending buildings have produced first.'},
    'requirements': {'title':"-----Worker Requirements-----",'info':'A list of required **certification**s (or certs) a unit will need in order to work at the respective building.'},
    'certification': {'title':"-----Certification-----",'info':'A list of **requirement**s met that a unit possesses in order to work at a given building or perform a given function.'},
    'effect': {'title':"-----Effect-----",'info':'A temporary **trait** which can modify its host (unit/building) in a variety of ways. Effects usually are removed at the end of a day.'},
    'trait': {'title':"-----Trait-----",'info':'A trait is a bundle of modifiers that can be applied to a unit or building. It may come with adjustments to stats, inventory, or bring new functionalities.'},

    #Traits
    #Classes
    'worker': {'title':"-----Worker-----",'info':'A simple worker. If they meet all of a building\'s **requirement**s, they may work there to foster **production**.'},
    'engineer': {'title':"-----Engineer-----",'info':'A more focused mind. An Engineer has additional **certification**s which will grant them additional opportunities for work.'},
    'scout': {'title':"-----Scout-----",'info':'A brave wanderer. Scouts have the ability to **explore** adjacent districts and **scavange** resources.'},
    'warrior': {'title':"-----Warrior-----",'info':'A basic soldier. Warriors possess the ability to perform an additional attack considered a **crit**.'},
    'ranger': {'title':"-----Ranger-----",'info':'A shrewed marksman. Rangers have the ability to **barrage** their opponent.'},
    'guardian': {'title':"-----Guardian-----",'info':'A noble protector. Guardians have increased threat as well as the ability to **block**.'},
    'knight': {'title':"-----Knight-----",'info':'A valiant swordsman. Knights have the ability to both Minor Crit and Minor Block. If charged, they deal 1 extra damage on crit.'},
    'witch': {'title':"-----Witch-----",'info':'A wicked acolyte. A Witch can **channel** their energy into a strong **Arcanae**, Charging allies.'},
    'alchemist': {'title':"-----Alchemist-----",'info':'An **Industrialist** scholar. The Alchemist has the ability to ERROR.'},
    'technophant': {'title':"-----Technophant-----",'info':'A dark manipulator of **Atomkia**. With each passing strike, the Technophant grows in power...'},

    #Races
    'aratori': {'title':"-----Aratori-----",'info':'A mighty race of great strength, the power of an Aratori is scarcely rivaled (can Major Crit as an attacker).'},
    'barheim': {'title':"-----Barheim-----",'info':'A race of Engineers, their hearts are said to be as hard and cold as their flesh (works two slots).'},
    'automata': {'title':"-----Automata-----",'info':'A creation of the Barheim, the Automata were built to last much longer than any organic being (No Upkeep).'},
    'loyavasi': {'title':"-----Loyavasi-----",'info':'A hoofed people from the mountains, the Loyavasi can travel more in a day than any other (+2 Endurance over cap)'},
    'otavan': {'title':"-----Otavan-----",'info':'Descendants of Aratori colonists, these who have made their lives in the countryside have learned to subvert strength with subterfuge (-2 Threat).'},
    'prismari': {'title':"-----Prismari-----",'info':'A regal race of birds who move quite fast for their size. The Prismari may Parry when attacked, potentially dealing damage against their opponent.'},
    'rivenborne': {'title':"-----Rivenborne-----",'info':'A mysterious race full of intrigue. The energy coursing through their rocky forms empowers them (has the Charged trait which self-renews each Day).'},
    'xinn': {'title':"-----Xinn-----",'info':'An brutal race of bipedal bovines. The Xinn\'s strenght is commonly exploited for manual labor, and as such each knows how to Harvest (is granted the Harvest cert).'},
    'yavari': {'title':"-----Yavari-----",'info':'A race of hunters, attuned to nature. Once per day as an action, a user may spend 1 Influence to spread all **effects** from this unit to another.'},
    'bloodless': {'title':"-----Bloodless-----",'info':'A cruel, wicked race which corrupts their prey and leads them into darkness.'},

    #Abilities
    'gather': {'title':"-----Gather-----",'info':''},
    'scavenge': {'title':"-----Scavenge-----",'info':''},
    'crit': {'title':"-----Crit-----",'info':'There are several varieties of Critical hits. The basic Crit rolls the attacker\'s dice vs the opponenet\'s Defense. On hit, health is directly dealt per hit. A **Major Crit** is behaves similarly, with the change being that on any hit count the damage is dealt overall and with the value being equal to the attacker\'s Attack. A **Minor Crit* is identical to the previous, but with a maximum damage value of 1.'},
    'barrage': {'title':"-----Barrage-----",'info':'Following an attack when a barrage occurs, the attacker rolls their dice vs their opponent\'s Defense. Per hit, they reduce their opponent\'s Defense by 1.'},
    'block': {'title':"-----Block-----",'info':'Once per round of combat, when attacked, a unit with the block ability may roll against their own defense. For each hit, they fail to block 1 damage. A variant of this is the **Minor Block** which only blocks 1 damage maximum (but can occur on every attack in a round).'},
    'explore': {'title':"-----Explore-----",'info':'A pathfinder with full (or greater) Endurance may explore from their current location, creating a path to an adjacent one (discovered or otherwise).'},
    'channel': {'title':"-----Channel-----",'info':''},
    'info': {'title':"-----Info-----",'info':''},
    'info': {'title':"-----Info-----",'info':''},
    'info': {'title':"-----Info-----",'info':''},
    'info': {'title':"-----Info-----",'info':''},
    'info': {'title':"-----Info-----",'info':''},
    'info': {'title':"-----Info-----",'info':''},
    'info': {'title':"-----Info-----",'info':''},

}





info_dict_v1 = {
    #Game Mechanics
    'info': {'title':"-----Info-----",'info':'Type this command followed by a keyword to learn more about it.'},
    'harvest':{'title':"-----Harvest-----",'info':'At the end of every day phase there is a harvest. This occurs after any **battles** take place. At this time units will consume their upkeep from resources in their inventory. They will then roll for upkeep with their **dice set**. A hit for this roll is a value greater than their defense + fortitude. Hits result in damage taken.'},
    'production': {'title':"-----Production-----",'info':'If at the end of the day a building is fully worked and has any required catalysts and inputs in its inventory, it will produce the designated outputs into its inventory during production.'},
    'battle': {'title':"-----Battle-----",'info':'A battle occurs when a commander of an allegiance at a given location sets their stance to attack. All **squads** in that location will then attack the ruling body (the current Occupance, or otherwise, Government). Squads from each side will duel each other until only one side remains. This side will then be able to attack one final time, this time targeting the other side\'s buildings (or otherwise, non-squad units)'},
    'squad': {'title':"-----Squad-----",'info':'A squad is a group of 2-4 units which move together. The occupying **commander** of a location is determined by their number of squads present. In battle, squads of opposing sides will duel, whereas other units will stand idly by.'},
    'commander': {'title':"-----Commander-----",'info':'A commander is a leader of an allegiance within a given location. They are permitted to set the **stance** of that allegiance at that location. They are determined by comparing the (maximum) **Influence** each player with presence there (squad count breaking ties). The alleigance with the most squads will become the **Occupance** of that location.'},
    'occupance': {'title':"-----Occupance-----",'info':'An occupance is a ruling force at a given location. The alleigance with the most **squads** will become the Occupance of that location. They will overrule any **government** also present.'},
    'government': {'title':"-----Government-----",'info':'A government ruling body at a given location. They are determined by comparing the buildings of each allegiance present. The ruling body of a given location will dictate who may build there.'},
    'governor': {'title':"-----Governor-----",'info':'A Governor is one who is in charge of an allegiance\'s local infrastructure. This position is determined by comparing the **Influence** of each player with presense (buildings or they themselves). The Governor with the most buildings across their allegiance will claim the location for their party.'},
    'influence': {'title':"-----Influence-----",'info':'Influence is a metric by which a player\'s power is measured. It can be used to play units among other things.'},
    'upkeep': {'title':"-----Upkeep-----",'info':'Upkeep is required to keep units healthy. Failure to pay upkeep during the **harvest** will result in a loss of **Defense**. This occurs before the upkeep roll, which will result in damage taken if hit.'},
    'refresh': {'title':"-----Refresh-----",'info':'At the end of each **day**, each unit is refreshed. At this time their attack, endurance, and fortitude is restored.'},
    'day': {'title':"-----Day-----",'info':'The Day phase refers to a 24 hour period where players may speak openly and take actions freely. At the end of the day battles, production, the harvest, and the refresh (of units) will occur in that order.'},
    'night': {'title':"-----Night-----",'info':'The Night phase refers to a 24 hours period where chats are closed and players may not take actions.'},
    'district': {'title':"-----District-----",'info':'A district is a location housed within a **region**. Districts have different sizes which can support different numbers of units and buildings. A link to another nearby district is called a path.'},
    'region': {'title':"-----Region-----",'info':'A region houses several **districts**, which in turn can contain buildings and units.'},
    'stats': {'title':"-----Stats-----",'info':'Both units and buildings have stats. Units have Attack, Defense, Health, Endurance, and Fortitude (as well as Initiative and Threat). Buildings have many of the same, with the addition of inputs, outputs, catalysts, and worker requirements.'},

    #Units
    'attack': {'title':"-----Attack-----",'info':'A unit (or building)\'s capacity to deal damage to another entity.'},
    'defense': {'title':"-----Defense-----",'info':'A unit (or building)\'s capacity to receive damage before loosing Health.'},
    'health': {'title':"-----Health-----",'info':'A unit (or building)\'s capacity to receive damage before dying.'},
    'endurance': {'title':"-----Endurance-----",'info':'A unit\'s capacity to move to an adjacent district (1 point per move).'},
    'fortitude': {'title':"-----Fortitude-----",'info':'A unit\'s ability to endure going without an **upkeep** resource. This combines with Defense to provide a higher threshold when rolling for damage during the **harvest**.'},
    'initiative': {'title':"-----Initiative-----",'info':'Units with higher initiative will attack first in **battles**. Units in combat will be ranked by initiatives (i.e. units with 2 will attack in a wave before units with 1). For each wave, attackers always attack before defenders.'},
    'threat': {'title':"-----Threat-----",'info':'The unit with the highest threat will be targeted by all opposing units in battle.'},
    'input': {'title':"-----Input-----",'info':'A list of items a building will need in its inventory prior to the Day\'s end in order to produce its output.'},
    'output': {'title':"-----Output-----",'info':'A list of items a building will produce at Day\'s end granted all prerequisites are met. Output items will go into the building\'s inventory unless they have a **Link** to another.'},
    'catalyst': {'title':"-----Catalyst-----",'info':'A list of items a building needs in its inventory to produce at Day\'s end (they will not be consumed)'},
    'link': {'title':"-----Link-----",'info':'A link is a one way routing of items from one building to another *during* production. Buildings on the receiving end of a link will not produce until all sending buildings have produced first.'},
    'requirements': {'title':"-----Worker Requirements-----",'info':'A list of required **certification**s (or certs) a unit will need in order to work at the respective building.'},
    'certification': {'title':"-----Certification-----",'info':'A list of **requirement**s met that a unit possesses in order to work at a given building.'},
    'effect': {'title':"-----Effect-----",'info':'A temporary **trait** which can modify its host (unit/building) in a variety of ways. Effects usually are removed at the end of a day.'},
    'trait': {'title':"-----Trait-----",'info':'A trait is a bundle of modifiers that can be applied to a unit or building. It may come with adjustments to stats, inventory, or bring new functionalities.'},


    'info': {'title':"-----Info-----",'info':''},
    #Traits
    #Classes
    'worker': {'title':"-----Worker-----",'info':'A simple worker. If they meet all of a building\'s **requirement**s, they may work there to foster **production**.'},
    'engineer': {'title':"-----Engineer-----",'info':'A more focused mind. An Engineer has additional **certification**s which will grant them additional opportunities for work.'},
    'scout': {'title':"-----Scout-----",'info':'A brave wanderer. Scouts have the ability to **explore** adjacent districts and **scavange** resources.'},
    'warrior': {'title':"-----Warrior-----",'info':'A basic soldier. Warriors possess the ability to perform an additional attack considered a **crit**.'},
    'ranger': {'title':"-----Ranger-----",'info':'A shrewed marksman. Rangers have the ability to **barrage** their opponent.'},
    'guardian': {'title':"-----Guardian-----",'info':'A noble protector. Guardians have increased threat as well as the ability to **block**.'},
    'knight': {'title':"-----Knight-----",'info':'A valiant swordsman. Knights have the ability to both Minor Crit and Minor Block. If charged, they deal 1 extra damage on crit.'},
    'witch': {'title':"-----Witch-----",'info':'A wicked acolyte. A Witch can **channel** their energy into a strong **Arcanae**, Charging allies.'},
    'alchemist': {'title':"-----Alchemist-----",'info':'An **Industrus** scholar. The Alchemist has the ability to XXX.'},
    'technophant': {'title':"-----Technophant-----",'info':'A dark manipulator of **Atomkia**. With each passing strike, the Technophant grows in power...'},

    #Races
    'aratori': {'title':"-----Aratori-----",'info':'A mighty race of great strength, the power of an Aratori is scarcely rivaled (can Major Crit as an attacker).'},
    'barheim': {'title':"-----Barheim-----",'info':'A race of Engineers, their hearts are said to be as hard and cold as their flesh (works two slots).'},
    'automata': {'title':"-----Automata-----",'info':'A creation of the Barheim, the Automata were built to last much longer than any organic being (No Upkeep).'},
    'loyavasi': {'title':"-----Loyavasi-----",'info':'A hoofed people from the mountains, the Loyavasi can travel more in a day than any other (+2 Endurance over cap)'},
    'otavan': {'title':"-----Otavan-----",'info':'Descendants of Aratori colonists, these who have made their lives in the countryside have learned to subvert strength with subterfuge (-2 Threat).'},
    'prismari': {'title':"-----Prismari-----",'info':'A regal race of birds who move quite fast for their size. The Prismari may Parry when attacked, potentially dealing damage against their opponent.'},
    'rivenborne': {'title':"-----Rivenborne-----",'info':'A mysterious race full of intrigue. The energy coursing through their rocky forms empowers them (has the Charged trait which self-renews each Day).'},
    'xinn': {'title':"-----Xinn-----",'info':'An brutal race of bipedal bovines. The Xinn\'s strenght is commonly exploited for manual labor, and as such each knows how to Harvest (is granted the Harvest cert).'},
    'yavari': {'title':"-----Yavari-----",'info':'A race of hunters, attuned to nature. Once per day as an action, a user may spend 1 Influence to spread all **effects** from this unit to another.'},
    'bloodless': {'title':"-----Bloodless-----",'info':'A cruel, wicked race which corrupts their prey and leads them into darkness.'},

    #Abilities
    'gather': {'title':"-----Gather-----",'info':''},
    'scavenge': {'title':"-----Scavenge-----",'info':''},
    'crit': {'title':"-----Crit-----",'info':'There are several varieties of Critical hits. The basic Crit rolls the attacker\'s dice vs the opponenet\'s Defense. On hit, health is directly dealt per hit. A **Major Crit** is behaves similarly, with the change being that on any hit count the damage is dealt overall and with the value being equal to the attacker\'s Attack. A **Minor Crit* is identical to the previous, but with a maximum damage value of 1.'},
    'barrage': {'title':"-----Barrage-----",'info':'Following an attack when a barrage occurs, the attacker rolls their dice vs their opponent\'s Defense. Per hit, they reduce their opponent\'s Defense by 1.'},
    'block': {'title':"-----Block-----",'info':'Once per round of combat, when attacked, a unit with the block ability may roll against their own defense. For each hit, they fail to block 1 damage. A variant of this is the **Minor Block** which only blocks 1 damage maximum (but can occur on every attack in a round).'},
    'explore': {'title':"-----Explore-----",'info':'A squad of 2 or more Scouts where each unit has full Endurance may **explore** into an adjacent district.'},
    'channel': {'title':"-----Channel-----",'info':''},
    'info': {'title':"-----Info-----",'info':''},
    'info': {'title':"-----Info-----",'info':''},
    'info': {'title':"-----Info-----",'info':''},
    'info': {'title':"-----Info-----",'info':''},
    'info': {'title':"-----Info-----",'info':''},
    'info': {'title':"-----Info-----",'info':''},
    'info': {'title':"-----Info-----",'info':''},








}
