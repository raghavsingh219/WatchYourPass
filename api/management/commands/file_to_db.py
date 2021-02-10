from multiprocessing.context import Process
from threading import Thread

from django.core.management.base import BaseCommand, CommandError
import os,time,hashlib,mmap,errno
from django import db
from django.db import connection, connections
import re

from django.db.utils import load_backend


class Command(BaseCommand):
    help = 'Adds file data to db'

    def _create_and_populate_tmp_table_from_file(self,file_path,file_name,cursor):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # read sql from tmp_tbl.sql and create tmp table
        with open(os.path.join(dir_path,'sql/tmp_tbl.sql'),'r') as f:
            cursor.execute(f.read())

        # populating tmp table
        with open(os.path.join(dir_path, 'sql/populate_tmp_tbl.sql'), 'r') as f:
            cursor.execute(f.read())
            cursor.execute("CALL populate_tmp('"+os.path.abspath(os.path.join(file_path,file_name))+"')")
            os.remove(os.path.abspath(os.path.join(file_path,file_name)))

    def _populate_domain_table(self,dir_path,cursor):
        with open(os.path.join(dir_path, 'sql/populate_domain_table.sql'), 'r') as f:
            cursor.execute(f.read())

    def _populate_password_table(self,dir_path,cursor):
        with open(os.path.join(dir_path, 'sql/populate_password_table.sql'), 'r') as f:
            cursor.execute(f.read())

    def _populate_account_table(self, dir_path, cursor):
        with open(os.path.join(dir_path, 'sql/populate_account_table.sql'), 'r') as f:
            cursor.execute(f.read())


    def _populate_all_tables(self,cursor):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        t1=Thread(target=self._populate_domain_table(dir_path,cursor))
        t2=Thread(target=self._populate_password_table,args=(dir_path, cursor))
        t3=Thread(target=self._populate_account_table,args=(dir_path ,cursor))

        t2.start()
        t1.start()
        t1.join()
        t3.start()
        t2.join()
        t3.join()

        with open(os.path.join(dir_path, 'sql/populate_relation_table.sql'), 'r') as f:
            cursor.execute(f.read())

    def add_arguments(self, parser):
        parser.add_argument('folder_path', type=str)

    def files(self,path):
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                yield file

    def handle(self, *args, **kwargs):
        start_time = time.time()
        folder_path = kwargs['folder_path']
        no_of_lines = 1
        lines = []

        if os.path.exists(os.path.join(folder_path,'tmp.txt')):
            os.remove(os.path.join(folder_path,'tmp.txt'))

        if os.path.exists(folder_path):  # if folder_path exists

            for filename in self.files(os.path.abspath(folder_path)):
                if filename!='tmp.txt':
                    with open(os.path.join(folder_path,filename), 'r+b') as f:
                        mm = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)

                        for linee in iter(mm.readline, b""):
                            # convert the bytes to a utf-8 string and split the fields
                            no_of_lines+=1
                            try:
                                line = linee.decode()
                                email = line.split('@')[0].lower()

                                domain = line.split('@')[1].split(':')[0].lower()
                                hashedPassword = hashlib.sha256(line.split('@', 1)[1].split(':')[1].encode()).hexdigest()
                                lines.append(email+";"+domain+";"+hashedPassword)
                            except Exception as e:
                                pass
                        tmp_file_name = 'tmp.txt'
                        tmp_file_path = os.path.dirname(folder_path)

                        with open(os.path.join(tmp_file_path, tmp_file_name), 'w') as f:
                            for line in lines:
                                f.write(line + "\n")

                        with connection.cursor() as c:
                            self._create_and_populate_tmp_table_from_file(tmp_file_path, tmp_file_name, c)
                            self._populate_all_tables(c)
                        elapsed_time = time.time() - start_time

            print("Number of lines:"+str(no_of_lines))

            print("Elapsed time:"+str(elapsed_time))
        else:
            raise CommandError(
                errno.ENOENT, os.strerror(errno.ENOENT), os.path.basename(folder_path)
            )


