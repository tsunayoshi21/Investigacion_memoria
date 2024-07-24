"""
Autor: Cristobal Vasquez
Fecha: 24-07-2024
Este script realiza scraping de la página web de Memoria Chilena (https://www.memoriachilena.gob.cl/602/) para obtener información de imágenes y guardarla en un archivo JSON.
Además, guarda las imágenes de los libros en una carpeta llamada "images_scrapped".
Es llegar y correr si se verifican las rutas previamente.
Se escogen las valid_keys según la estructura de clasificación de la página web.
Las palabras clave y años de interés se definen en según interés en la epoca estudiada.
Los rangos de interés fueron obtenidos empíricamente, siendo esos rangos los que tienen información de interés (cumple con el año y las palabras relevantes).

Considerar que pueden haber fallas en los filtros y que pueden haber fotos no recopiladas. Podrían haber otras formas de filtrar la información.


"""


import requests
from bs4 import BeautifulSoup
import os
import json
from itertools import chain


# Función para dividir una cadena en partes de longitud fija
def split_fixed_length(value, length=4):
    return [value[i:i+length] for i in range(0, len(value), length)]

# Función para separar el valor de "Materias" por '-' y ','
def split_materias(value):
    return [item.strip() for item in value.replace('-', ',').split(',')]

base_url = "https://www.memoriachilena.gob.cl/602/"
# Lista de posibles claves válidas

valid_keys = [
    'Autor', 'Propiedad intelectual', 'Tipo', 'Descripción física', 
    'Datos de publicación', 'Notas', 'Año', 'Idioma', 'Colección', 
    'Códigos BN', 'Materias', 'Temas relacionados'
]

años_validos = range(1970, 1990)
palabras_clave = ["dictadura", "pinochet", "golpe", "1973", "augusto", "allende"]
json_data = {}

# Definir los rangos de interés
rangos_interes = [range(10000, 10445), range(31761, 31807), range(41749, 41847), 
                  range(43926, 43927), range(46863, 46890), range(49423, 49440), 
                  range(54069, 54109), range(54239, 54307), range(54564, 54804), 
                  range(55133, 55208), range(55559, 55656), range(55827, 55922), 
                  range(56129, 56152), range(56317, 56418), range(56919, 57009), 
                  range(57276, 57277), range(57611, 57632), range(58618, 58768), 
                  range(58951, 58953), range(59068, 59096), range(59356, 59367), 
                  range(59497, 59618), range(59758, 59814), range(60014, 60118), 
                  range(60315, 60337), range(60480, 60484), range(60701, 60756), 
                  range(61014, 61119), range(61757, 62246), range(62474, 62490), 
                  range(62697, 62926), range(63056, 63589), range(63755, 63756), 
                  range(63962, 64085), range(64242, 64287), range(64438, 64460), 
                  range(64789, 65221), range(65325, 65342), range(65511, 65519), 
                  range(65821, 65835), range(66147, 66413), range(67278, 67295), 
                  range(67409, 67410), range(67544, 67849), range(68220, 68514), 
                  range(68907, 70080), range(70196, 70258), range(70369, 70376), 
                  range(70576, 70577), range(70688, 70727), range(71009, 71088), 
                  range(71244, 71645), range(71905, 71992), range(72120, 73344), 
                  range(73597, 73649), range(73824, 73835), range(73952, 73954), 
                  range(74078, 74408), range(74744, 75622), range(75856, 75857), 
                  range(75979, 76361), range(76515, 77054), range(77227, 77454), 
                  range(77623, 78245), range(78359, 78858), range(78963, 82466), 
                  range(82584, 83545), range(83674, 84141), range(84448, 84462), 
                  range(84609, 84720), range(84824, 85126), range(85329, 85605), 
                  range(85708, 85848), range(85997, 86309), range(86484, 86579), 
                  range(86859, 87408), range(98254, 99740), range(99852, 99853), 
                  range(99992, 99993)]



for i in chain(*rangos_interes):

    url = "https://www.memoriachilena.gob.cl/602/w3-article-{:05d}.html".format(i)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #encontrar div con clase "ar_clasificaciones"
    clasifications = soup.find_all('div', class_='ar_clasificaciones')

    #clasifications = False
    if clasifications:
        print("Scraping: ", url)

        # Creemos un diccionario para almacenar la información
        info_dict = {}

        # Iteramos sobre los elementos encontrados
        for clasification in clasifications:
            # Buscamos los recuadros con información
            recuadros = clasification.find_all('div', class_='recuadro')

            for recuadro in recuadros:
                # Extraemos las etiquetas p
                p_tags = recuadro.find_all('p')

                for p in p_tags:
                    text = p.get_text(strip=True)
                    # Separar la clave y el valor solo si la clave es válida
                    if ':' in text:
                        key_val = text.split(':', 1)
                        key, val = key_val[0].strip(), key_val[1].strip()
                        
                        if key in valid_keys:
                            if key == 'Año':
                                if len(val) > 4:
                                    val = split_fixed_length(val)
                                else:
                                    val = [int(val)]
                            elif key == 'Materias':
                                val = split_materias(val)
                            if key in info_dict:
                                if isinstance(info_dict[key], list):
                                    info_dict[key].append(val)
                                else:
                                    info_dict[key] += f'; {val}'
                            else:
                                info_dict[key] = val

                # Buscamos otros elementos clave-valor que no siguen la estructura p:span
                spans = recuadro.find_all('div', class_='pn-xattr')
                for span in spans:
                    text = span.get_text(strip=True)
                    if ':' in text:
                        key_val = text.split(':', 1)
                        key, val = key_val[0].strip(), key_val[1].strip()
                        
                        if key in valid_keys:
                            if key == 'Año' and len(val) > 4:
                                val = split_fixed_length(val)
                            elif key == 'Materias':
                                val = split_materias(val)
                            if key in info_dict:
                                if isinstance(info_dict[key], list):
                                    info_dict[key].append(val)
                                else:
                                    info_dict[key] += f'; {val}'
                            else:
                                info_dict[key] = val

            # Extraemos temas relacionados si están presentes
            temas_relacionados_div = clasification.find(id='clasificacion_04')
            if temas_relacionados_div:
                temas = temas_relacionados_div.find_all('p', class_='titulo')
                temas_relacionados = [tema.get_text(strip=True) for tema in temas]
                if temas_relacionados:
                    info_dict['Temas relacionados'] = '; '.join(temas_relacionados)

        try:
            # Extraemos la imagen   
            img = soup.find_all('div', class_='articulocompleto articuloUI_recursos')
            img = img[0].find_all('img')
            src = img[0]['src']
            alt = img[0]['alt']
            info_dict['src'] =  base_url + src
            info_dict['alt'] = alt


            titulo = soup.find_all('h1', class_="titulo")
            titulo = titulo[0].get_text(strip=True)
            info_dict['titulo'] = titulo

            try:
                datos = soup.find_all('div', class_='datos')
                fuente = datos[0].find_all('p')
                fuente = fuente[0].get_text(strip=True)
                info_dict['Fuente'] = fuente
            except:
                print("No se encontró la fuente")
                info_dict['Fuente'] = None
            
            # Guardamos la imagen
            interested = False
            try:
                for palabra in palabras_clave:
                    if palabra in "".join(info_dict['Materias']).lower():
                        interested = True
                        break
            except:
                print("No se encontraron materias")

            for año in info_dict['Año']:
                if año in años_validos:
                    interested = True
                    break
            if interested:
                print("Es de interés")
                image_data = requests.get(info_dict['src']).content
                with open(f'images_scrapped/imagen_{i:05d}.jpg', 'wb') as handler:
                    handler.write(image_data)

                # Guardamos la información en un archivo JSON
                json_data[i] = info_dict
            else:
                print("No es de interés")
            #print(info_dict)
        except:
            print("No se encontró imagen")
            print("No se encontró información en: ", url)

    else:
        #print('No se encontró información de clasificaciones')
        print("No se encontró información de clasificaciones en: ", url)

# Guardamos la información en un archivo JSON
with open('info.json', 'w', encoding='utf-8') as file:
    json.dump(json_data, file, ensure_ascii=False, indent=4)
print("Fin del scraping")