import os
import logging
import subprocess
from datetime import datetime
from django.conf import settings
from .models import Backup

# Configuración de logging
logger = logging.getLogger(__name__)

def create_backup():
    # Configuración del comando mysqldump
    user = os.environ.get('DB_USER', settings.DATABASES['default']['USER'])
    password = os.environ.get('DB_PASSWORD', settings.DATABASES['default']['PASSWORD'])
    database = settings.DATABASES['default']['NAME']
    backup_file = os.path.join(settings.MEDIA_ROOT, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql")

    command = [
        "mysqldump",
        f"--user={user}",
        f"--password={password}",
        database
    ]
    
    try:
        logger.info(f"Comando de backup: {' '.join(command)}")
        with open(backup_file, "w") as f:
            result = subprocess.run(command, check=True, capture_output=True, text=True, stdout=f)

        logger.info(f"Backup creado exitosamente: {backup_file}")
        return backup_file

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
        
        # Configuración del comando mysql
        user = settings.DATABASES['default']['USER']
        password = settings.DATABASES['default']['PASSWORD']
        host = settings.DATABASES['default']['HOST']
        port = settings.DATABASES['default']['PORT']
        database = settings.DATABASES['default']['NAME']
        
        command = [
            'mysql',
            f'--user={user}',
            f'--password={password}',
            f'--host={host}',
            f'--port={port}',
            database
        ]
        
        with open(backup_file, 'r') as f:
            subprocess.run(command, stdin=f, check=True)
        
        logger.info(f"Backup restaurado exitosamente desde: {backup_file}")
        return True
    
    except Backup.DoesNotExist as e:
        logger.error(f'Error: No se encontró el backup con ID {backup_id}. {e}')
    except subprocess.CalledProcessError as e:
        logger.error(f'Error al restaurar el backup: {e}')
        logger.error(f'Salida de error: {e.stderr}')
    except Exception as e:
        logger.error(f'Error inesperado al restaurar el backup: {e}')
    
    return False
