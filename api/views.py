import multiprocessing
from multiprocessing import Pool

from django.shortcuts import render
from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Domain, BreachedSite, Password, Account
from .serializers import UserSerializer, DomainSerializer, Breached_SiteSerializer, PasswordSerializer, EmailSerializer, \
    UploadSerializer
from django.contrib.auth.models import User
import re
import hashlib
from django.db import IntegrityError
from urllib.parse import unquote
from rest_framework.viewsets import ViewSet

comboMatchRegex = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+:{1,1}[a-zA-Z0-9 !\"#$%&\'()*+,-.\/:;<=>?@[\\]^_`{|}~]+$'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=['POST'])
    def add_domain(self, request, **kwargs):
        if 'domain' in request.data:
            domain = request.data['domain']
            if '@' in domain and '.' in domain:
                try:
                    domain = Domain.objects.get(domain=domain)
                    domain.count = domain.count + 1
                    domain.save(update_fields=['count'])
                    serializer = DomainSerializer(domain, many=False)
                    response = {'already exists': 'the domain already exists, incrementing counter by 1',
                                'result': serializer.data}
                    return Response(response, status=status.HTTP_200_OK)
                except:
                    try:
                        domain = Domain.objects.create(domain=domain)
                        serializer = DomainSerializer(domain, many=False)
                        response = {'created': 'domain hasn\'t been seen before adding to system',
                                    'result': serializer.data}
                        return Response(response, status=status.HTTP_200_OK)
                    except Exception as e:
                        response = {'error': str(e)}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                response = {'error': 'your request must include a valid email domain'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {'error': 'your request must include a valid email domain'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class PasswordViewSet(viewsets.ModelViewSet):
    queryset = Password.objects.all()
    serializer_class = PasswordSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=['POST'])
    def add_password(self, request, **kwargs):
        if 'hash' in request.data:
            hash = request.data['hash']
            if len(hash) == 64:
                try:
                    password = Password.objects.get(hash=hash)
                    password.count = password.count + 1
                    password.save(update_fields=['count'])
                    serializer = PasswordSerializer(password, many=False)
                    response = {'already exists': 'the password already exists, incrementing counter by 1',
                                'result': serializer.data}
                    return Response(response, status=status.HTTP_200_OK)
                except:
                    try:
                        password = Password.objects.create(hash=hash)
                        serializer = PasswordSerializer(password, many=False)
                        response = {'created': 'password hasn\'t been seen before adding to system',
                                    'result': serializer.data}
                        return Response(response, status=status.HTTP_200_OK)
                    except Exception as e:
                        response = {'error': str(e)}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                response = {'error': 'your request must include a valid password'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {'error': 'your request must include a valid password'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class EmailViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = EmailSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    class DualSerializerViewSet(viewsets.ModelViewSet):
        def get_serializer_class(self):
            if self.action == 'list':
                return serializers.ListaGruppi
            if self.action == 'retrieve':
                return serializers.DettaglioGruppi
            return EmailSerializer

    @action(detail=False, methods=['POST'])
    def add_combo(self, request, **kwargs):
        if 'combo' in request.data:
            combo = request.data['combo']
            if '%40' in combo:
                combo = unquote(combo)
            if re.match(comboMatchRegex, combo):
                splitCombo = combo.split(':')
                email = splitCombo[0].split('@')[0]
                domain = splitCombo[0].split('@')[1]
                password = ''
                hashedPassword = ''
                for piece in splitCombo[1:]:
                    password += piece
                hashedPassword = hashlib.sha256(password.encode()).hexdigest()
                try:
                    response = {}
                    # password
                    try:
                        passwordObject = Password.objects.create(hash=hashedPassword, count=1)
                        serializer = PasswordSerializer(passwordObject, many=False)
                        response["password"] = "hasn't been seen before adding to database"
                        response["password result"] = serializer.data
                    except IntegrityError as e:
                        if 'UNIQUE constraint' in str(e):
                            passwordObject = Password.objects.get(hash=hashedPassword)
                            passwordObject.count = passwordObject.count + 1
                            passwordObject.save(update_fields=['count'])
                            serializer = PasswordSerializer(passwordObject, many=False)
                            response["password"] = "is already in database incrementing count by 1"
                            response["password result"] = serializer.data
                    except Exception as e:
                        response["password"] = str(e)
                    # domain
                    try:
                        domainObject = Domain.objects.create(domain=domain, count=1)
                        serializer = DomainSerializer(domainObject, many=False)
                        response["domain"] = "hasn't been seen before adding to database"
                        response["domain result"] = serializer.data
                    except IntegrityError as e:
                        if 'UNIQUE constraint' in str(e):
                            domainObject = Domain.objects.get(domain=domain)
                            domainObject.count = domainObject.count + 1
                            domainObject.save(update_fields=['count'])
                            serializer = DomainSerializer(domainObject, many=False)
                            response["domain"] = "is already in database incrementing count by 1"
                            response["domain result"] = serializer.data
                    except Exception as e:
                        response["domain"] = str(e)
                    # email
                    try:
                        domainObject = Domain.objects.get(domain=domain)
                        passwordObject = Password.objects.get(hash=hashedPassword)
                        emailObject = Account.objects.create(email=email, domain=domainObject)
                        emailObject.passwords.add(passwordObject)
                        serializer = EmailSerializer(emailObject, many=False)
                        response["account"] = "hasn't been seen before adding to database"
                        response["account result"] = serializer.data
                    except IntegrityError as e:
                        if 'UNIQUE constraint' in str(e):
                            domainObject = Domain.objects.get(domain=domain)
                            passwordObject = Password.objects.get(hash=hashedPassword)
                            emailObject = Account.objects.get(email=email, domain=domainObject)
                            try:
                                emailObject.objects.get(passwords_hash=hashedPassword)
                                emailObject.count = emailObject.count + 1
                                emailObject.save(update_fields=['count'])
                                serializer = EmailSerializer(emailObject, many=False)
                                response["account"] = "is already in database incrementing count by 1"
                                response["account result"] = serializer.data
                            except:
                                emailObject.passwords.add(passwordObject)
                                emailObject.count = emailObject.count + 1
                                emailObject.save(update_fields=['count'])
                                serializer = EmailSerializer(emailObject, many=False)
                                response[
                                    "account"] = "account only in database, but password isn't adding password and incrementing by 1"
                                response["account result"] = serializer.data
                    except Exception as e:
                        response["account"] = str(e)

                    return Response(response, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
            else:
                response = {'error': 'your request must include a valid combo'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        else:
            print("no combo")
            response = {'error': 'your request must include a valid combo'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class BulkUploadViewSet(ViewSet):
    serializer_class = UploadSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def add_combo(self, combo):
        return Response('')

    def create(self, request):
        response = request.FILES.get('file_uploaded').read().decode("utf-8")
        custom_regex = "[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+:{1,1}[a-zA-Z0-9 !\"#$%&\'()*+,-.\/:;<=>?@[\\]^_`{|}~]+"
        valid_combos = re.findall(custom_regex, response)
        with multiprocessing.Pool(5) as p:
            pass
            #print(p.map(self.add_combo, [1, 2, 3, 4, 5, 6, 7]))
        return Response((valid_combos))
