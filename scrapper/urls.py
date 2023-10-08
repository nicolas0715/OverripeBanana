from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    #path('', views.scrap, name='scrap'),
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    #path('peliculas/', views.peliculas, name='peliculas'),
    #path('series/', views.series, name='series'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.propio_logout, name='logout'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('perfil/', views.perfil, name='perfil'),
    path('cambiar_contrasena/', views.cambiar_contrasena, name='cambiar_contrasena'),
    
    path('<str:tipo>/', views.tipo_view, name='tipo_view'),
    path('<str:tipo>/<str:stream>/', views.stream_view, name='stream_view'),

]
