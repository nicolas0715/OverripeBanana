from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as login1
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash

from django.db import connection

from scrapper.models import *
from scrapper.forms import *

from bs4 import BeautifulSoup
import requests

# Create your views here.

# Tipo de contenido
pelicula = "movies_at_home"
serie = "tv_series_browse"

# Tipos de streamming
netflix = "netflix"
amazon_prime = "amazon_prime"
disney_plus = "disney_plus"
max_us = "max_us"
paramount_plus = "paramount_plus"
apple_tv_us = "apple_tv_us"




def conectar_db():
    try:
        # Conectarse a la base de datos
        connection.connect()
        # Realizar operaciones con la base de datos aquí
    except Exception as e:
        # Manejar cualquier error de conexión
        print("Error al conectar a la base de datos:", e)


def landing(request):
    scraping(request)
    return render(request, 'landing_page.html')

@login_required
def home(request):
    usuario = request.user
    contexto = {'usuario': usuario, 'peliculas': scrap(request, 'https://www.rottentomatoes.com/browse/movies_at_home/?page=5', 'pelicula'), 'series': scrap(request, 'https://www.rottentomatoes.com/browse/tv_series_browse/?page=5', 'serie')}
    return render(request, 'home.html', {'contexto': contexto})

@login_required
def tipo_view(request, tipo):
    if tipo == 'pelicula':
        return render(request, 'peliculas.html', scrap(request, 'https://www.rottentomatoes.com/browse/movies_at_home/?page=5', 'pelicula'))
    elif tipo == 'serie':
        return render(request, 'series.html', scrap(request, 'https://www.rottentomatoes.com/browse/tv_series_browse/?page=5', 'serie'))
    else:
        return HttpResponse("Tipo no válido", status=400)

@login_required
def stream_view(request, tipo, stream):
    if tipo == 'pelicula':
        return render(request, 'peliculas.html', scrap(f"https://www.rottentomatoes.com/browse/movies_at_home/affiliates:{str(stream)}?page=5", 'pelicula'))
    elif tipo == 'serie':
        return render(request, 'series.html', scrap(f"https://www.rottentomatoes.com/browse/tv_series_browse/affiliates:{str(stream)}?page=5", 'serie'))

def scrap(request, url, tipo):
    usuario = request.user
    response = requests.get(url)
    html_content = response.content

    soup = BeautifulSoup(html_content, "html.parser")
    
    #divs = soup.find_all('div', class_='js-tile-link')
    #links = soup.find_all('a', class_='js-tile-link')
    elementos = soup.select('div.js-tile-link, a.js-tile-link')
    
    datos_peliculas = []
    datos_series = []
    
    if tipo == 'pelicula':
        for elemento in elementos:
            # Extrae los datos que necesitas de cada etiqueta
            nombre_pelicula = elemento.find('span', class_='p--small').get_text(strip=True)
            fecha_streaming_tag = elemento.find('span', class_='smaller')
            if fecha_streaming_tag:
                fecha_streaming = fecha_streaming_tag.get_text(strip=True)
            else:
                # Si no se encuentra, asigna un valor por defecto
                fecha_streaming = '-'
            imagen = elemento.find('img')['src']
            criticsscore_tag = elemento.find('score-pairs-deprecated')
            if criticsscore_tag and criticsscore_tag.get('criticsscore') != '':
                criticsscore = criticsscore_tag.get('criticsscore')
            else:
                criticsscore = '-'
                
            audiencescore_tag = elemento.find('score-pairs-deprecated')
            if audiencescore_tag and audiencescore_tag.get('audiencescore') != '':
                audiencescore = audiencescore_tag.get('audiencescore')
            else:
                audiencescore = '-'

            pelicula = {
                'Nombre_pelicula': nombre_pelicula,
                'Fecha_streaming': fecha_streaming,
                'Imagen': imagen,
                'Criticsscore': criticsscore,
                'Audiencescore': audiencescore
            }

            # Agrega el diccionario a la lista de datos de películas
            datos_peliculas.append(pelicula)
        return {'usuario': usuario, 'peliculas': datos_peliculas}
        
    elif tipo == 'serie':
        for elemento in elementos:
            # Extrae los datos que necesitas de cada etiqueta
            nombre_serie = elemento.find('span', class_='p--small').get_text(strip=True)
            fecha_streaming_tag = elemento.find('span', class_='smaller')
            if fecha_streaming_tag:
                fecha_streaming = fecha_streaming_tag.get_text(strip=True)
            else:
                # Si no se encuentra, asigna un valor por defecto
                fecha_streaming = '-'
            imagen = elemento.find('img')['src']
            criticsscore_tag = elemento.find('score-pairs-deprecated')
            if criticsscore_tag:
                criticsscore = criticsscore_tag.get('criticsscore')
            else:
                criticsscore = '-'
            audiencescore_tag = elemento.find('score-pairs-deprecated')
            if criticsscore_tag:
                audiencescore = audiencescore_tag.get('audiencescore')
            else:
                audiencescore = '-'

            serie = {
                'Nombre_serie': nombre_serie,
                'Fecha_streaming': fecha_streaming,
                'Imagen': imagen,
                'Criticsscore': criticsscore,
                'Audiencescore': audiencescore
            }

            # Agrega el diccionario a la lista de datos de películas
            datos_series.append(serie)
        return {'usuario': usuario, 'series': datos_series}
    
#==========================Nuevo========================

from scrapper.models import Pelicula, Serie
from datetime import datetime

def scraping(request):
    # Obtener el usuario logueado
    usuario = request.user
    
    # Urls para scrapear
    urls = ['https://www.rottentomatoes.com/browse/movies_at_home/?page=5',
            'https://www.rottentomatoes.com/browse/tv_series_browse/?page=5']
    
    datos_peliculas = []
    datos_series = []
    
    for url in urls:
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, "html.parser")
        elementos = soup.select('div.js-tile-link, a.js-tile-link')

        if url == urls[0]:
            for elemento in elementos:
            # Extrae los datos que necesitas de cada etiqueta
                nombre_pelicula = elemento.find('span', class_='p--small').get_text(strip=True)
                fecha_streaming_tag = elemento.find('span', class_='smaller')
                if fecha_streaming_tag:
                    fecha_streaming_no_format = fecha_streaming_tag.get_text(strip=True)[10:]
                    fecha_streaming_format = datetime.strptime(fecha_streaming_no_format, "%b %d, %Y")
                    fecha_streaming = fecha_streaming_format.strftime("%Y-%m-%d")
                else:
                    # Si no se encuentra, asigna un valor por defecto
                    fecha_streaming = None
                imagen = elemento.find('img')['src']
                criticsscore_tag = elemento.find('score-pairs-deprecated')
                if criticsscore_tag and criticsscore_tag.get('criticsscore') != '':
                    criticsscore = criticsscore_tag.get('criticsscore')
                else:
                    criticsscore = 0
                    
                audiencescore_tag = elemento.find('score-pairs-deprecated')
                if audiencescore_tag and audiencescore_tag.get('audiencescore') != '':
                    audiencescore = audiencescore_tag.get('audiencescore')
                else:
                    audiencescore = 0

                pelicula = {
                    'nombre_pelicula': nombre_pelicula,
                    'fecha_streaming': fecha_streaming,
                    'imagen': imagen,
                    'critics_score': criticsscore,
                    'audience_score': audiencescore
                }

                # Agregar las pelis a la base de datos
                nueva_peli = Pelicula(
                    nombre_pelicula = pelicula['nombre_pelicula'],
                    fecha_streaming = pelicula['fecha_streaming'],
                    imagen = pelicula['imagen'],
                    critics_score = pelicula['critics_score'],
                    audience_score = pelicula['audience_score'],
                    user_score = 0,
                    streaming = ' ',
                )
                
                nombre_pelicula = pelicula['nombre_pelicula']
                pelicula_existente = Pelicula.objects.filter(nombre_pelicula=nombre_pelicula).first()

                if pelicula_existente is None:
                    # La película no existe en la base de datos, por lo que puedes guardarla
                    nueva_peli.save()
                else:
                    # La película ya existe en la base de datos, no necesitas guardarla nuevamente
                    print(f'La película "{nombre_pelicula}" ya existe en la base de datos.')

                # Agrega el diccionario a la lista de datos de películas
                datos_peliculas.append(pelicula)
        
        elif url == urls[1]:
            for elemento in elementos:
            # Extrae los datos que necesitas de cada etiqueta
                nombre_serie = elemento.find('span', class_='p--small').get_text(strip=True)
                ultimo_capitulo_tag = elemento.find('span', class_='smaller')
                if ultimo_capitulo_tag:
                    ultimo_capitulo_no_format = ultimo_capitulo_tag.get_text(strip=True)[16:]
                    ultimo_capitulo_format = datetime.strptime(ultimo_capitulo_no_format, '%b %d')
                    ultimo_capitulo_format = ultimo_capitulo_format.replace(year=datetime.now().year)
                    ultimo_capitulo = ultimo_capitulo_format.strftime("%Y-%m-%d")
                else:
                    # Si no se encuentra, asigna un valor por defecto
                    ultimo_capitulo = None
                imagen = elemento.find('img')['src']
                criticsscore_tag = elemento.find('score-pairs-deprecated')
                if criticsscore_tag and criticsscore_tag.get('criticsscore') != '':
                    criticsscore = criticsscore_tag.get('criticsscore')
                else:
                    criticsscore = 0
                audiencescore_tag = elemento.find('score-pairs-deprecated')
                if audiencescore_tag and audiencescore_tag.get('audiencescore') != '':
                    audiencescore = audiencescore_tag.get('audiencescore')
                else:
                    audiencescore = 0

                serie = {
                    'nombre_serie': nombre_serie,
                    'ultimo_capitulo': ultimo_capitulo,
                    'imagen': imagen,
                    'criticsscore': criticsscore,
                    'audiencescore': audiencescore
                }
                
                # Agregar las series a la base de datos
                nueva_serie = Serie(
                    nombre_serie = serie['nombre_serie'], 
                    ultimo_capitulo = serie['ultimo_capitulo'],
                    imagen = serie['imagen'],
                    critics_score = serie['criticsscore'],
                    audience_score = serie['audiencescore'],
                    user_score = 0,
                    streaming = ' ',
                )
                
                nombre_serie = serie['nombre_serie']
                serie_existente = Serie.objects.filter(nombre_serie=nombre_serie).first()

                if serie_existente is None:
                    # La película no existe en la base de datos, por lo que puedes guardarla
                    nueva_serie.save()
                else:
                    # La película ya existe en la base de datos, no necesitas guardarla nuevamente
                    print(f'La serie "{nombre_serie}" ya existe en la base de datos.')

                # Agrega el diccionario a la lista de datos de películas
                datos_series.append(serie)
    return {'usuario': usuario, 'peliculas': datos_peliculas, 'series': datos_series}

def login(request):

    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST)

        if form.is_valid():
            user = form.cleaned_data.get("username")
            pdw = form.cleaned_data.get("password")
            
            user = authenticate(username = user, password = pdw)

            if user is not None:
                login1(request, user)
                avatar = Avatar.objects.filter(user = request.user.id)
                try:
                    avatar = avatar[0].image.url
                except:
                    avatar = None
                
                usuario = request.user
                
                contexto = {'usuario': usuario, 'peliculas': scrap(request, 'https://www.rottentomatoes.com/browse/movies_in_theaters/', 'pelicula'), 'series': scrap(request, 'https://www.rottentomatoes.com/browse/tv_series_browse/', 'serie')}
                
                print('Todo OK')
                return render(request, "home.html", {'contexto': contexto})
            else:
                return render(request, "login.html", {"form": form})
        else:
            return render(request, "login.html", {"form": form})
    form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def signup(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            print('form valid')
#           username = form.cleaned_data["username"]
            form.save()
            avatar = Avatar.objects.filter(user = request.user.id)
            try:
                avatar = avatar[0].image.url
            except:
                avatar = None
            return render(request, "home.html", {"avatar": avatar})
        print(form.errors)
    form = UserRegisterForm()
    return render(request, "signup.html", {"form": form})

def propio_logout(request):
    logout(request)
    return landing(request)






def perfil(request):
    usuario = request.user
    contexto = {'usuario': usuario}
    return render(request, 'perfil.html', {'contexto': contexto})

def editar_perfil(request):
    usuario = request.user
    user_basic_info = User.objects.get(id = usuario.id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance = usuario)
        if form.is_valid():
            user_basic_info.username = form.cleaned_data.get('username')
            user_basic_info.email = form.cleaned_data.get('email')
            user_basic_info.first_name = form.cleaned_data.get('first_name')
            user_basic_info.last_name = form.cleaned_data.get('last_name')
            user_basic_info.save()
            return render(request, 'perfil.html')
        else:
            return render(request, 'editar_perfil.html', {'form': form})
    else:
        form = UserEditForm(initial = {'email' : usuario.email, 
                                        'username': usuario.username, 
                                        'first_name': usuario.first_name, 
                                        'last_name': usuario.last_name
                                        })
        contexto = {'form': form, 'usuario': usuario}
        return render(request, 'editar_perfil.html', {'contexto': contexto})

def cambiar_contrasena(request):
    usuario = request.user
    if request.method == "POST":
        form = ChangePasswordForm(data = request.POST, user = request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            avatar = Avatar.objects.filter(user = request.user.id)
            try:
                avatar = avatar[0].image.url
            except:
                avatar = None
            return render(request, "perfil.html", {"avatar": avatar})
    else:
        form = ChangePasswordForm(user = request.user)
        contexto = {'usuario': usuario, 'form': form}
    return render(request, "cambiar_contrasena.html", {"contexto": contexto}) 