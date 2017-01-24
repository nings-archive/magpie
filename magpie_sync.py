'''
Magpie.sync
'''

class Sync:
    def __init__(self, bot):
        '''
        initiate with telegram.Bot obj
        '''
        self.bot = bot

    def new_updates(self):
        '''
        returns list[telegram.Update]
        '''
        updates = self.bot.getUpdates()

        # reset updates
        if len(updates) != 0:
            update_id_last = int(updates[-1].update_id)
            update_id_next = str(update_id_last+1)
            self.bot.getUpdates(offset=update_id_next)

        return updates

    @staticmethod
    def get_file_id(update):
        '''
        returns file_id of attached media
        returns None if no attached media
        '''
        # audio
        try:
            return update.message.audio.file_id
        except AttributeError:
            pass
        # document
        try:
            return update.message.document.file_id
        except AttributeError:
            pass
        # photo
        try:
            return update.message.photo[-1].file_id
        except AttributeError:
            pass
        # video
        try:
            return update.message.video.file_id
        except AttributeError:
            pass
        # voice
        try:
            return update.message.voice.file_id
        except AttributeError:
            pass
        # no media
        return None

    def download(self, file_id, dl_dir):
        '''
        downloads media of file_id to dl_dir
        '''
        file_ob = self.bot.getFile(file_id)
        file_name = file_ob.file_path
        file_name = file_name[file_name.rfind('/')+1:]
        file_ob.download(dl_dir+file_name)
