from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:season_year>/<str:season_name>/', views.AnimeListView.as_view(), name='animeList'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('form/', views.FormView.as_view(), name='form'),
    path('malLogin/', views.MalLogin.as_view(), name='malLogin'),
    path('auth/', views.Authorize.as_view(), name='authorize'),
    path('updateImage/', views.UpdateImageView.as_view(), name='updateImageHub'),
    path('updateImage/<int:season_year>/<str:season_name>', views.UpdateImageView.as_view(), name='updateImage'),
]
