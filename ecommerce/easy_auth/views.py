from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from easy_auth.backends import VdkDefaultEmail
from rest_framework.response import Response
from easy_auth.backends import create_pass
from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework import status
from easy_auth.models import User
from threading import Thread

# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def restricted(request, *args, **kwargs):
    return Response(data="Only for logged in User", status=status.HTTP_200_OK)


class RestorePassView(APIView):

    def post(self, request, *args, **kwargs):

        user = User.objects.filter(email=request.data['email']).first()
        if user:
            password = create_pass()
            user.set_password(password)
            user.save()
            text = 'Добрый день {}. Вам отправлен новый пароль для входа в личный кабинет: {}'.format(
                user.get_first_last_name(), password)
            mail = VdkDefaultEmail(text)
            Thread(target=mail.send_message, args=(user.email,)).start()
            return Response(data="Письмо с новым паролем выслано на почту {}".format(
                user.email), status=status.HTTP_200_OK)
        else:
            return Response(data="Такого пользователя нет в системе",
                            status=status.HTTP_404_NOT_FOUND)

class Password(APIView):

    '''
    this method allows to change password by user
    '''
    def post(self, request, *args, **kwargs):

        user = request.auth.user
        try:
            if request.data['newPass'] == request.data['newPassRe']:
                old_password_correct = user.check_password(request.data['oldPass'])
                if old_password_correct:
                    user.set_password(request.data['newPass'])
                    user.save()
                    return Response(data="Пароль успешно изменён!", status=status.HTTP_200_OK)
                else:
                    return Response(data="Старый пароль неверный!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(data="Пароли не совпадают!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            return Response(data="В ходе изменения пароля возникла ошибка!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

