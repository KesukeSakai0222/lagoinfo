from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:season_year>/<str:season_name>/', views.AnimeListView.as_view(), name='animeList'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('form/', views.FormView.as_view(), name='form'),
    path('login/', views.login, name='login'),
    path('auth/', views.authorize, name='authorize'),
    path('updateImage/', views.UpdateImageHubView, name='updateImageHub'),
    path('updateImage/<int:season_year>/<str:season_name>', views.UpdateImageView.as_view(), name='updateImage'),
]

