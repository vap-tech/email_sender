from django.db import models, transaction
from config.settings import AUTH_USER_MODEL as AU_MODEL


NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    email = models.EmailField(verbose_name='email', unique=True)
    fio = models.CharField(max_length=200, verbose_name='ФИО')
    comment = models.TextField(max_length=200, verbose_name='комментарий', **NULLABLE)

    creator = models.ForeignKey(AU_MODEL, on_delete=models.CASCADE, verbose_name='создатель', **NULLABLE)

    def __str__(self):
        return f'{self.fio}: {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('email', 'fio',)


class Mailing(models.Model):
    INTERVAL_CHOICES = [
        ('D', 'раз в день'),
        ('W', 'раз в неделю'),
        ('M', 'раз в месяц'),
    ]
    STATUS_CHOICES = [
        (1, 'включена'),
        (0, 'отключена'),
    ]

    name = models.CharField(max_length=100, verbose_name='наименование')
    subject = models.CharField(max_length=200, verbose_name='Тема')
    message = models.TextField(verbose_name='Сообщение')

    created_date = models.DateTimeField(verbose_name='дата создания')
    end_date = models.DateTimeField(verbose_name='дата окончания')
    intervals = models.CharField(max_length=1, verbose_name='Периодичность', choices=INTERVAL_CHOICES, default='D')
    status = models.PositiveSmallIntegerField(verbose_name='Статус', choices=STATUS_CHOICES, default=1)

    creator = models.ForeignKey(AU_MODEL, on_delete=models.CASCADE, verbose_name='создатель', **NULLABLE)

    def __str__(self):
        return f'{self.name} {self.subject}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ('name',)


class ClientSet(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='рассылка')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='адресат')

    def save(self, *args, **kwargs):
        with transaction.atomic():
            ClientSet.objects.filter(mailing=self.mailing, client=self.client).delete()
        return super(ClientSet, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.mailing} для {self.client}'

    class Meta:
        verbose_name = 'Установленный адресат'
        verbose_name_plural = 'Установленные адресаты'
        ordering = ('mailing',)


class LogSending(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='адресат')
    date_time = models.DateTimeField(verbose_name='Последняя попытка')
    status_post = models.CharField(verbose_name='Статус')
    server_request = models.CharField(verbose_name='Ответ сервера')

    creator = models.ForeignKey(AU_MODEL, on_delete=models.CASCADE, verbose_name='создатель', **NULLABLE)

    def __str__(self):
        return f'{self.mailing}: {self.status_post}'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
        ordering = ('mailing',)


class Feedback(models.Model):
    name = models.CharField(max_length=150, verbose_name='Имя')
    phone = models.CharField(max_length=25, verbose_name='Телефон')
    email = models.CharField(max_length=100, verbose_name='Почта')
    message = models.TextField(verbose_name='Сообщение')

    def __str__(self):
        return f'{self.name}: {self.message[:30]}'

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратные связи'
        ordering = ('email',)


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    slug = models.CharField(max_length=200, verbose_name='ЧПУ')
    content = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(upload_to='blogs/', verbose_name='превью', **NULLABLE)
    created_date = models.DateTimeField(verbose_name='дата создания', **NULLABLE)
    is_public = models.BooleanField(default=True, verbose_name='опубликовано или нет')
    views_count = models.IntegerField(default=0, verbose_name='количество просмотров')

    creator = models.ForeignKey(AU_MODEL, on_delete=models.CASCADE, verbose_name='создатель', **NULLABLE)

    def __str__(self):
        return f'{self.title} {self.content[:50]}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
