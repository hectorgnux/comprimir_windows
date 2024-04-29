import os
import subprocess
import glob
import configparser
import shutil

def leer_parametros(ruta_config):
    config = configparser.ConfigParser()
    config.read(ruta_config)
    parametros = {}
    for seccion in config.sections():
        for clave, valor in config.items(seccion):
            parametros[clave] = valor
    return parametros

def comprimir_archivos(directorio, extension, winrar_path, carpeta_destino):
    # Buscar archivos con la extensión especificada en el directorio
    archivos_extension = glob.glob(os.path.join(directorio, "*." + extension))
    if archivos_extension:
        # Encontrar el archivo más reciente
        archivo_mas_reciente = max(archivos_extension, key=os.path.getctime)
        
        print("El archivo más reciente es:", archivo_mas_reciente)
        
        # Comprimir los archivos excepto el más reciente
        for archivo in archivos_extension:
            if archivo != archivo_mas_reciente:
                nombre_archivo = os.path.basename(archivo)
                archivo_comprimido = os.path.join(carpeta_destino, nombre_archivo + ".rar")
                comando = [winrar_path, "a", "-ep1", archivo_comprimido, archivo]
                subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                # Verificar si el archivo comprimido existe
                if os.path.exists(archivo_comprimido):
                    print("Archivo comprimido creado:", archivo_comprimido)
                    # Eliminar el archivo original después de la compresión
                    os.remove(archivo)
                else:
                    print("Error al comprimir el archivo:", archivo)
    else:
        print("No se encontraron archivos con la extensión {} en el directorio especificado.".format(extension))

# Leer los parámetros del archivo de configuración
parametros = leer_parametros("parametros.cfg")

# Directorio donde se encuentran los archivos
directorio = parametros.get("directorio", "")
# Extensión de los archivos a comprimir
extension = parametros.get("extension", "")
# Ruta donde se encuentra WinRAR
winrar_path = parametros.get("rar", "")
# Carpeta donde se moverán los archivos comprimidos
carpeta_destino = parametros.get("mover", "")

# Comprimir los archivos
comprimir_archivos(directorio, extension, winrar_path, carpeta_destino)