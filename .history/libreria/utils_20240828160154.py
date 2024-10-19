import os
from django.conf import settings
from datetime import datetime
import mysql.connector
from mysql.connector import Error
from .models import Backup

def create_backup(user=None):
    # Directorio para guardar los backups
    backup_dir = os.path.join(settings.BASE_DIR, 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    
    # Nombre del archivo de backup basado en la fecha y hora actuales
    backup_file = os.path.join(backup_dir, f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.sql')
    
    # Conexión a la base de datos
    try:
        connection = mysql.connector.connect(
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'],
            database=settings.DATABASES['default']['NAME']
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Comando para crear el backup de la base de datos usando mysqldump
            backup_command = f"mysqldump --user={settings.DATABASES['default']['USER']} --password={settings.DATABASES['default']['PASSWORD']} --host={settings.DATABASES['default']['HOST']} --port={settings.DATABASES['default']['PORT']} {settings.DATABASES['default']['NAME']} > {backup_file}"
            
            os.system(backup_command)
            
            # Crear un registro en la base de datos para el backup
            backup = Backup.objects.create(
                file_name=os.path.basename(backup_file),
                file_path=backup_file,
                created_by=user  # Asignar el usuario que crea el backup, si se proporciona
            )
            
            return backup
    except Error as e:
        print(f'Error al crear el backup: {e}')
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def restore_backup(backup_id):
    try:
        backup = Backup.objects.get(id=backup_id)
        backup_file = backup.file_path
        
        # Conexión a la base de datos
        connection = mysql.connector.connect(
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'],
            database=settings.DATABASES['default']['NAME']
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Comando para restaurar la base de datos usando mysql
            restore_command = f"mysql --user={settings.DATABASES['default']['USER']} --password={settings.DATABASES['default']['PASSWORD']} --host={settings.DATABASES['default']['HOST']} --port={settings.DATABASES['default']['PORT']} {settings.DATABASES['default']['NAME']} < {backup_file}"
            
            os.system(restore_command)
            return True
    except (Backup.DoesNotExist, Error) as e:
        print(f'Error al restaurar el backup: {e}')
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
