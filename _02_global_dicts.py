district_dict = {}
fab_dict = {}
region_dict = {}
resource_dict = {}
player_dict = {}
played_cards_dict = {'unit':[], 'building':[]}

allegiance_dict = {
    'Bandits':{'Camp':'Hostile', 'Cows':'Hostile'},
    'Camp':{'Bandits':'Hostile', 'Cows':'Friendly'},
    'Cows':{'Bandits':'Hostile', 'Camp':'Friendly'}
}
