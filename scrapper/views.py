from django.shortcuts import render
from django.http import HttpResponse

from .forms import UserRegistrationForm

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

def landing(request):
    contexto = {'peliculas': scrap('https://www.rottentomatoes.com/browse/movies_in_theaters/', 'pelicula'), 'series': scrap('https://www.rottentomatoes.com/browse/tv_series_browse/', 'serie')}
    print(contexto)
    return render(request, 'landing_page.html', {'contexto': contexto})

'''
contexto = {
    'peliculas': pelicula = {
                        'Nombre_pelicula': nombre_pelicula,
                        'Fecha_streaming': fecha_streaming,
                        'Imagen': imagen,
                        'Criticsscore': criticsscore,
                        'Audiencescore': audiencescore
                        },
    'series': serie = {
                        'Nombre_serie': nombre_serie,
                        'Fecha_streaming': fecha_streaming,
                        'Imagen': valor_imagen,
                        'Criticsscore': criticsscore,
                        'Audiencescore': audiencescore
                        },
}
'''

def tipo_view(request, tipo):
    if tipo == 'pelicula':
        return render(request, 'peliculas.html', scrap('https://www.rottentomatoes.com/browse/movies_at_home/?page=5', 'pelicula'))
    elif tipo == 'serie':
        return render(request, 'series.html', scrap('https://www.rottentomatoes.com/browse/tv_series_browse/?page=5', 'serie'))
    else:
        # Manejar casos no válidos, por ejemplo, devolviendo un mensaje de error
        return HttpResponse("Tipo no válido: " + tipo, status=400)
    
def stream_view(request, tipo, stream):
    if tipo == 'pelicula':
        return render(request, 'peliculas.html', scrap(f"https://www.rottentomatoes.com/browse/movies_at_home/affiliates:{str(stream)}?page=5", 'pelicula'))
    elif tipo == 'serie':
        return render(request, 'series.html', scrap(f"https://www.rottentomatoes.com/browse/tv_series_browse/affiliates:{str(stream)}?page=5", 'serie'))

def scrap(url, tipo):
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
        return {'peliculas': datos_peliculas}
        
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
        return {'series': datos_series}


def login(request):
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return render(request, 'landing_page.html')
    else:
        form = UserRegistrationForm()
        return render(request, 'signup.html', {'form': form})