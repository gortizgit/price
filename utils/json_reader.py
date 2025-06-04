import json
import os

def load_json(relative_path):
    # Obtiene el directorio absoluto del archivo actual (utils/)
    project_root = os.path.dirname(os.path.abspath(__file__))

    # Sube un nivel en la jerarquía de carpetas (a la raíz del proyecto: price/)
    project_root = os.path.abspath(os.path.join(project_root, ".."))

    # Construye la ruta absoluta al archivo JSON usando el separador del sistema operativo
    full_path = os.path.join(project_root, relative_path.replace("/", os.sep))

    # Verifica si el archivo existe, si no lanza un error
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"No se encontró el archivo JSON en: {full_path}")

    # Abre el archivo y lo carga como diccionario (o lista, dependiendo del contenido)
    with open(full_path, encoding='utf-8') as f:
        return json.load(f)
