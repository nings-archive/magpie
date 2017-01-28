'''
magpie_sync
'''

class Sync:
    '''
    Handle interactions with telegram.update
    '''

    def __init__(self, bot):
        '''
        Initiate sync with telegram.Bot
        '''
        self.bot = bot

    def new_updates(self):
        '''
        Return list of telegram.update

        Also clears get_updates() using offset
        '''
        updates = self.bot.get_updates()

        # reset updates
        if len(updates) != 0:
            update_id_last = int(updates[-1].update_id)
            update_id_next = str(update_id_last+1)
            self.bot.get_updates(offset=update_id_next)

        return updates

    @staticmethod
    def get_file_id(update):
        '''
        Return file_id of attached telegram.Update media

        ARGUMENTS
        update: telegram.update

        Return None if no media
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
        Download media of file_id to dl_dir

        ARGUMENTS
        file_id: file_id (str) attribute of telegram.(media)
        dl_dir: directory to be downloaded to (CONFIG)
        '''
        file_ob = self.bot.getFile(file_id)
        file_name = file_ob.file_path
        file_name = file_name[file_name.rfind('/')+1:]
        file_ob.download(dl_dir+file_name)
