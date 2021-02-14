from multiprocessing.context import Process
import multiprocessing
from threading import Thread

from django.core.management.base import BaseCommand, CommandError
import os,time,hashlib,mmap,errno

from django.db import connection, connections
from django import db

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
        with open(os.path.join(dir_path, 'sql/create_and_populate_tmp_password.sql'), 'r') as tmp_pwd,open(dir_path, 'sql/create_tmp2_password.sql') as tmp2_pwd:
            cursor.execute(tmp_pwd.read())
            cursor.execute(tmp2_pwd.read())

    def _populate_account_table(self, dir_path, cursor):
        with open(os.path.join(dir_path, 'sql/populate_account_table.sql'), 'r') as f:
            cursor.execute(f.read())


    def _populate_all_tables(self):
        strt=time.time()
        cursor=connection.cursor()
        dir_path = os.path.dirname(os.path.realpath(__file__))

        t1=Thread(target=self._populate_domain_table(dir_path,cursor))
        t2=Thread(target=self._populate_password_table,args=(dir_path, cursor))
        t3=Thread(target=self._populate_account_table,args=(dir_path ,cursor))

        t2.start()
        t1.start()
        t1.join()
        print("Populated domain table in:"+str(time.time()-strt))
        strtt=time.time()
        t3.start()
        t2.join()
        print("Populated password table in:" + str(time.time() - strt))
        t3.join()
        print("Populated account table in:"+str(time.time()-strtt))

        strtt=time.time()
        with open(os.path.join(dir_path, 'sql/populate_relation_table.sql'), 'r') as f:
            cursor.execute(f.read())
        print("Populated relation table in:"+str(time.time()-strtt))
        print("Populated all tables in:" + str(time.time() - strt))

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
        prevthread=None
        if os.path.exists(folder_path):  # if folder_path exists
            tmp_file_name = 'tmp.txt'
            for filename in self.files(os.path.abspath(folder_path)):
                print("Processing :" + str(filename))
                if os.path.exists(os.path.join(folder_path, tmp_file_name)):
                    os.remove(os.path.join(folder_path, tmp_file_name))
                if filename!=tmp_file_name:
                    with open(os.path.join(folder_path,filename), 'r+b') as f,open(os.path.join(folder_path,tmp_file_name),'w',encoding='utf-8') as destf:
                        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

                        for linee in iter(mm.readline, b""):
                            # convert the bytes to a utf-8 string and split the fields
                            no_of_lines+=1
                            try:
                                line = linee.decode('utf-8')
                                email = line.split('@')[0].lower()
                                domain = line.split('@')[1].split(':')[0].lower()
                                hashedPassword = hashlib.sha256(line.split('@', 1)[1].split(':')[1].encode()).hexdigest()
                                destf.write(email+";"+domain+";"+hashedPassword+"\n")
                            except Exception as e:
                                print(e)
                                pass

                    t=Thread(target=self._populate_all_tables)
                    with connection.cursor() as c:
                        if prevthread:
                            print("Waiting for process:"+str(prevthread.name))
                            prevthread.join()
                        self._create_and_populate_tmp_table_from_file(folder_path, tmp_file_name, c)
                        db.connections.close_all()
                        prevthread=t
                        t.start()


            elapsed_time = time.time() - start_time

            print("Number of lines:"+str(no_of_lines))

            print("Elapsed time:"+str(elapsed_time))
        else:
            raise CommandError(
                errno.ENOENT, os.strerror(errno.ENOENT), os.path.basename(folder_path)
            )


