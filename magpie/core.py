import logging
import telegram, telegram.ext

import services.os

class Bot(telegram.ext.Updater):
    def __init__(self, *, token, admin_id):
        self.admin_id = admin_id
        telegram.ext.Updater.__init__(self, token=token)
        self.dispatcher.add_handler(*services.os.commands)

    def listen(self):
        self.start_polling()
        self.idle()

    def send_admin(self, text):
        return self.bot.send_message(
            chat_id=self.admin_id,
            text=text,
            parse_mode=telegram.ParseMode.HTML
        )
