from asyncio.subprocess import Process
from multiprocessing.dummy import Process

from django.core.management.base import BaseCommand, CommandError
import os,time,re,mmap,hashlib,math
import multiprocessing
import errno
from api.models import Account, Domain, Password
from collections import Counter
from collections import defaultdict
from django.apps import apps
from concurrent.futures import ProcessPoolExecutor
from django import db


class BulkCreateManager(object):
    """
    This helper class keeps track of ORM objects to be created for multiple
    model classes, and automatically creates those objects with `bulk_create`
    when the number of objects accumulated for a given model class exceeds
    `chunk_size`.
    Upon completion of the loop that's `add()`ing objects, the developer must
    call `done()` to ensure the final set of objects is created for all models.
    """

    def __init__(self, chunk_size=100):
        self._create_queues = defaultdict(list)
        self.chunk_size = chunk_size

    def _commit(self, model_class):
        model_key = model_class._meta.label
        model_class.objects.bulk_create(self._create_queues[model_key])
        self._create_queues[model_key] = []

    def add(self, obj):
        """
        Add an object to the queue to be created, and call bulk_create if we
        have enough objs.
        """
        model_class = type(obj)
        model_key = model_class._meta.label
        self._create_queues[model_key].append(obj)
        if len(self._create_queues[model_key]) >= self.chunk_size:
            self._commit(model_class)

    def done(self):
        """
        Always call this upon completion to make sure the final partial chunk
        is saved.
        """
        for model_name, objs in self._create_queues.items():
            if len(objs) > 0:
                self._commit(apps.get_model(model_name))

class Command(BaseCommand):
    help = 'Adds file data to db'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def _divide_chunks(self,lst, n):

        # looping till length l
        p=math.ceil(len(lst)/n)
        for i in range(0, len(lst), p):
            yield lst[i:i + p]

    def _get_object_from_domain(self,domain,domain_objects):
        for obj in domain_objects:
            if domain == obj.domain:
                return obj

    def _get_object_from_password(self,password_hash,password_objects):
        for obj in password_objects:
            if password_hash == obj.hash:
                return obj

    def _get_pwd_id_lst(self,email__domain__hashed_pass,pwd_id_lst):
        get_pwd_id_lst=[Password.objects.get(hash=pwd_obj[2]) for pwd_obj, count in email__domain__hashed_pass.items()]
        return get_pwd_id_lst

    def handle(self, *args, **kwargs):
        start_time = time.time()
        file_path=kwargs['file_path']
        if os.path.exists(file_path):  # if file_path exists

            with open(file_path, 'r+b') as f:
                mm = mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ)
                # iterate over the block, until next newline

                domains=[]
                hashed_passwords=[]
                email__domain__hashed_pass=[]


                for linee in iter(mm.readline, b""):
                    # convert the bytes to a utf-8 string and split the fields
                    line=linee.decode()
                    email=line.split('@')[0].lower()
                    domain=line.split('@')[1].split(':')[0].lower()
                    hashedPassword = hashlib.sha256(line.split('@', 1)[1].split(':')[1].encode()).hexdigest()

                    email__domain__hashed_pass.append((email,domain,hashedPassword))
                    hashed_passwords.append(hashedPassword)
                    domains.append(domain)

                domains=(Counter(domains))
                hashed_passwords=(Counter(hashed_passwords))
                email__domain__hashed_pass = Counter(email__domain__hashed_pass)


                bulk_mgr = BulkCreateManager(chunk_size=150000)


                def domain_db_worker(domain_bulk_mgr):
                    domain_objects = [domain_bulk_mgr.add(Domain(domain=domain, count=count)) for domain, count in domains.items()]

                def password_hash_db_worker(hash_bulk_mgr):
                    hashed_password_objects = [bulk_mgr.add(Password(hash=hash, count=count)) for hash, count in hashed_passwords.items()]

                print("Creating hashed password objects...", end="")
                hashed_password_objects = [Password(hash=hash, count=count) for hash, count in hashed_passwords.items()]
                print("done")

                # p2=Process(target=password_hash_db_worker,args=(hashed_password_bulk_mgr,))
                print("saving hashed password objects...", end="")

                # Password.objects.bulk_create(hashed_password_objects)
                p1=Process(target=Password.objects.bulk_create,args=(hashed_password_objects,))
                p1.start()
                p1.join()
                print("done")

                elapsed_time = time.time() - start_time

                print("Elapsed time:" + str(elapsed_time))
                print("Getting pwd_id_lst")
                pwd_id_mgr=multiprocessing.Manager()
                get_pwd_id_list=pwd_id_mgr.list()
                # get_pwd_id_list = [Password.objects.get(hash=pwd_obj[2]) for pwd_obj, count in email__domain__hashed_pass.items()]


                p2=Process(target=self._get_pwd_id_lst,args=(email__domain__hashed_pass,get_pwd_id_list))
                p2.start()

                domain_objects = [Domain(domain=domain, count=count) for domain, count in
                                  domains.items()]
                print("Created domain_objects")
                saved_domain_objects=Domain.objects.bulk_create(domain_objects)
                print("Saved domain objects")
                elapsed_time = time.time() - start_time

                print("Elapsed time:" + str(elapsed_time))


                print("Creating email__domain_objects...",end="")
                email__domain_objects = [
                    Account(
                        email=obj[0],
                        domain=self._get_object_from_domain(obj[1],saved_domain_objects),
                        count=count) for obj, count in email__domain__hashed_pass.items()
                ]
                print("done")
                elapsed_time = time.time() - start_time

                print("Elapsed time:" + str(elapsed_time))
                print("saving account account objects...",end="")

                saved_account_objects = Account.objects.bulk_create(email__domain_objects, ignore_conflicts=True)
                print("done")


                p2.join()
                print("Creating through_objs")
                through_objs=[]
                for i in range(0,len(saved_account_objects)):
                    through_objs.append(
                        Account.passwords.through(
                        account_id=saved_account_objects[i].id,
                        password_id=get_pwd_id_list[i].id
                        )
                    )
                Account.passwords.through.objects.bulk_create(through_objs,ignore_conflicts=True)


                # for obj in email__domain_objects:
                #     email__domain__hashed_pass_objects=obj.passwords.add(Password.objects.get(passwords=))


                elapsed_time = time.time() - start_time

                print("Elapsed time:" + str(elapsed_time))


        else:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT),os.path.basename(file_path)
            )




