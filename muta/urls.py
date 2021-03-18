from django.urls import path
from .decorators import ip_checker

from . import views

handler500 = views.my_customized_server_error

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:season_year>/<str:season_name>/', views.AnimeListView.as_view(), name='animeList'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('form/', views.FormView.as_view(), name='form'),
    path('allSeasons/', views.AllSeasons.as_view(), name='allSeasons'),
    path('malLogin/', ip_checker(views.MalLogin.as_view()), name='malLogin'),
    path('auth/', ip_checker(views.Authorize.as_view()), name='authorize'),
    path('updateImage/', ip_checker(views.UpdateImageView.as_view()), name='updateImageHub'),
    path('updateImage/<int:season_year>/<str:season_name>', ip_checker(views.UpdateImageView.as_view()), name='updateImage'),
]
