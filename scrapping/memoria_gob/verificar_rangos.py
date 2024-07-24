"""
Autor: Cristobal Vasquez
Fecha: 24-07-2024
Este script lee el json generado por el scraper_w3.py y verifica los rangos de las imagenes que se descargaron.
Esto se hizo para luego no tener que verificar el rango completo al scrappear.
"""

import json
from itertools import chain

# Definir ruta al archivo JSON
ruta_json_metadata = 'info.json'  # Cambia esto a la ruta de tu archivo JSON

# Leer el archivo JSON con la metadata
with open(ruta_json_metadata, 'r', encoding='utf-8') as file:
    metadata = json.load(file)

# Obtener y ordenar los IDs de las imágenes
ids_imagenes = sorted(int(imagen_id) for imagen_id in metadata.keys())

# Encontrar los rangos donde sí hay imágenes
rangos_con_imagenes = []
rango_inicio = ids_imagenes[0]

for i in range(1, len(ids_imagenes)):
    if ids_imagenes[i] - ids_imagenes[i - 1] > 100:
        rango_fin = ids_imagenes[i - 1]
        rangos_con_imagenes.append(range(rango_inicio, rango_fin + 1))
        rango_inicio = ids_imagenes[i]

# Añadir el último rango
rangos_con_imagenes.append(range(rango_inicio, ids_imagenes[-1] + 1))
print(rangos_con_imagenes)

# Mostrar los rangos con imágenes
for rango in rangos_con_imagenes:
    print(f"Rango con imágenes: {rango.start} - {rango.stop - 1}")

# Ejemplo de uso de los rangos en un bucle for
for i in chain(*rangos_con_imagenes):
    # Aquí puedes poner el código que deseas ejecutar para cada ID en los rangos
    print(i)

print("Proceso completado.")
