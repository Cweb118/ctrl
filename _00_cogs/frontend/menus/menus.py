import _00_cogs.frontend.menus.card.cards_menu as cards_menu
import _00_cogs.frontend.menus.card.play_menu as play_menu
import _00_cogs.frontend.menus.card.manage_menu as manage_menu
import _00_cogs.frontend.menus.card.squad_menu as squad_menu
import _00_cogs.frontend.menus.card.squads_menu as squads_menu
import _00_cogs.frontend.menus.district.district_menu as district_menu
import _00_cogs.frontend.menus.district.travel_menu as travel_menu

cardsMenu = cards_menu.CardsMenu()
cardMenu = cards_menu.CardMenu()
buildingPlayMenu = play_menu.BuildingPlayMenu()
squadMenu = squad_menu.SquadMenu()
squadsMenu = squads_menu.SquadsMenu()
districtMenu = district_menu.DistrictMenu()
travelMenu = travel_menu.TravelMenu()

playMenu = play_menu.PlayMenu()
manageMenu = manage_menu.ManageMenu()