import os
import logging
import subprocess
from django.conf import settings
from datetime import datetime
from .models import Backup
import comand
# Al principio de utils.py
logger = logging.getLogger(__name__)

def create_backup():
    try:
        # ... (código existente) ...
        logger.info(f"Comando de backup: {' '.join(command)}")
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logger.info(f"Backup creado exitosamente: {backup_file}")
        return backup
    except FileNotFoundError as e:
        logger.error(f"Error: No se encontró el ejecutable mysqldump. Asegúrate de que MySQL esté instalado y en el PATH. {e}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error al crear el backup: {e}")
        logger.error(f"Salida de error: {e.stderr}")
    except Exception as e:
        logger.error(f"Error inesperado al crear el backup: {e}")
    return None

def restore_backup(backup_id):
    try:
        backup = Backup.objects.get(id=backup_id)
        backup_file = backup.file_path
        
        # Comando para restaurar la base de datos usando mysql
        command = [
            'mysql',
            '--user=' + settings.DATABASES['default']['USER'],
            '--password=' + settings.DATABASES['default']['PASSWORD'],
            '--host=' + settings.DATABASES['default']['HOST'],
            '--port=' + str(settings.DATABASES['default']['PORT']),
            settings.DATABASES['default']['NAME'],
            '--execute=' + f'SOURCE {backup_file}'
        ]
        
        subprocess.run(command, check=True)
        return True
    except (Backup.DoesNotExist, subprocess.CalledProcessError) as e:
        print(f'Error al restaurar el backup: {e}')
        return False
