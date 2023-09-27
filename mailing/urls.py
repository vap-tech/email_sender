from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.views import *
from mailing.apps import MailingConfig

app_name = MailingConfig.name

urlpatterns = [
    path('', cache_page(5)(IndexListView.as_view()), name='index'),

    path('mailing/all/', cache_page(10)(MailingListView.as_view()), name='mailing-all'),
    path('mailing/create/', MailingCreateView.as_view(), name='mailing-create'),
    path('mailing/<int:pk>/', MailingDetailView.as_view(), name='mailing-detail'),
    path('mailing/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing-delete'),
    path('mailing/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing-update'),


    path('client/all/', ClientListView.as_view(), name='client-list'),
    path('client/create/', ClientCreateView.as_view(), name='client-create'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('client/<int:pk>/delete/', ClientDeleteView.as_view(), name='client-delete'),
    path('client/<int:pk>/update/', ClientUpdateView.as_view(), name='client-update'),

    path('blog/all/', BlogListView.as_view(), name='blog-list'),
    path('blog/create/', BlogCreateView.as_view(), name='blog-create'),
    path('blog/<str:slug>/', BlogDetailView.as_view(), name='blog-detail'),
    path('blog/<str:slug>/delete/', BlogDeleteView.as_view(), name='blog-delete'),
    path('blog/<str:slug>/update/', BlogUpdateView.as_view(), name='blog-update'),

    path('messages/', FeedbackListView.as_view(), name='messages'),
    path('feedback-create/', FeedbackCreateView.as_view(), name='feedback-create'),

    path('log/all/', LogSendingListView.as_view(), name='log-all'),

]
