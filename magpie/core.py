import logging
import telegram, telegram.ext

CommandHandler = telegram.ext.CommandHandler

class Bot(telegram.Bot):
    def __init__(self, *, token, admin_id):
        telegram.Bot.__init__(self, token=token)
        self.admin_id = admin_id

    def listen(self):
        self.updater = telegram.ext.Updater(bot=self)
        self.dispatcher = self.updater.dispatcher
        self.updater.start_polling()
        self.updater.idle()

    def send_admin(self, text):
        return super().send_message(
            chat_id=self.admin_id,
            text=text,
            parse_mode=telegram.ParseMode.HTML
        )
