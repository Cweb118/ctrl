from typing import List
from discord import Interaction, SelectOption
from nextcord import ButtonStyle
import nextcord


def Button(id: str, label: str, style: ButtonStyle = ButtonStyle.secondary, includeFun = lambda state: True, disabledFun = lambda state: False):
    def render(fun, state):
        if includeFun(state):
            return nextcord.ui.Button(custom_id=fun.id, label=label, style=style, disabled=disabledFun(state))
        else:
            return None

    def wrapper(fun):
        fun.id = id
        fun.is_element = True
        fun.render = render

        return fun

    return wrapper

def UnlimitedSelect(id: str, optionsFun):
    def render(fun, state):
        options = optionsFun(state)

        if len(options) == 0:
            options = [SelectOption(label='Nothing', value='empty-list-nothing')]
        else:
            page = state.get('page', 0)

            maxPages = (len(options) - 1) // 23

            if maxPages < page:
                page = maxPages
                state['page'] = page
            elif page < 0:
                page = 0
                state['page'] = page

            start = page * 23
            end = min((page + 1)*23, len(options))

            options = options[start:end]

            if page != 0:
                options = [SelectOption(label='Prev Page', value='list-previous-page', emoji='⬅')] + options

            if page != maxPages:
                options = options + [SelectOption(label='Next Page', value='list-next-page', emoji='➡')]

        return nextcord.ui.Select(custom_id=id, options=options)

    def wrapper(fun):
        async def wrapper2(self, state, interaction: Interaction):
            value = interaction.data['values'][0]

            if value == 'empty-list-nothing':
                return False
            elif value == 'list-previous-page':
                page = state.get('page', 0)
                state['page'] = page - 1
                return True
            elif value == 'list-next-page':
                page = state.get('page', 0)
                state['page'] = page + 1
                return True
            else:
                return await fun(self, state, interaction)

        wrapper2.id = id
        wrapper2.is_element = True
        wrapper2.render = render

        return wrapper2

    return wrapper