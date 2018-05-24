import telegram, telegram.ext

import subprocess

def get_uptime(bot, update):
    bot.send_message(
        chat_id=update.message.chat_id,
        text='<code>{}</code>'.format(_get_uptime()),
        parse_mode=telegram.ParseMode.HTML
    )

def _get_uptime():
    hostname = subprocess.check_output(('hostname',)).decode().strip()
    uptime = subprocess.check_output(('uptime', '-p')).decode()
    return '{}: {}'.format(hostname, uptime)

commands = (telegram.ext.CommandHandler('osuptime', get_uptime),)
