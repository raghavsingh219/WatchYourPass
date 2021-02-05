from multiprocessing.context import Process
from threading import Thread

from django.core.management.base import BaseCommand, CommandError
import os,time,hashlib,mmap,errno

from django.db import connection, connections
import re

from django.db.utils import load_backend


class Command(BaseCommand):
    help = 'Adds file data to db'

    def _new_db_connection(alias='default'):
        """Returns a new database connection.
        Use with RawSQL to execute the query using new connection. If you run a
        query in a new process, see users.helpers.timeout(), it will throw
        "OperationalError: SSL error: decryption failed or bad record mac". You
        can either (1) close the current connection and Django will create new one
        or (2) use a new connection. Note that if you are inside a database
        transaction, you cannot close the current connection.
        """
        connections.ensure_defaults(alias)
        connections.prepare_test_settings(alias)
        db = connections.databases[alias]
        backend = load_backend(db['ENGINE'])
        return backend.DatabaseWrapper(db, alias)

    def _create_and_populate_tmp_table_from_file(self,file_path,file_name,cursor):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # read sql from tmp_tbl.sql and create tmp table
        with open(os.path.join(dir_path,'sql/tmp_tbl.sql'),'r') as f:
            cursor.execute(f.read())

        # populating tmp table
        with open(os.path.join(dir_path, 'sql/populate_tmp_tbl.sql'), 'r') as f:
            cursor.execute(f.read())
            cursor.execute("CALL populate_tmp('"+os.path.abspath(os.path.join(file_path,file_name))+"')")

    def _populate_password_table(self,dir_path,cursor):
        with open(os.path.join(dir_path, 'sql/populate_password_table.sql'), 'r') as f:
            cursor.execute(f.read())

    def _populate_account_table(self, dir_path, cursor):
        with open(os.path.join(dir_path, 'sql/populate_account_table.sql'), 'r') as f:
            cursor.execute(f.read())


    def _populate_all_tables(self,cursor):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        with open(os.path.join(dir_path, 'sql/populate_domain_table.sql'), 'r') as f:
            cursor.execute(f.read())

        t1=Thread(target=self._populate_password_table,args=(dir_path, cursor))
        t2=Thread(target=self._populate_account_table,args=(dir_path ,cursor))

        t1.start()
        t2.start()
        t1.join()
        t2.join()
        with open(os.path.join(dir_path, 'sql/populate_relation_table.sql'), 'r') as f:
            cursor.execute(f.read())

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **kwargs):
#
#         cursor = connection.cursor()
#         cursor.execute("create procedure abc() "+
#             "language plpgsql "+
# "as $$ "+
# "begin "+
# "insert into api_domain(domain,count) values('abc',10); "+
# "commit; "+
# "end;$$; ")


        start_time = time.time()
        file_path = kwargs['file_path']
        if os.path.exists(file_path):  # if file_path exists
            with open(file_path, 'r+b') as f:
                mm = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
                lines=[]
                for linee in iter(mm.readline, b""):
                    # convert the bytes to a utf-8 string and split the fields
                    line = linee.decode()
                    email = line.split('@')[0].lower()
                    domain = line.split('@')[1].split(':')[0].lower()
                    hashedPassword = hashlib.sha256(line.split('@', 1)[1].split(':')[1].encode()).hexdigest()
                    lines.append(email+";"+domain+";"+hashedPassword)

                tmp_file_name='tmp.txt'
                tmp_file_path='/tmp'

                with open(os.path.join(tmp_file_path,tmp_file_name), 'w') as f:
                    for line in lines:
                        f.write(line+"\n")

                with connection.cursor() as c:
                    self._create_and_populate_tmp_table_from_file(tmp_file_path,tmp_file_name,c)
                    self._populate_all_tables(c)
            elapsed_time=time.time()-start_time

            print("Elapsed time:"+str(elapsed_time))

        else:
            raise CommandError(
                errno.ENOENT, os.strerror(errno.ENOENT),os.path.basename(file_path)
            )
