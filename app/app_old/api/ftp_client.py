import os
import sys
from ftplib import FTP

BYTE_IN_MB = 1024

BYTE_IN_GB = 1073741824

sys.path.append('/home/pi/picam/app')
# print(sys.path)
from settings import *


class FTPUploader(object):

    def __init__(self, debug=0, *args, **kwargs):
        self.ftp = FTP(timeout=120)
        self.ftp.set_debuglevel(debug)
        self.ftp.connect(FTP_HOST, FTP_PORT)
        self.ftp.login(FTP_USER, FTP_PASS)
        self.ftp.cwd(FTP_ARCHIVE_PATH)

    @staticmethod
    def __get_photos_from_path(abs_path):
        lst = sorted(list(filter(lambda x: x.endswith('.jpg') and not 'thumbnail' in x, os.listdir(abs_path))))
        return ["{}".format(file) for file in lst]

    def __ftp_upload(self, localfile):
        with open(localfile, 'rb') as fp:
            self.ftp.storbinary('STOR %s' % os.path.basename(localfile), fp, 1024)

    def __get_files_from_ftp_dir(self):
        files = []
        try:
            files = self.ftp.nlst()
        except (FTP.error_perm, resp):
            if str(resp) == "550 No files found":
                print("No files in this directory")
            else:
                raise
        return files

    def __upload_img(self, file):
        self.__ftp_upload("{}/{}".format(RAM_DISK_ABS_PATH, file))

    def run(self):
        try:
            print("==== CALC SIZE PHOTOS =====")
            ftp_files = self.__clear_dir()
            print("==== COPY PHOTOS =====")
            index = 0
            for img in set(self.__get_photos_from_path(RAM_DISK_ABS_PATH)) - set(ftp_files):
                try:
                    self.__upload_img(img)
                except Exception as error:
                    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                    print(template.format(type(error).__name__, error.args))
                    continue
                index += 1
            print("==== COPIED {} PHOTOS =====".format(index))
        except Exception as e:
            raise e
        finally:
            self.ftp.quit()

    def __clear_dir(self):
        size = 0
        files = []
        for name, facts in self.ftp.mlsd():
            if name in ['.', '..']:
                continue
            files.append([name, int(facts.get('size', 0))])
            size += int(facts.get('size', 0))
        print("==== CALC SIZE: {:.2f} Mb ====".format(size / BYTE_IN_GB * BYTE_IN_MB))
        if size > FTP_SIZE:
            files.sort()
            diff_size = abs(size - FTP_SIZE)
            lst_files_del = self.__get_files_del(files, diff_size)
            print("==== REMOVE {} PHOTOS =====".format(len(lst_files_del)))
            for f in lst_files_del:
                self.ftp.delete(f)
        return [name for name, s in files]

    @staticmethod
    def __get_files_del(files, size):
        count_size = 0
        new_files = []
        for name, s in files:
            if count_size >= size:
                break
            count_size += s
            new_files.append(name)
        return new_files


if __name__ == '__main__':
    FTPUploader().run()
