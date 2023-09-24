from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.forms import CustomAuthenticationForm
from users.views import CountryCreateView, CountryListView, CountryUpdateView, CountryDetailView, CountryDeleteView, \
    RegisterView, ProfileView, Verification, generate_new_password

from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(form_class=CustomAuthenticationForm, template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('<int:pk>/verification/<int:v_cod>/', Verification.as_view(), name='verification'),
    path('profile/genpassword/', generate_new_password, name='genpassword'),
    path('country/create/', CountryCreateView.as_view(), name='country-create'),
    path('country/<int:pk>/update/', CountryUpdateView.as_view(), name='country-update'),
    path('country/<int:pk>/delete/', CountryDeleteView.as_view(), name='country-delete'),
    path('country/list/', CountryListView.as_view(), name='country-list'),
    path('country/<int:pk>/', CountryDetailView.as_view(), name='country-detail'),
]
