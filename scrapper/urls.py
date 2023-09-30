from django.urls import path
from . import views

urlpatterns = [
    #path('', views.scrap, name='scrap'),
    path('', views.landing, name='landing'),
    #path('peliculas/', views.peliculas, name='peliculas'),
    #path('series/', views.series, name='series'),
    path('<str:tipo>/', views.tipo_view, name='tipo_view'),
    path('<str:tipo>/<str:stream>/', views.stream_view, name='stream_view'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),

]
