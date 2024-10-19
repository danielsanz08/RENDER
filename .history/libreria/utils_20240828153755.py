from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Backup
from .utils import create_backup, restore_backup

@login_required
def backup_view(request):
    if request.method == 'POST':
        if 'create_backup' in request.POST:
            success = create_backup()
            if success:
                messages.success(request, 'Copia de seguridad creada exitosamente.')
            else:
                messages.error(request, 'Error al crear la copia de seguridad.')
        elif 'restore_backup' in request.POST:
            backup_id = request.POST.get('backup_id')
            if backup_id:
                success = restore_backup(backup_id)
                if success:
                    messages.success(request, 'Base de datos restaurada exitosamente.')
                else:
                    messages.error(request, 'Error al restaurar la base de datos.')
            else:
                messages.error(request, 'ID de copia de seguridad no proporcionado.')
        elif 'delete_backup' in request.POST:
            backup_id = request.POST.get('backup_id')
            if backup_id:
                try:
                    backup = Backup.objects.get(id=backup_id)
                    backup.delete()
                    messages.success(request, 'Copia de seguridad eliminada exitosamente.')
                except Backup.DoesNotExist:
                    messages.error(request, 'Copia de seguridad no encontrada.')
            else:
                messages.error(request, 'ID de copia de seguridad no proporcionado.')

    backups = Backup.objects.all().order_by('-created_at')
    return render(request, 'backup_restore/backup.html', {'backups': backups})
