import _00_cogs.frontend.menus.card.cards_menu as cards_menu
import _00_cogs.frontend.menus.card.play_menu as play_menu
import _00_cogs.frontend.menus.card.manage_menu as manage_menu
import _00_cogs.frontend.menus.card.command_menu as command_menu
import _00_cogs.frontend.menus.card.transfer_resource_menu as transfer_resource_menu
import _00_cogs.frontend.menus.card.squad_menu as squad_menu
import _00_cogs.frontend.menus.card.squads_menu as squads_menu
import _00_cogs.frontend.menus.district.district_menu as district_menu
import _00_cogs.frontend.menus.district.travel_menu as travel_menu
import _00_cogs.frontend.menus.district.interact_menu as interact_menu
import _00_cogs.frontend.menus.card.move_menu as move_menu
import _00_cogs.frontend.menus.card.actions.act_menu as act_menu
import _00_cogs.frontend.menus.card.actions.adjacent_param_menu as adjacent_param_menu
import _00_cogs.frontend.menus.card.actions.card_param_menu as card_param_menu

cardsMenu = cards_menu.CardsMenu()
cardMenu = cards_menu.CardMenu()
buildingPlayMenu = play_menu.BuildingPlayMenu()
squadMenu = squad_menu.SquadMenu()
squadsMenu = squads_menu.SquadsMenu()
districtMenu = district_menu.DistrictMenu()
travelMenu = travel_menu.TravelMenu()
interactMenu = interact_menu.InteractMenu()

playMenu = play_menu.PlayMenu()
manageMenu = manage_menu.ManageMenu()
commandMenu = command_menu.CommandMenu()
transferResourceMenu = transfer_resource_menu.TransferResourceMenu()
actMenu = act_menu.ActMenu()
adjacentParamMenu = adjacent_param_menu.AdjacentParamMenu()
unitParamMenu = card_param_menu.UnitParamMenu()
buildingParamMenu = card_param_menu.BuildingParamMenu()

moveMenu = move_menu.MoveMenu()
buildingMoveMenu = move_menu.BuildingMoveMenu()
districtMoveMenu = move_menu.DistrictMoveMenu()