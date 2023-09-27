from django.conf import settings
from django.core.cache import cache
from datetime import datetime
from django.core.mail import send_mail

from mailing.models import Mailing, LogSending, Blog


def get_mailing():
    """
    Получает рассылки для отправки
    :return: Queryset рассылок
    """
    current_datetime = datetime.now()
    data = Mailing.objects.filter(created_date__lt=current_datetime, end_date__gt=current_datetime)
    return data


def get_client_set(mailings):
    """
    Получает адреса клиентов для рассылки
    :param mailings: Queryset рассылок
    :return: список Queryset'ов из ClientSet
    """
    client_set = []
    if mailings:
        for mailing in mailings:
            client_set.append(mailing.clientset_set.all())

    return client_set


def send_mailing(client_sets):
    for client_set in client_sets:
        for item in client_set:

            result = send_mail(
                item.mailing.subject,
                item.mailing.message,
                'admin@v-petrenko.ru',
                [item.client.email],
                fail_silently=False,
            )

            server_request = '200'

            LogSending.objects.filter(mailing=item.mailing, client=item.client).delete()

            log = LogSending.objects.create(
                mailing=item.mailing,
                client=item.client,
                date_time=datetime.now(),
                status_post=result,
                server_request=server_request,
                creator=item.mailing.creator)
            log.save()


def send_all():
    mailing = get_mailing()
    set_client = get_client_set(mailing)
    send_mailing(set_client)


def get_blog():
    if settings.CACHE_ENABLE:
        return cache.get_or_set('blog_list', Blog.objects.all())
    else:
        return Blog.objects.all()
