import telegram
# config.py
import config
# Sync class
import magpie_sync

bot = telegram.Bot(config.TELEGRAM_BOT_TOKEN)
sync = magpie_sync.Sync(bot)
# fetcher = magpie_fetcher.Fetcher(bot)

for update in sync.new_updates():
    file_id = sync.get_file_id(update)
    if file_id != None:
        sync.download(file_id, config.SYNC_DIR)
