from django.shortcuts import render

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
    return render(request, 'landing_page.html')

def tipo_view(request, tipo):
    if tipo == 'pelicula':
        return render(request, 'peliculas.html', scrap('https://www.rottentomatoes.com/browse/movies_at_home/?page=5'))
    elif tipo == 'serie':
        return render(request, 'series.html', scrap('https://www.rottentomatoes.com/browse/tv_series_browse/?page=5'))

def stream_view(request, tipo, stream):
    if tipo == 'pelicula':
        return render(request, 'peliculas.html', scrap(f"https://www.rottentomatoes.com/browse/movies_at_home/affiliates:{str(stream)}?page=5"))
    elif tipo == 'serie':
        return render(request, 'series.html', scrap(f"https://www.rottentomatoes.com/browse/tv_series_browse/affiliates:{str(stream)}?page=5"))

def scrap(url):
    response = requests.get(url)
    html_content = response.content

    soup = BeautifulSoup(html_content, "html.parser")

    divs = soup.find_all('div', class_='js-tile-link')
    links = soup.find_all('a', class_='js-tile-link')

    datos_peliculas = []
    for div, link in zip(divs, links):
        # Extrae los datos que necesitas de cada etiqueta
        nombre_pelicula = div.find('span', class_='p--small').get_text(strip=True)
        fecha_streaming_tag = div.find('span', class_='smaller')
        if fecha_streaming_tag:
            fecha_streaming = fecha_streaming_tag.get_text(strip=True)
        else:
            # Si no se encuentra, asigna un valor por defecto
            fecha_streaming = '-'
        imagen = div.find('img')['src']
        criticsscore = div.find('score-pairs')['criticsscore']
        audiencescore = div.find('score-pairs')['audiencescore']

        pelicula = {
            'Nombre_pelicula': nombre_pelicula,
            'Fecha_streaming': fecha_streaming,
            'Imagen': imagen,
            'Criticsscore': criticsscore,
            'Audiencescore': audiencescore
        }

        # Agrega el diccionario a la lista de datos de películas
        datos_peliculas.append(pelicula)

        nombre_pelicula = link.find('span', class_='p--small').get_text(strip=True)
        fecha_streaming_tag = div.find('span', class_='smaller')
        if fecha_streaming_tag:
            fecha_streaming = fecha_streaming_tag.get_text(strip=True)
        else:
            # Si no se encuentra, asigna un valor por defecto
            fecha_streaming = '-'
        imagen = link.find('img')['src']
        criticsscore = link.find('score-pairs')['criticsscore']
        audiencescore = link.find('score-pairs')['audiencescore']

        pelicula = {
            'Nombre_pelicula': nombre_pelicula,
            'Fecha_streaming': fecha_streaming,
            'Imagen': imagen,
            'Criticsscore': criticsscore,
            'Audiencescore': audiencescore
        }
    
        # Agrega el diccionario a la lista de datos de películas
        datos_peliculas.append(pelicula)
    
    print(datos_peliculas)
    return ({'pelis': datos_peliculas})