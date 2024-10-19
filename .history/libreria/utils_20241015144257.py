import os
import logging
from django.conf import settings
from datetime import datetime
from .models import Backup
import mysql.connector

# Corregido el nombre del logger
logger = logging.getLogger(__name__)

def create_backup(user=None):
    backup_dir = os.path.join(settings.BASE_DIR, 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    
    backup_file = os.path.join(backup_dir, f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.sql')
    
    try:
        # Usa mysqldump para crear el backup
        command = (
            f"mysqldump --user={settings.DATABASES['default']['USER']} "
            f"--password={settings.DATABASES['default']['PASSWORD']} "
            f"--host={settings.DATABASES['default']['HOST']} "
            f"--port={settings.DATABASES['default']['PORT']} "
            f"{settings.DATABASES['default']['NAME']} "
            f"> {backup_file}"
        )
        
        # Ejecuta el comando del sistema
        os.system(command)
        
        backup = Backup.objects.create(
            file_name=os.path.basename(backup_file),
            file_path=backup_file,
            created_by=user
        )
        return backup
    except Exception as e:
        logger.error(f'Error creating backup: {e}')
        return None

def restore_backup(backup_id):
    try:
        backup = Backup.objects.get(id=backup_id)
        backup_file = backup.file_path
        
        # Conéctate a la base de datos
        conn = mysql.connector.connect(
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'],
            database=settings.DATABASES['default']['NAME']
        )
        cursor = conn.cursor()
        
        # Lee el archivo de backup y ejecuta los comandos SQL
        with open(backup_file, 'r') as file:
            sql_script = file.read()
        
        # Ejecuta los comandos SQL en la base de datos
        sql_statements = sql_script.split(';')
        for statement in sql_statements:
            statement = statement.strip()
            if statement:
                try:
                    cursor.execute(statement)
                except mysql.connector.Error as e:
                    logger.error(f'Error executing SQL statement: {e}')
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True
    except Backup.DoesNotExist:
        logger.error(f'Backup with ID {backup_id} does not exist.')
        return False
    except mysql.connector.Error as e:
        logger.error(f'Error restoring backup: {e}')
        return False
    except Exception as e:
        logger.error(f'Unexpected error: {e}')
        return False
