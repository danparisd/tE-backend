import hashlib
import json
import os
import zipfile

from api.models import Take

from .ArchiveProject import ArchiveProject


class ZipIt(ArchiveProject):

    def archive(self):
        pass

    @staticmethod
    def extract(file, directory, user, update_progress, task_args):
        try:
            with zipfile.ZipFile(file, "r") as zip_file:
                takes = zip_file.infolist()
                diff_list = ZipIt.get_diff_list(ZipIt.get_files(zip_file), zip_file)
                keys = set().union(*(d.keys() for d in diff_list))
                current_take = 0
                for i, take in enumerate(takes):
                    filename = take.filename
                    if filename in keys:
                        if len(filename) == 12:
                            loc = os.path.join(os.path.dirname(directory), "name_audios")
                            zip_file.extract(take, loc)
                            continue
                        if len(filename) > 12 and filename.endswith(".mp3"):
                            loc = os.path.join(os.path.dirname(directory), "comments")
                            zip_file.extract(take, loc)
                            continue
                        zip_file.extract(take, directory)

                        current_take += 1

                        if update_progress and task_args:
                            # 1/2 of overall task
                            progress = int(((current_take / len(takes) * 100) / 2))

                            new_task_args = task_args + (progress, 100, 'Extracting takes...', {
                                'user_icon_hash': user["icon_hash"],
                                'user_name_audio': user["name_audio"],
                                'lang_slug': "--",
                                'lang_name': "--",
                                'book_slug': "--",
                                'book_name': "--",
                                'result': str(take.filename)
                            })
                            update_progress(*new_task_args)

            return 'ok', 200

        except zipfile.BadZipfile as e:
            return e, 400

    @staticmethod
    def get_files(zip_file):
        for file in zip_file.infolist():
            if file.filename == "manifest.json":
                with zip_file.open(file) as f:
                    contents = f.read()
                    manifest_file = json.loads(contents.decode("utf-8"))
                    lang = manifest_file["language"]["slug"]
                    book = manifest_file["book"]["slug"]
                    version = manifest_file["version"]["slug"]
                    anthology = manifest_file["anthology"]["slug"]

        return ZipIt.get_takes(lang, book, version, anthology)

    @staticmethod
    def get_takes(lang, book, version, anthology):
        return Take.objects.filter(chunk__chapter__project__language__slug__iexact=lang).filter(
            chunk__chapter__project__anthology__slug__iexact=anthology).filter(
            chunk__chapter__project__version__slug__iexact=version).filter(
            chunk__chapter__project__book__slug__iexact=book)

    @staticmethod
    def get_local_file_hash(location):
        hash_md5 = hashlib.md5()
        with open(location, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b''):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    @staticmethod
    def get_zip_file_hash(zip_file, location):
        hash_md5 = hashlib.md5()
        with zip_file.open(location, "r") as file:
            for chunk in iter(lambda: file.read(4096), b''):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    @staticmethod
    def local_file_hash_list(file_list):
        hashes = []
        for file in file_list:
            hashes.append({file.name: ZipIt.get_local_file_hash(file.location)})
        return hashes

    @staticmethod
    def zip_file_hash_list(zip_file):
        hashes = []
        for file in zip_file.infolist():
            hashes.append({file.filename: ZipIt.get_zip_file_hash(zip_file, file)})
        return hashes

    @staticmethod
    def get_diff_list(local_file_list, zip_file):
        local_list = ZipIt.local_file_hash_list(local_file_list)
        zip_list = ZipIt.zip_file_hash_list(zip_file)
        return [x for x in local_list + zip_list if x not in local_list or x not in zip_list]
