from nextcord import Interaction
from _00_cogs.frontend.elements import TextInput
from _00_cogs.frontend.modal import Modal
from _00_cogs.frontend.state_error import StateError
from _02_global_dicts import theJar

class NicknameModal(Modal):
    def __init__(self):
        super().__init__('nicknamemodal', 'Set Nickname')

    @TextInput(id='nickname', label='Nickname')
    def nickname(self):
        pass

    async def onSubmit(self, state, values, interaction: Interaction):
        if 'card' not in state or 'card_type' not in state:
            raise StateError

        if 'player' not in state or state['player'] not in theJar['players']:
            raise StateError

        if 'nickname' not in values:
            raise StateError

        player = theJar['players'][state['player']]
        card = player.inventory.getCardByUniqueID(state['card_type'], state['card'])

        nickname = values['nickname']
        nickname = nickname[:25]
        card.setNick(nickname)
