from .FileTransfer import FileTransfer


class Upload(FileTransfer):

    def __init__(self, archive_project, audio_utility, file_utility, takeDatabase):       #these objects come from file transfer
        self.takeDatabase = takeDatabase
        super().__init__(archive_project, audio_utility, file_utility)

    def upload(self, file):
        directory = self.file_utility.rootDir(['media','dump'])
        resp, stat, ext = self.archive_project.extract(file, directory)   #returns response, status, and file extension
        if resp == 'ok':
            resp, stat = self.file_utility.processUploadedTakes(directory, self.takeDatabase, ext)

        return resp, stat



