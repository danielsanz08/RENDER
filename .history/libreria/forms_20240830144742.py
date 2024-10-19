from django import forms
from .models import Transaccion, Insumo,CustomUser,Backup
from django.contrib.auth import authenticate
class TransaccionForm(forms.ModelForm):
    from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model

class Meta:
        model = Transaccion
        fields = ['tipo', 'monto', 'descripcion', 'fecha']
        
class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ['nombre', 'descripcion', 'cantidad']
class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['profile_picture', 'name', 'email', 'role', 'phone', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Las contraseñas no coinciden.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        password = cleaned_data.get("password")

        if not name or not password:
            raise forms.ValidationError("Nombre y contraseña son requeridos.")
        
        return cleaned_data
    
class BackupForm(forms.ModelForm):
    class Meta:
        model = Backup
        fields = ['file_name', 'file_path']
        widgets = {
            'file_name': forms.TextInput(attrs={'placeholder': 'Nombre del archivo'}),
            'file_path': forms.TextInput(attrs={'placeholder': 'Ruta del archivo'}),
        }
        
User = get_user_model()

class CustomCambioForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label='Contraseña actual')
    new_password1 = forms.CharField(widget=forms.PasswordInput, label='Nueva contraseña')
    new_password2 = forms.CharField(widget=forms.PasswordInput, label='Confirmar nueva contraseña')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("La contraseña actual es incorrecta.")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        if new_password1 != new_password2:
            raise forms.ValidationError("Las nuevas contraseñas no coinciden.")
        return cleaned_data

    def save(self):
        new_password = self.cleaned_data.get('new_password1')
        self.user.set_password(new_password)
        self.user.save()