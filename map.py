

district_map = {
    'Yavar':['Yavar', 'Yavari Domain', 'huge', ['Central Yavar']],

    'The Shores':['The Shores', 'Levyt Cliffside', 'medium', ['Yavar','The Rise']],


    'The Threshold':['The Threshold', 'The City of Barheim', 'small', ['The Foot of Barheim', 'The Core']],
    'The Core':['The Core', 'The City of Barheim', 'large', ['The Threshold']],
}

district_map_PENDING = {
    #[name, region_name, size, path_list]
    'Yavar':['Yavar', 'Yavari Domain', 'huge', ['Central Yavar']],

    'The Shores':['The Shores', 'Levyt Cliffside', 'medium', ['Yavar','The Rise']],
    'The Rise':['The Rise', 'Levyt Cliffside', 'tiny', ['The Shores','The Overlook']],
    'The Overlook':['The Overlook', 'Levyt Cliffside', 'small', ['The Rise','The Treeline']],

    'The Treeline':['The Treeline', 'Greven Taiga', 'medium', ['The Overlook', 'The Frigid Quiet']],
    'The Frigid Quiet':['The Frigid Quiet', 'Greven Taiga', 'large', ['The Treeline', 'The Foot of Barheim']],
    'The Foot of Barheim':['The Foot of Barheim', 'Greven Taiga', 'small', ['The Frigid Quiet', 'The Threshold']],

    'The Threshold':['The Threshold', 'The City of Barheim', 'small', ['The Foot of Barheim', 'The Core']],
    'The Core':['The Core', 'The City of Barheim', 'large', ['The Threshold']],
}
