import logging
import telegram, telegram.ext
import lsm_helpers

CommandHandler = telegram.ext.CommandHandler

class Bot(telegram.Bot):
    def __init__(self, *, token, admin_id):
        telegram.Bot.__init__(self, token=token)
        self.admin_id = admin_id

    def listen(self):
        self.updater = telegram.ext.Updater(bot=self)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(CommandHandler('get_random_dsDNA', 
            self.get_random_dsDNA, pass_args=True))
        self.updater.start_polling()
        self.updater.idle()

    def get_random_dsDNA(self, bot, update, args):
        if args == []: args = [7]  # set a default value
        # try:
        length = int(args[0])
        seq = lsm_helpers.get_random_dsDNA(length)
        text = "<code>3'--{}--5'\n5'--{}--3'</code>".format(
            ''.join(seq[0]), ''.join(seq[1]))
        self.send(update.message.chat_id, text)
        # except Exception as error:
        #    text = "<code>ERR: {}</code>".format(str(error))
        #    self.send(update.message.chat_id, text)
        #    logging.info(error)  # raise it to logging anyway
                

    def send_me(self, text):
        return super().send_message(
            chat_id=self.admin_id,
            text=text,
            parse_mode=telegram.ParseMode.HTML
        )

    def send(self, chat_id, text):
        return super().send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=telegram.ParseMode.HTML
        )
