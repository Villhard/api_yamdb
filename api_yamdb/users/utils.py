from django.core.mail import EmailMessage

from api_yamdb.settings import EMAIL_HOST_USER


def send_mail(user, code):
    """
    Отправка письма с кодом подтверждения.
    """
    email = EmailMessage(
        'Код для подтверждения',
        f'{user.username}, Ваш код для входа\n{code}',
        EMAIL_HOST_USER,
        [user.email],
    )
    email.send()
