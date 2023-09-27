from django.contrib import admin

from mailing.models import Client, Mailing, Feedback, ClientSet, LogSending


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'fio', 'email',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subject', 'message',)
    list_filter = ('status',)
    search_fields = ('name', 'subject',)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'message',)


@admin.register(ClientSet)
class ClientSetAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'client',)


@admin.register(LogSending)
class LogSendingAdmin(admin.ModelAdmin):
    list_display = ('mailing', 'date_time', 'status_post', 'server_request',)
