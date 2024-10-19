import os
import subprocess
from django.conf import settings
from datetime import datetime
from .models import Backup

def create_backup():
    # ...
    password = settings.DATABASES['default']['PASSWORD']
    password_arg = f'--password={password}' if password else ''
    
    command = [
        'mysqldump',
        f'--user={settings.DATABASES["default"]["USER"]}',
        password_arg,
        f'--host={settings.DATABASES["default"]["HOST"]}',
        f'--port={settings.DATABASES["default"]["PORT"]}',
        settings.DATABASES['default']['NAME'],
        f'--result-file={backup_file}'
    ]
    
    # Elimina los elementos vacíos de la lista command
    command = [arg for arg in command if arg]

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
