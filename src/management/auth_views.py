from django.conf import settings
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import DatabaseError
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.crypto import get_random_string

from .models import User, UserAccessToken
from .serializers import UserLoginSerializer

from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed, APIException, ValidationError

import logging


class KeepAv(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None, **kwargs):
        return Response({
            'status': 'ok'
        })


# Create your views here.
class CustomAuthToken(ObtainAuthToken, APIView):
    # authentication_classes = []
    # permission_classes = []
    throttle_classes = [UserRateThrottle]
    throttle_scope = 'user'

    def post(self, request, *args, **kwargs):
        
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )

        status_token = status.HTTP_200_OK
        message = ''

        try:
            serializer.is_valid(raise_exception=True)   
            user = serializer.validated_data['user']
                     
            Token.objects.filter(user=user).delete()

            if (settings.AVOID_2FA == False):
                user, status_token = self.getToken2FA(self.request, user)

                if user:
                    if (request.data['auth_selection'] == 1):
                        status_token = self.send2FAEmail(user)
                        message = 'Check your inbox and follow the instructions.'
                    elif (request.data['auth_selection'] == 2):
                        if (len(user.user.phone.strip())==13):
                            self.send2FASMS(user)
                            message = 'Type the code sent to your mobile phone.'
                        else:
                            raise Exception('contact_phone_invalid')

                return Response({'message': message}, status=status_token, headers={})
            else:
                token, create = Token.objects.update_or_create(user=user)

                from django.contrib.auth.models import update_last_login
                update_last_login(None, user)

                userSerializer = UserLoginSerializer(user, many=False)

                return Response({
                    'token': token.key,
                    'user': userSerializer.data,
                })

        except ValidationError as e:
            status_token = status.HTTP_200_OK
            message = 'credentials_incorrect'
            return Response({'message': message}, status=status_token, headers={})
        except DatabaseError as e:
            status_token = status.HTTP_200_OK
            message = 'd_error'
            return Response({'message': message}, status=status_token, headers={})
        except Exception as e:
            status_token = status.HTTP_200_OK
            message = 'something_wrong'
            if len(e.args)>0:
                message = e.args[0]
            return Response({'message': message}, status=status_token, headers={})
        
    def getToken2FA(self, request, user):
        from django.contrib.auth.tokens import PasswordResetTokenGenerator

        token = None
        status_token = None
        usr = None

        try:
            prg = PasswordResetTokenGenerator()
            token = prg.make_token(user)

            if token:
                status_token = status.HTTP_201_CREATED

                usr = UserAccessToken.objects.filter(user = user)
                try:
                    usr.delete()
                except Exception as e:
                    pass

                usr = UserAccessToken.objects.create(
                    user = user,
                    token = token
                )
            else:
                status_token = status.HTTP_406_NOT_ACCEPTABLE
        except Exception as e:
            raise Exception("Error")
        finally:
            return usr, status_token
        
    def send2FAEmail(self, user):
        from django.core.mail import send_mail
        from django.contrib.auth.tokens import PasswordResetTokenGenerator
        from django.urls import reverse

        status_token = status.HTTP_201_CREATED

        try:
            msg_plain = render_to_string('2FA.txt', {'user': user.user.username, 'token': settings.URL_BASE + '/#'+ reverse('generate-password') + user.user.email + '/'+user.token[-8:]+'/'})
            msg_html = render_to_string('2FA.html', {'user': user.user.username, 'token': user.token[-8:]})

            msg = EmailMessage('DetectOne Authentication', msg_html, settings.EMAIL_HOST_USER, [user.user.email])
            msg.content_subtype = "html"  
            msg.send()

        except Exception as e:
            status_token = status.HTTP_406_NOT_ACCEPTABLE
            raise Exception("Error")
        finally:
            return status_token

    def send2FASMS(self, user):
        logging.debug(f"[2FA SMS] >> SEND SMS")
        nogas_client = settings.NOGAS_RNA
        # contacts = settings.CONTACTS
        status_token = status.HTTP_201_CREATED
         
        sms_msj = f"Acceso DetectOne. Clave un solo uso: {user.token[-8:]}"
        try:
            result = nogas_client.send_basic_text_message(user.user.phone, sms_msj)
            logging.debug(f"Respuesta del servicio NOGAS: {result}")
 
            if not result:
                return False
            return result
        except Exception as e:
            status_token = status.HTTP_406_NOT_ACCEPTABLE
            print(f"Error en la petición: {e}")
            raise Exception(e)
        finally:
            return status_token


class CustomPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def make_token(self, user):
        token = get_random_string(length=8)
        return super().make_token(user) + '|' + token


class RecoverPass(APIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        from django.core.mail import send_mail

        email = self.request.POST['email']

        token = None
        status_token = None
        message = ''

        try:
            user = User.objects.get(email=email)

            token, status_token = self.recoverPasswordEmail(self.request, user)
            message = 'Check your inbox and follow the instructions to recover the password.'

        except Exception as e:
            status_token = status.HTTP_201_CREATED
            message = 'Something went wrong'

        finally:
            return Response({'message': message}, status=status_token, headers={})

    def recoverPasswordEmail(self, request, user):
        from django.core.mail import send_mail
        from django.urls import reverse

        token = None
        status_token = None

        try:
            prg = PasswordResetTokenGenerator()
            token = prg.make_token(user)

            if token:
                status_token = status.HTTP_201_CREATED

                msg_plain = render_to_string('recover_password.txt', {'app_name': settings.APP_NAME, 'user': user.username, 'url': settings.URL_BASE + '/#/generate_password/' + user.email + '/'+token+'/'})
                msg_html = render_to_string('recover_password.html', {'app_name': settings.APP_NAME, 'user': user.username, 'url': settings.URL_BASE + '/#/generate_password/' + user.email + '/'+token+'/'})

                msg = EmailMessage(settings.APP_NAME + ' password recovery', msg_html, settings.EMAIL_HOST_USER, [user.email])
                msg.content_subtype = "html"  
                msg.send()

            else:
                # raise AuthenticationFailed("The Token is expired")
                status_token = status.HTTP_406_NOT_ACCEPTABLE
        except Exception as e:
            raise Exception("Error")
        finally:
            return token, status_token


class Validate2FA(ObtainAuthToken, APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        token = self.request.data['token']

        if len(token.replace(" ", ""))<8:
            status_token = status.HTTP_201_CREATED
            message = 'Something went wrong'
            return Response({'message': message}, status=status_token, headers={})

        status_token = None
        message = ''
        try:
            serializer = self.serializer_class(
                data=request.data,
                context={'request': request}
            )

            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']

            token_access = UserAccessToken.objects.get(user=user, token__contains=token)

            validator = PasswordResetTokenGenerator()

            if (validator.check_token(user, token_access.token)):
                token, create = Token.objects.update_or_create(user=user)

                from django.contrib.auth.models import update_last_login
                update_last_login(None, user)

                userSerializer = UserLoginSerializer(user, many=False)

                token_access.delete()

                return Response({
                    'token': token.key,
                    'user': userSerializer.data,
                })
            else:
                status_token = status.HTTP_201_CREATED
                message = 'something_wrong'
                return Response({'message': message}, status=status_token, headers={})

        except Exception as e:
            status_token = status.HTTP_201_CREATED
            message = 'something_wrong'
            return Response({'message': message}, status=status_token, headers={})

        # finally:
        #     return Response({'message': message}, status=status_token, headers={})


class GeneratePass(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        
        status_generation = None

        token = self.request.POST['token']
        email = self.request.POST['email']
        password = self.request.POST['password']

        message = ''

        try:
            user = User.objects.get(email=email)
            validator = PasswordResetTokenGenerator()
            if (validator.check_token(user, token)):
                user.set_password(password)
                user.save()
                status_generation = status.HTTP_201_CREATED
                message = 'Password updated! Go to Login and register.'
            else:
                status_generation = status.HTTP_406_NOT_ACCEPTABLE
                message = "Token expired. Please run 'Forgot password' process again."

        except ObjectDoesNotExist:
            status_generation = status.HTTP_406_NOT_ACCEPTABLE
            message = "Error."
        finally:
            return Response({'message': message}, status=status_generation, headers={})
