from nextcord import Interaction

from _02_global_dicts import theJar
from _00_cogs.frontend.state_error import StateError
import _00_cogs.frontend.menus.menus as Menus

def getAction(card, act_id):
    if card.skillsets:
        for skillset in card.skillsets:
            if ('on_act' in skillset.triggers) and skillset.act_id == act_id:
                return skillset
    
    return None

async def resolveAction(interaction: Interaction, state):
    if 'card' not in state or 'card_type' not in state:
        raise StateError

    if 'player' not in state or state['player'] not in theJar['players']:
        raise StateError

    player = theJar['players'][state['player']]
    card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

    if card is None:
        raise StateError

    if 'action' not in state:
        raise StateError

    action = getAction(card, state['action'])

    if action is None:
        raise StateError

    if 'act_params' not in state or 'act_param' not in state or 'act_param_stage' not in state:
        raise StateError

    params = state['act_params']
    param_num = state['act_param']
    param_stage = state['act_param_stage']

    if param_num <= -1 and param_stage <= -1:
        if len(action.act_params) == 0:
            await action.act(card)
            return
        
        param_num = 0
        param_stage = -1

    if len(action.act_params) <= param_num:
        raise StateError

    if len(action.act_params[param_num]) <= param_stage + 1:
        raise StateError

    param_stage += 1

    if len(action.act_params[param_num]) <= param_stage + 1:
        param_num += 1
        param_stage = 0

        if len(action.act_params) <= param_num:
            parsed_params = []

            def parseDistrict(raw_param):
                if raw_param not in theJar['districts']:
                    raise StateError

                return theJar['districts'][raw_param]

            def parseCard(card_type, raw_param):
                raw_param_split = raw_param.split('|')

                if len(raw_param_split) != 2:
                    raise StateError

                player_id, card_id = raw_param_split

                if player_id not in theJar['players']:
                    raise StateError

                player = theJar['players'][player_id]
                card = player.inventory.getCardByUniqueID(card_type, card_id)

                if card is None:
                    raise StateError

                return card

            for i in range(len(action.act_params)):
                param_opts = action.act_params[i]
                last_type = param_opts[len(param_opts) - 1]

                raw_param = params[i]               

                if last_type == 'current_location' or last_type == 'adjacent_location':
                    parsed_params.append(parseDistrict(raw_param))
                elif last_type == 'unit':\
                    parsed_params.append(parseCard('unit', raw_param))
                elif last_type == 'building':
                    parsed_params.append(parseCard('building', raw_param))

            await action.act(card, *parsed_params)
            return

    param = action.act_params[param_num]
    param_type = param[param_stage + 1][0]

    if param_type == 'current_location':
        while len(params) <= param_num:
            params.append(None)

        params[param_num] = card.location.title

        await resolveAction(interaction, {
            'card': state['card'], 'card_type': state['card_type'],
            'player': state['player'],
            'action': state['action'],
            'act_params': params, 'act_param': param_num, 'act_param_stage': param_stage
        })
    elif param_type == 'adjacent_location':
        await Menus.adjacentParamMenu.show(interaction, newState={
            'card': state['card'], 'card_type': state['card_type'],
            'player': state['player'],
            'action': state['action'],
            'act_params': params, 'act_param': param_num, 'act_param_stage': param_stage
        })
    elif param_type == 'unit':
        await Menus.unitParamMenu.show(interaction, newState={
            'card': state['card'], 'card_type': state['card_type'],
            'player': state['player'],
            'action': state['action'],
            'act_params': params, 'act_param': param_num, 'act_param_stage': param_stage
        })
    elif param_type == 'building':
        await Menus.buildingParamMenu.show(interaction, newState={
            'card': state['card'], 'card_type': state['card_type'],
            'player': state['player'],
            'action': state['action'],
            'act_params': params, 'act_param': param_num, 'act_param_stage': param_stage
        })