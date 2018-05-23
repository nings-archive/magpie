import logging
import telegram, telegram.ext

CommandHandler = telegram.ext.CommandHandler

class Bot(telegram.ext.Updater):
    def __init__(self, *, token, admin_id):
        telegram.ext.Updater.__init__(self, token=token)
        self.admin_id = admin_id

    def send_admin(self, text):
        return self.bot.send_message(
            chat_id=self.admin_id,
            text=text,
            parse_mode=telegram.ParseMode.HTML
        )
