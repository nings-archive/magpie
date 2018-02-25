import telegram
import lsm_helpers

class Bot(telegram.Bot):
    def __init__(self, token, my_id):
        telegram.Bot.__init__(self, token=token)
        self.my_id = my_id

    def send_me(self, text):
        return super().send_message(
            chat_id = self.my_id,
            text=text,
            parse_mode=telegram.ParseMode.HTML
        )
