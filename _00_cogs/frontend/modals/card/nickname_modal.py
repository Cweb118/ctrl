from nextcord import Interaction
from _00_cogs.frontend.elements import TextInput
from _00_cogs.frontend.modal import Modal

class NicknameModal(Modal):
    def __init__(self):
        super().__init__('nicknamemodal', 'Set Nickname')

    @TextInput(id='nickname', label='Nickname')
    def nickname(self):
        pass

    async def onSubmit(self, interaction: Interaction):
        pass