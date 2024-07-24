"""
Autor: Cristobal Vasquez
Fecha: 24-07-2024
Este script filtra las imagenes ya scrapeadas con un criterio específico.
En este caso, se filtro por Materias que contengan palabras clave y por Tipo de imagen.
"""

import os
import shutil
import json

# Definir rutas y parámetros
ruta_carpeta_imagenes = 'images_scrapped'  # Cambia esto a la ruta de tu carpeta de imágenes
ruta_json_metadata = 'info.json'  # Cambia esto a la ruta de tu archivo JSON
ruta_carpeta_destino = 'imagenes_filtradas'  # Cambia esto a la ruta de la carpeta de destino
contenidos_relevantes = ["dictadura", "pinochet", "golpe", "1973", "augusto", "allende"]

# Crear la carpeta de destino si no existe
if not os.path.exists(ruta_carpeta_destino):
    os.makedirs(ruta_carpeta_destino)

# Leer el archivo JSON con la metadata
with open(ruta_json_metadata, 'r', encoding='utf-8') as file:
    metadata = json.load(file)

# Filtrar y copiar las imágenes
for imagen_id, info in metadata.items():
    if 'Materias' in info:
        if any(any(contenido_relevante.lower() in materia.lower() for contenido_relevante in contenidos_relevantes) for materia in info['Materias']) and info['Tipo'] == 'Fotografía':
            nombre_imagen = f"imagen_{int(imagen_id):05d}.jpg"  # Asumiendo que las imágenes son .jpg
            ruta_imagen = os.path.join(ruta_carpeta_imagenes, nombre_imagen)
            if os.path.exists(ruta_imagen):
                shutil.copy(ruta_imagen, ruta_carpeta_destino)
            else:
                print(f"La imagen {imagen_id} no se encontró en la carpeta de imágenes")
                print(f"Ruta de la imagen: {ruta_imagen}")
    else:
        print(f"La imagen {imagen_id} no tiene información de materia")
print("Proceso completado.")
