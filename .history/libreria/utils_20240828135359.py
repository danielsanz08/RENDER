import os
import subprocess
from django.conf import settings
from datetime import datetime
from .models import Backup

def create_backup():
    # Directorio para guardar los backups
    backup_dir = os.path.join(settings.BASE_DIR, 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    
    # Nombre del archivo de backup basado en la fecha y hora actuales
    backup_file = os.path.join(backup_dir, f'backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.sql')
    
    # Comando para crear el backup de la base de datos usando mysqldump
    command = [
        'mysqldump',
        '--user=' + settings.DATABASES['default']['USER'],
        '--password=' + settings.DATABASES['default']['PASSWORD'],
        '--host=' + settings.DATABASES['default']['HOST'],
        '--port=' + str(settings.DATABASES['default']['PORT']),
        settings.DATABASES['default']['NAME'],
        '--result-file=' + backup_file
    ]
    
    try:
        # Ejecutar el comando y crear el backup
        subprocess.run(command, check=True)
        
        # Crear un registro en la base de datos para el backup
        backup = Backup.objects.create(
            file_name=os.path.basename(backup_file),
            file_path=backup_file,
            created_by=None  # Cambia esto para usar el usuario adecuado si es necesario
        )
        
        return backup
    except subprocess.CalledProcessError as e:
        print(f'Error al crear el backup: {e}')
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
