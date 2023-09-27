# email_sender


### Проект по управлению рассылками пользователей


Данное ПО позволяет развернуть сервер для почтовых рассылок.


+ Внимание, перед добавлением пользователя добавьте как минимум одну страну!
+ Для добавления суперпользователя - manage.py csu
+ При DEBUG = False необходимо папку статики обрабатывать средствами вэб-сервера
+ При работе по https возможны проблемы с csrf. В этом случае необходимо установить CSRF_TRUSTED_ORIGINS 
+ Некоторые настройки проекта расположены в .env файле в корне проекта. 



### Пример файла .env

CACHE_ENABLE = True
LOCATION = redis://127.0.0.1:6379

DEBUG = True

EMAIL_HOST = mail.nic.ru
EMAIL_PORT = 25
EMAIL_HOST_USER = admin@v-petrenko.ru
EMAIL_HOST_PASSWORD = M342R_crb

DB_HOST = localhost
DB_USER = postgres
DB_PASS = 123
DB_NAME = project4

SU_MAIL = admin@example.ru
SU_PASS = admin12345
