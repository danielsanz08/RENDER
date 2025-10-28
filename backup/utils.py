import os
import json
from django.core import management
from django.conf import settings
from django.apps import apps
from django.db import transaction
from django.core import serializers
import subprocess
from datetime import datetime
def crear_backup():
    
    modelos = [
        'libreria.Transaccion',
        'libreria.Insumo',
        'libreria.Proveedor',
        'libreria.Producto',
        'libreria.Cliente',
        'libreria.CustomUser',
        'libreria.CustomUserManager',
        
        
    ]
    
    data = {}
    for model_name in modelos:
        modelo = apps.get_model(model_name)
        objetos = modelo.objects.all()
        data[model_name] = serializers.serialize('json', objetos)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    nombre_archivo = f'backup_{timestamp}.json'
    ruta_archivo = os.path.join(settings.MEDIA_ROOT, 'backups', nombre_archivo)
    os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
    
    with open(ruta_archivo, 'w') as f:
        json.dump(data, f)
    
    return nombre_archivo, ruta_archivo


def restaurar_backup_json(ruta_archivo):
    """
    Restaura un JSON que puede ser:
      1) Dump completo (lista de objetos) generado por `dumpdata`.
      2) Backup “por modelos” (diccionario con clave=modelo y valor=serialización JSON).
    """
    try:
        
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            data = json.load(f)

        
        if isinstance(data, list):
            
            management.call_command('flush', interactive=False, verbosity=0)
            
            management.call_command('loaddata', ruta_archivo, verbosity=0)
            return

        if isinstance(data, dict):
            
            modelos_a_borrar = [
                'libreria.CustomUser',
                'papeleria.Articulo',
                'papeleria.Pedido',
                'papeleria.PedidoArticulo',
            ]
            for model_name in modelos_a_borrar:
                Modelo = apps.get_model(model_name)
                with transaction.atomic():
                    Modelo.objects.all().delete()

            
            for model_name, model_data in data.items():
                temp_file = os.path.join(settings.MEDIA_ROOT, 'temp.json')
                with open(temp_file, 'w', encoding='utf-8') as tf:
                    tf.write(model_data)

                management.call_command('loaddata', temp_file, verbosity=0)
                os.remove(temp_file)

            return

        
        raise ValueError("Formato JSON no reconocido para restauración.")

    except Exception as e:
        raise Exception(f"Error al restaurar JSON: {str(e)}")


def restaurar_backup_sql(ruta_archivo):
    """Para backups SQL, se mantiene igual que antes."""
    db = settings.DATABASES['default']
    try:
        if db['ENGINE'] == 'django.db.backends.mysql':
            comando = f"mysql -u {db['USER']} -p{db['PASSWORD']} {db['NAME']} < {ruta_archivo}"
        elif db['ENGINE'] == 'django.db.backends.postgresql':
            comando = f"psql -U {db['USER']} -d {db['NAME']} -f {ruta_archivo}"
        else:
            raise Exception("Motor de base de datos no soportado")
        subprocess.run(comando, shell=True, check=True)
    except Exception as e:
        raise Exception(f"Error al restaurar SQL: {str(e)}")


def restaurar_backup(ruta_archivo):
    """Función principal de restauración que detecta el tipo de archivo"""
    if ruta_archivo.endswith('.json'):
        return restaurar_backup_json(ruta_archivo)
    elif ruta_archivo.endswith('.sql'):      
        return restaurar_backup_sql(ruta_archivo)
    else:
        raise ValueError("Formato de archivo no soportado")
