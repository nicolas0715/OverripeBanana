from bs4 import BeautifulSoup
import requests

from datetime import datetime


def scrap(url):
    response = requests.get(url)
    html_content = response.content

    soup = BeautifulSoup(html_content, "html.parser")
    
    #divs = soup.find_all('div', class_='js-tile-link')
    #links = soup.find_all('a', class_='js-tile-link')
    elementos = soup.select('div.js-tile-link, a.js-tile-link')
    listado = []
    for elemento in elementos:
        nombre = elemento.find('span', class_='p--small').get_text(strip=True)
        fecha = elemento.find('span', class_='smaller')
        if fecha:
            fecha = elemento.find('span', class_='smaller').get_text(strip=True)
            fecha = fecha[10:]
            fecha_objeto = datetime.strptime(fecha, "%b %d, %Y")
            fecha = fecha_objeto.strftime("%Y-%m-%d")
            
        imagen = elemento.find('img')['src']
        critic_score = elemento.find('score-pairs-deprecated').get('criticsscore')
        if critic_score == '':
            critic_score = ' '
        audience_score = elemento.find('score-pairs-deprecated').get('audiencescore')
        if audience_score == '':
            audience_score = ' '
            
        element = {'nombre': nombre,
                    'fecha': fecha,
                    'imagen': imagen,
                    'criticscore': critic_score,
                    'audienceScore': audience_score 
        }
        listado.append(element)
        print(nombre, fecha, imagen, critic_score, audience_score)
    
    print(listado)
    return listado

scrap('https://www.rottentomatoes.com/browse/movies_at_home/?page=5')
#scrap('https://www.rottentomatoes.com/browse/tv_series_browse/?page=5')


def ingreso_db():
    pass